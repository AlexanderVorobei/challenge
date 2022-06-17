from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model

User = get_user_model()


class Schema(models.Model):
    class Delimiter(models.TextChoices):
        COMMA = "comma ( , )"
        SEMICOLON = "semicolon ( ; )"
        COLON = "colon ( : )"
        TAB = "tab (   )"

    class Quote(models.TextChoices):
        DOUBLE_QUOTE = 'Double-quote ( " )'
        SINGLE_QUOTE = "Single-quote ( ' )"

    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=128)
    column_separator = models.CharField(
        max_length=24, choices=Delimiter.choices, default=Delimiter.COMMA
    )
    string_character = models.CharField(
        max_length=24, choices=Quote.choices, default=Quote.SINGLE_QUOTE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "schema"
        verbose_name_plural = "schemas"


class Column(models.Model):
    class Type(models.TextChoices):
        FULLNAME = "Full name"
        JOB = "Job"
        EMAIL = "Email"
        DOMAINNAME = "Domain name"
        COMPANYNAME = "Company name"
        TEXT = "Text"
        INTEGER = "Integer"
        ADDRESS = "Address"
        DATE = "Date"

    schema = models.ForeignKey(Schema, related_name="columns", on_delete=CASCADE)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=24, choices=Type.choices, default=Type.TEXT)
    filter = models.JSONField(null=True, blank=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.name} - {self.schema.name}"

    class Meta:
        unique_together = ("schema", "order")
        verbose_name = "column"
        verbose_name_plural = "columns"


class DataSet(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "Processing"
        READY = "Ready"

    schema = models.ForeignKey(
        Schema, related_name="datasets_schema", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=24, choices=Status.choices, default=Status.PROCESSING
    )
    rows = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.schema.name} - {self.status}"

    class Meta:
        verbose_name = "dataSet"
        verbose_name_plural = "dataSet"
