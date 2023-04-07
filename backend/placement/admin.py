from django.contrib import admin
from placement import models as m

# Register your models here.


@admin.register(m.StudentOpening)
class StudentOpeningManager(admin.ModelAdmin):
    list_display = (
        "student",
        "opening",
        "applied",
        "selected",
        "accepted",
    )
    list_filter = (
        "applied",
        "selected",
        "accepted",
    )



@admin.register(m.OnCampusPlacedDetail)
class OnCampusPlacedDetailManager(admin.ModelAdmin):
    pass


@admin.register(m.OffCampusPlacedDetail)
class OffCampusPlacedDetailManager(admin.ModelAdmin):
    pass
