from django.contrib import admin

from .models import Schema, SchemaColumns, DataSet


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "name",
        "column_separator",
        "string_character",
    ]
    list_display = [
        "id",
        "user",
        "name",
        "column_separator",
        "string_character",
        "created_at",
        "updated_at",
    ]


@admin.register(SchemaColumns)
class ColumnAdmin(admin.ModelAdmin):
    fields = [
        "schema",
        "column_name",
        "column_type",
        "column_from",
        "column_to",
        "column_order",
    ]
    list_display = [
        "id",
        "schema",
        "column_name",
        "column_type",
        "column_order",
    ]


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "schema",
        "created_at",
        "file",
    ]
    readonly_fields = ["file"]

    def get_field_queryset(self, db, db_field, request):
        return db_field.remote_field.model.objects.filter(user=request.user)
