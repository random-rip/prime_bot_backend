from django.contrib import admin


class ScoutingWebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'separator', 'multi', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'name', 'name']
    search_fields = ['name', 'base_url']
    readonly_fields = (
        "created_at",
        "updated_at",
    )
