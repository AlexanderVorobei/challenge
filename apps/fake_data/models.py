from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Schema(models.Model):
    class ColumnSeparator(models.TextChoices):
        COMMA = "comma [,]"
        SEMICOLON = "semicolon [;]"
        COLON = "colon [:]"

    class StringCharacter(models.TextChoices):
        DOUBLE_QUOTE = 'double quote ["]'
        APOSTROPHE = "apostrophe [']"

    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=128)
    column_separator = models.CharField(max_length=16, choices=ColumnSeparator.choices)
    string_character = models.CharField(max_length=16, choices=StringCharacter.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "schema"
        verbose_name_plural = "schemas"


class SchemaColumns(models.Model):
    class ColumnType(models.TextChoices):
        FULL_NAME = "Full name"
        JOB = "Job"
        EMAIL = "Email"
        DOMAIN_NAME = "Domain name"
        COMPANY_NAME = "Company name"
        TEXT = "Text"
        INTEGER = "Integer"
        ADDRESS = "Address"
        DATE = "Date"

    schema = models.ForeignKey(Schema, related_name="columns_schema", on_delete=CASCADE)
    column_name = models.CharField(max_length=128)
    column_type = models.CharField(max_length=16, choices=ColumnType.choices)
    column_from = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    column_to = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    column_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.column_order}:{self.column_name}"

    class Meta:
        verbose_name = "column"
        verbose_name_plural = "columns"


class DataSet(models.Model):
    schema = models.ForeignKey(
        Schema, related_name="datasets_schema", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_ready = models.BooleanField(default=False)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.schema.name} - {self.is_ready}"

    class Meta:
        verbose_name = "dataSet"
        verbose_name_plural = "dataSet"
