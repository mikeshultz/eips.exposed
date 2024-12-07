from datetime import UTC, datetime

from eips import EIPs, ERCs

from eips_etl.models import Commit, Document


def import_repo(mecha: type[EIPs] | type[ERCs], /, **kwargs) -> int:
    """Import all new items to the repo."""
    ymd = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
    batch_name = f"{mecha.__name__.lower()}-import-{ymd}"
    docs = mecha(**kwargs)
    docs.repo_fetch()

    doc_fields = [f.name for f in Document._meta.fields if f.name != "document_id"]

    count = 0
    for commit, doc in docs.all():
        commit_id = commit.id.decode()
        cdict = Commit.dulwich_to_dict(commit)
        cobj, _created = Commit.objects.update_or_create(**cdict)

        dinst, new_authors = Document.from_dict(cobj, doc.model_dump())
        updates = {k: v for k, v in dinst.__dict__.items() if k in doc_fields}

        existing = Document.objects.filter(
            document_number=doc.id, commit_id=commit_id
        ).first()

        def save_and_add_rels():
            dinst.save()

            for author in new_authors:
                author.save()
                dinst.authors.add(author)

            for message in doc.errors:
                dinst.errors.create(import_batch=batch_name, message=message)

        if not existing:
            save_and_add_rels()
        elif existing.reimport:
            existing.delete()
            save_and_add_rels()
        elif updates:
            for k, v in updates.items():
                setattr(existing, k, v)
            existing.save()

        count += 1

    return count
