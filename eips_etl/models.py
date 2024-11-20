from enum import Enum
from typing import Self

from django.contrib.postgres.fields import ArrayField
from django.db import models
from dulwich.objects import Commit as DulwichCommit
from eips.enum import DocumentType, EIP1Category, EIP1Status, EIP1Type
from eips.util import gitstamp_to_dt


def enum_to_choices(en: type[Enum]) -> list[tuple[str, str]]:
    """Convert a Python Enum to Django choices."""
    return [(e.name, e.value) for e in en]


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    # TODO: Parse the constiuent parts to something more useful
    person_string = models.CharField(max_length=1024)

    def __str__(self) -> str:
        return str(self.person_string)


class Commit(models.Model):
    commit_id = models.CharField(primary_key=True, max_length=40)

    author = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="author"
    )
    committer = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="committer"
    )

    author_time = models.DateTimeField()
    commit_time = models.DateTimeField()
    gpg_sig = models.TextField(default="", null=False)
    message = models.TextField(default="", null=False)
    parents = ArrayField(models.CharField(max_length=40))

    def __str__(self) -> str:
        return str(self.commit_id)[:7]

    @classmethod
    def from_dulwich(cls, commit: DulwichCommit) -> Self:
        author_time = gitstamp_to_dt(commit.author_time, commit.author_timezone)
        commit_time = gitstamp_to_dt(commit.commit_time, commit.commit_timezone)
        return cls(
            commit_id=commit.id.decode(),
            author=Person.objects.get_or_create(person_string=commit.author)[0],
            committer=Person.objects.get_or_create(person_string=commit.committer)[0],
            author_time=author_time,
            commit_time=commit_time,
            gpg_sig=commit.gpgsig or b"",
            message=commit.message or b"",
            parents=[p.decode() for p in commit.parents],
        )


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    document_id = models.IntegerField()
    # commit = models.CharField(max_length=40)
    commit = models.ForeignKey("Commit", on_delete=models.CASCADE)
    document_type = models.CharField(
        max_length=3, choices=enum_to_choices(DocumentType)
    )
    created = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True, default=None)

    status = models.CharField(max_length=20, choices=enum_to_choices(EIP1Status))
    category = models.CharField(
        max_length=20,
        default="",
        blank=True,
        choices=enum_to_choices(EIP1Category),
    )
    type = models.CharField(
        max_length=20,
        default="",
        blank=True,
        choices=enum_to_choices(EIP1Type),
    )
    resolution = models.CharField(max_length=1024, default="", blank=True)
    title = models.CharField(max_length=1024, default="", blank=True)
    discussions_to = models.CharField(max_length=2048, default="", blank=True)
    review_period_end = models.CharField(max_length=2048, default="", blank=True)

    requires = ArrayField(models.IntegerField())
    replaces = ArrayField(models.IntegerField())
    superseded_by = ArrayField(models.IntegerField())

    description = models.TextField()
    body = models.TextField()

    # authors = models.ForeignKey("Person", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Person")

    error_message = models.CharField(max_length=2028, default="", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["document_id", "document_type"]),
            models.Index(fields=["commit"]),
        ]
        unique_together = [["document_id", "commit"]]

    def __str__(self) -> str:
        return f"<Document: {self.document_type} {self.document_id}: {self.title}>"

    @classmethod
    def from_dict(cls, commit: Commit, doc: dict) -> Self:
        new_doc = cls(
            document_id=doc["id"],
            commit=commit,
            document_type=doc["document_type"].value,
            created=doc["created"],
            updated=doc["updated"],
            category=doc["category"] or "",
            status=doc["status"].value,
            type=doc["type"] or "",
            resolution=doc["resolution"] or "",
            title=doc["title"] or "",
            discussions_to=doc["discussions_to"] or "",
            review_period_end=doc["review_period_end"] or "",
            requires=doc.get("requires") or list(),
            replaces=doc.get("replaces") or list(),
            superseded_by=doc.get("superseded_by") or list(),
            description=doc["description"],
            body=doc["body"],
        )

        if doc_authors := doc.get("authors", []):
            authors = Person.objects.filter(person_string__in=doc_authors)

            if len(doc_authors) != len(authors):
                unmatched = set(doc_authors) - set([str(a) for a in authors])

                for author_str in unmatched:
                    author = Person(author_string=author_str)
                    author.save()
                    authors.append(author)

            new_doc.authors = authors

        return new_doc
