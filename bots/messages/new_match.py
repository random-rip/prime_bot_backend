from django.utils.translation import gettext as _

from bots.messages.base import MatchMessage


class NewMatchNotification(MatchMessage):
    """
    Teamaktualisierungen generieren keine Benachrichtigungen, deswegen ist die Message silenced.
    (Bisher gedacht für Kalibrierungsspiele, kann aber auf die Starterdivision ausgeweitet werden)
    # TODO implementieren von einem oder mehreren neuen Matches
    """
    settings_key = "NEW_MATCH_NOTIFICATION"
    mentionable = True

    def __init__(self, team_id: int, match_id: int):
        super().__init__(team_id=team_id, match_id=match_id)

    def _generate_title(self):
        return "🔥 " + _("New match")

    def _generate_message(self):
        return _(
            "Your next match in the calibration stage:\n"
            "[{match_day}]({match_url}) against [{enemy_team_tag}]({enemy_team_url}):\n"
            "Here is your [{website} link]({scouting_url}) of the team."
        ).format(
            match_day=self.match_helper.display_match_day(self.match),
            match_url=self.match_url,
            enemy_team_tag=self.match.enemy_team.team_tag,
            enemy_team_url=self.enemy_team_url,
            website=self.scouting_website,
            scouting_url=self.enemy_team_scouting_url,
        )
