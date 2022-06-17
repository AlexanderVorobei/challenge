import io
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from faker import Faker

User = get_user_model()


class Schema(models.Model):
    class Meta:
        verbose_name = "schema"
        verbose_name_plural = "schemas"

    class Delimiter(models.TextChoices):
        COMMA = ",", "comma ( , )"
        SEMICOLON = ";", "semicolon ( ; )"
        COLON = ":", "colon ( : )"

    class Quote(models.TextChoices):
        DOUBLE_QUOTE = '"', 'Double-quote ( " )'
        SINGLE_QUOTE = "'", "Single-quote ( ' )"

    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=128)
    column_separator = models.CharField(
        max_length=24, choices=Delimiter.choices, default=Delimiter.COMMA
    )
    string_character = models.CharField(
        max_length=24, choices=Quote.choices, default=Quote.SINGLE_QUOTE
    )
    columns = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class ColumnGenerator:
    TYPES = (
        "full_name",
        "job",
        "email",
        "domain_name",
        "company_name",
        "text",
        "integer",
        "address",
        "date",
    )

    def __init__(self, schema: Schema):
        self.schema = schema
        self.faker = Faker()

    @classmethod
    def choices(cls):
        return [
            (data_type, data_type.replace("_", " ").title()) for data_type in cls.TYPES
        ]

    def _wrapper(self, value: str):
        return self.schema.string_character + value + self.schema.string_character

    def full_name(self):
        return self._wrapper(self.faker.name())

    def job(self):
        return self._wrapper(self.faker.job())

    def domain_name(self):
        return self.faker.domain_name()

    def phone_number(self):
        return self.faker.msisdn()

    def company_name(self):
        return self._wrapper(self.faker.company())

    def address(self):
        return self._wrapper(self.faker.address().replace("\n", ", "))

    def date(self):
        return self.faker.date()

    def __getitem__(self, item):
        return getattr(self, item)()

    def generate(self, rows):
        names = [x["name"] for x in self.schema.columns.get("schema")]
        types = [x["type"] for x in self.schema.columns.get("schema")]
        separator = self.schema.column_separator
        yield separator.join(names) + "\n"
        for _ in range(rows):
            yield separator.join(self[t] for t in types) + "\n"


class DataSet(models.Model):
    class Meta:
        verbose_name = "dataSet"
        verbose_name_plural = "dataSet"

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
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.schema.id}-{self.schema.name} - {self.created_at}"

    def update_dataset(self):
        generator = ColumnGenerator(self.schema)
        with io.BytesIO() as buffer:
            for line in generator.generate(rows=self.rows):
                buffer.write(line.encode("utf-8"))
            self.file.save(
                (
                    "{0}-{1}-{2}.csv".format(
                        self.schema.id, self.schema.name, self.created_at
                    )
                ),
                ContentFile(buffer.getbuffer()),
            )
            self.status = self.Status.READY
        return True
