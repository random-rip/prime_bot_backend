from django.test import TestCase

from app_prime_league.models import Match, Team, Player
from core.comparers.match_comparer import MatchComparer
from core.test_utils import string_to_datetime, create_temporary_match_data


class SuggestionsTest(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(id=1, name="Team 1", team_tag="T1")
        self.enemy_team = Team.objects.create(id=2, name="Team 2", team_tag="T2")

    def test_enemy_made_a_first_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                         latest_suggestions=[
                                             string_to_datetime("2022-01-01 17:00")
                                         ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_new_suggestion(of_enemy_team=True),
                        "Enemy Team had new suggestion, but was not recognized")

    def test_enemy_has_existing_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                         latest_suggestions=[
                                             string_to_datetime("2022-01-01 17:00")
                                         ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=True),
                         "Enemy Team has existing suggestion, but not new")

    def test_enemy_made_new_suggestion_after_own_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                         latest_suggestions=[
                                             string_to_datetime("2022-01-01 17:00")
                                         ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_new_suggestion(of_enemy_team=True),
                        "Enemy Team had new suggestion, but was not recognized")

    def test_team_made_a_first_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                         latest_suggestions=[
                                             string_to_datetime("2022-01-01 17:00")
                                         ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_new_suggestion(of_enemy_team=False),
                        "Team had new suggestion, but was not recognized")

    def test_team_has_existing_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                         latest_suggestions=[
                                             string_to_datetime("2022-01-01 17:00")
                                         ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=False),
                         "Team has existing suggestion, but not new")

    def test_team_made_new_suggestion_after_enemy_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                         latest_suggestions=[
                                             string_to_datetime("2022-01-01 17:00")
                                         ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_new_suggestion(of_enemy_team=False),
                        "Team had new suggestion, but was not recognized")

    def test_no_open_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=None,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=None, )
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=True),
                         "No open suggestion, but was recognized as new")

    def test_no_open_suggestion_and_last_suggestion_was_made_of_team(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=None, )
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=True),
                         "No open suggestion, but was recognized as new")
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=False),
                         "No open suggestion, but was recognized as new")

    def test_no_open_suggestion_and_last_suggestion_was_made_of_enemy(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, team_made_latest_suggestion=None, )
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=True),
                         "No open suggestion, but was recognized as new")
        self.assertFalse(cp.compare_new_suggestion(of_enemy_team=False),
                         "No open suggestion, but was recognized as new")


class CompareConfirmationTest(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(id=1, name="Team 1", team_tag="T1")
        self.enemy_team = Team.objects.create(id=2, name="Team 2", team_tag="T2")

    def test_new_accepted_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=True,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, match_begin_confirmed=True)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_scheduling_confirmation(), "Enemy accepted suggestion, but was not recognized")

    def test_still_accepted_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, match_begin_confirmed=True,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, match_begin_confirmed=True)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_scheduling_confirmation(), "Accepted Match Begin, but was recognized as new")

    def test_no_accepted_suggestion(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team, team_made_latest_suggestion=False,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, match_begin_confirmed=False)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_scheduling_confirmation(), "No accepted Match Begin, but was recognized")


class CompareNewLineupTest(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(id=1, name="Team 1", team_tag="T1")
        self.enemy_team = Team.objects.create(id=2, name="Team 2", team_tag="T2")

    def test_no_lineup(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_lineup_confirmation(of_enemy_team=True),
                         "Enemy has no lineup, but was not recognized")

    def test_fresh_new_lineup(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team,
                                     has_side_choice=True)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, enemy_lineup=[
            (1, "Player 1", "Summonername 1", None),
            (2, "Player 2", "Summonername 2", None),
            (3, "Player 3", "Summonername 3", None),
            (4, "Player 4", "Summonername 4", None),
            (5, "Player 5", "Summonername 5", None),
        ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_lineup_confirmation(of_enemy_team=True),
                        "Enemy has fresh new lineup, but was not recognized")

    def test_existing_lineup(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team,
                                     has_side_choice=True)
        players = Player.objects.create_or_update_players([
            (1, "Player 1", "Summonername 1", False),
            (5, "Player 5", "Summonername 5", False),
        ], self.enemy_team)
        match.enemy_lineup.add(*players)
        match.save()
        match.refresh_from_db()
        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, enemy_lineup=[
            (1, "Player 1", "Summonername 1", None),
            (5, "Player 5", "Summonername 5", None),
        ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_lineup_confirmation(of_enemy_team=True),
                         "Enemy has no new lineup, but was not recognized as new")

    def test_new_lineup(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     enemy_team=self.enemy_team,
                                     has_side_choice=True)
        players = Player.objects.create_or_update_players([
            (1, "Player 1", "Summonername 1", False),
            (5, "Player 5", "Summonername 5", False),
        ], self.enemy_team)
        match.enemy_lineup.add(*players)
        match.save()
        match.refresh_from_db()
        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team, enemy_lineup=[
            (1, "Player 1", "Summonername 1", None),
            (2, "Player 2", "Summonername 2", None),
        ])
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_lineup_confirmation(of_enemy_team=True),
                        "Enemy has new lineup, but was not recognized")


class CompareEnemyTeamIDTest(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(id=1, name="Team 1", team_tag="T1")
        self.enemy_team = Team.objects.create(id=2, name="Team 2", team_tag="T2")

    def test_not_set(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     has_side_choice=True, enemy_team=None)

        md = create_temporary_match_data(team=self.team)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_enemy_team())

    def test_not_changed(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     has_side_choice=True, enemy_team=self.enemy_team)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertFalse(cp.compare_new_enemy_team())

    def test_new_set(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     has_side_choice=True, enemy_team=None)

        md = create_temporary_match_data(team=self.team, enemy_team=self.enemy_team)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_new_enemy_team())

    def test_unset(self):
        match = Match.objects.create(match_id=1, match_day=1, match_type=Match.MATCH_TYPE_LEAGUE, team=self.team,
                                     has_side_choice=True, enemy_team=self.enemy_team)

        md = create_temporary_match_data(team=self.team, enemy_team=None)
        cp = MatchComparer(match_old=match, match_new=md)
        self.assertTrue(cp.compare_new_enemy_team())