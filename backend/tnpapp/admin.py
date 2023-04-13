from django.contrib import admin
from typing import Tuple, Any, Iterable
from copy import deepcopy
from django.http import HttpResponse
import csv
from django.contrib.auth.admin import UserAdmin as UserAdmin_
from django.utils.functional import cached_property


class CustomUserAdmin(UserAdmin_):
    new_fields: Tuple[str, ...]
    new_add_fields: Tuple[str, ...]
    new_list_filters: Tuple[str, ...]

    default_exclude = ("username",)

    def append_primary_fields(
        self,
        old_fields: Tuple[str, ...],
        new_fields: Tuple[str, ...],
        exclusions: Tuple[str, ...] = (),
    ):
        # exclude = ("username", "email")
        old_fields = deepcopy(old_fields)
        old_fields[0][1]["fields"] = tuple(
            i for i in (old_fields[0][1]["fields"] + new_fields) if i not in exclusions
        )
        return old_fields

    @cached_property
    def fieldsets(self):
        if not hasattr(self, "new_fields"):
            self.new_fields = ()
        return self.append_primary_fields(super().fieldsets, self.new_fields)

    @cached_property
    def add_fieldsets(self):
        if not hasattr(self, "new_add_fields"):
            self.new_add_fields = ()
        return self.append_primary_fields(
            super().add_fieldsets,
            (*self.new_fields, *self.new_add_fields),
            exclusions=self.default_exclude,
        )

    @cached_property
    def list_filter(self):
        if not hasattr(self, "new_list_filters"):
            self.new_list_filters = ()
        return super().list_filter + self.new_list_filters


# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/actions/#actions-that-provide-intermediate-pages
# https://docs.djangoproject.com/en/4.1/howto/outputting-csv/
# TODO : add custom permission for exports
def export_as_csv(modeladmin, request, queryset) -> HttpResponse:
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


admin.site.add_action(export_as_csv, "export_selected")

# def append_primary_fields(
#     data: Tuple[Any, ...],
#     new_fields=Set[str],
# ):
#     tmp_data = copy(data)
#     tupleset = set(tmp_data[0][1]["fields"]).union(new_fields)
#     tmp_data[0][1]["fields"] = tuple(tupleset)
#     return tmp_data
