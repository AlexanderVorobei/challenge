from typing import Generator
from faker import Faker
from .models import Schema


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

    def generate(self, rows, *args) -> Generator[str]:
        names = [x["name"] for x in self.schema.columns.get("schema")]
        types = [x["type"] for x in self.schema.columns.get("schema")]
        sep = self.schema.column_delimiter
        yield sep.join(names) + "\n"
        for _ in range(rows):
            yield sep.join(self[t] for t in types) + "\n"
