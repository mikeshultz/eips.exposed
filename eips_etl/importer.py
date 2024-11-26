from eips import EIPs, ERCs

from eips_etl.models import Commit, Document


def import_repo(mecha: type[EIPs] | type[ERCs], /, **kwargs) -> int:
    """Import all new items to the repo."""
    docs = mecha(**kwargs)
    docs.repo_fetch()

    doc_fields = [f.name for f in Document._meta.fields if f.name != "id"]

    count = 0
    for commit, doc in docs.all():
        commit_id = commit.id.decode()
        cdict = Commit.dulwich_to_dict(commit)
        cobj, _created = Commit.objects.update_or_create(**cdict)

        dobj, new_authors = Document.from_dict(cobj, doc.model_dump())
        updates = {k: v for k, v in dobj.__dict__.items() if k in doc_fields}

        if not Document.objects.filter(document_id=doc.id, commit_id=commit_id).update(
            **updates
        ):
            dobj.save()
            for author in new_authors:
                author.save()
                dobj.authors.add(author)

        count += 1

    return count
