from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html


class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_id', 'match_day', 'match_type', 'team', 'enemy_team', 'begin', 'closed', "prime_league_link",
                    'result', 'created_at', 'updated_at', ]
    list_filter = ['match_day', 'match_type', 'created_at', 'updated_at', 'begin']
    readonly_fields = ("created_at", "updated_at",)
    filter_vertical = ("enemy_lineup", "team_lineup",)
    search_fields = ['team__id', 'team__name', 'enemy_team__id', 'enemy_team__name', 'match_id']

    def prime_league_link(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Zur PL</a>&nbsp;',
            f"{settings.MATCH_URI}{obj.match_id}",
        )

    prime_league_link.allow_tags = True
    prime_league_link.short_description = "Prime League"


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'begin', 'match', 'created_at']
