from django.contrib import admin
from django_q.admin import FailAdmin as DjangoQ2FailAdmin
from django_q.admin import ScheduleAdmin as DjangoQ2ScheduleAdmin
from django_q.admin import TaskAdmin as DjangoQ2TaskAdmin
from django_q.models import Failure, Schedule, Success

admin.site.unregister(Schedule)
admin.site.unregister(Failure)
admin.site.unregister(Success)


class ScheduleAdmin(DjangoQ2ScheduleAdmin):
    """Removed the 'func' field from the list_display."""

    list_display = (
        "id",
        "name",
        "schedule_type",
        "repeats",
        "cluster",
        "next_run",
        "get_last_run",
        "get_success",
    )


class TaskAdmin(DjangoQ2TaskAdmin):
    """Removed the 'func' field from the list_display."""

    search_fields = ("name", "group")
    list_display = (
        "name",
        "group",
        "cluster",
        "started",
        "stopped",
        "time_taken",
    )
    list_filter = ["cluster"]


class FailAdmin(DjangoQ2FailAdmin):
    """Removed the 'func' field from the list_display."""

    list_display = (
        "name",
        "group",
        "cluster",
        "started",
        "stopped",
        "short_result",
    )
    list_filter = ["cluster"]
