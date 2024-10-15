from django.test import TestCase

from app_prime_league.models import Match, Player, Team
from core.comparers.match_comparer import NewCommentsComparer
from core.test_utils import create_comment, create_temporary_comment, create_temporary_match_data


class CompareCommentsTest(TestCase):
    def setUp(self) -> None:
        self.team_a = Team.objects.create(id=1, name="Team A", team_tag="TA")
        self.team_b = Team.objects.create(id=2, name="Team B", team_tag="TB")
        self.team_a_player = Player.objects.create_or_update_players(
            [
                (1, "Player 1", "Summonername 1", False),
            ],
            self.team_a,
        )[0]
        self.enemy_player = Player.objects.create_or_update_players(
            [
                (10, "EnemyPlayer 10", "Summonername 10", False),
            ],
            self.team_b,
        )[0]

    def test_no_comments(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        md = create_temporary_match_data(
            team=self.team_a,
            enemy_team=self.team_b,
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "No comments, but new comments were recognized")

    def test_existing_comments(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )
        create_comment(comment_id=1, user_id=1, match=match)
        md = create_temporary_match_data(
            team=self.team_a, enemy_team=self.team_b, comments=[create_temporary_comment(comment_id=1, user_id=1)]
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "1 comment exists, but new comments were recognized")

    def test_new_comment_of_team(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        md = create_temporary_match_data(
            team=self.team_a, enemy_team=self.team_b, comments=[create_temporary_comment(comment_id=1, user_id=1)]
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "New comment of members, but recognized as new")

    def test_new_comment_of_enemy_team(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        md = create_temporary_match_data(
            team=self.team_a, enemy_team=self.team_b, comments=[create_temporary_comment(comment_id=10, user_id=10)]
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertListEqual(cp.compare(), [10], "New comment, but not recognized")

    def test_new_comment_of_random_user_id(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        md = create_temporary_match_data(
            team=self.team_a, enemy_team=self.team_b, comments=[create_temporary_comment(comment_id=100, user_id=100)]
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertListEqual(cp.compare(), [100], "New comment, but not recognized")

    def test_deleted_comment_of_team(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        create_comment(comment_id=1, user_id=1, match=match)
        md = create_temporary_match_data(team=self.team_a, enemy_team=self.team_b, comments=[])
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "No comment, but not recognized")

    def test_deleted_comment_of_enemy_team(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        create_comment(comment_id=10, user_id=10, match=match)
        md = create_temporary_match_data(team=self.team_a, enemy_team=self.team_b, comments=[])
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "No comment, but not recognized")

    def test_deleted_comment_of_random_user_id(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        create_comment(comment_id=100, user_id=100, match=match)
        md = create_temporary_match_data(team=self.team_a, enemy_team=self.team_b, comments=[])
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "No comment, but not recognized")

    def test_multiple_new_comments(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        md = create_temporary_match_data(
            team=self.team_a,
            enemy_team=self.team_b,
            comments=[
                create_temporary_comment(comment_id=1, user_id=1),
                create_temporary_comment(comment_id=100, user_id=100),
                create_temporary_comment(comment_id=10, user_id=10),
            ],
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertListEqual(cp.compare(), [10, 100], "Expected 2 new comments")

    def test_multiple_deletions(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        create_comment(comment_id=1, user_id=1, match=match)
        create_comment(comment_id=101, user_id=100, match=match)
        create_comment(comment_id=100, user_id=100, match=match)
        create_comment(comment_id=10, user_id=10, match=match)
        create_comment(comment_id=11, user_id=10, match=match)
        md = create_temporary_match_data(
            team=self.team_a,
            enemy_team=self.team_b,
            comments=[
                create_temporary_comment(comment_id=1, user_id=1),
                create_temporary_comment(comment_id=100, user_id=100),
                create_temporary_comment(comment_id=10, user_id=10),
            ],
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertFalse(cp.compare(), "No new comments expected")

    def test_multiple_adds_and_deletions(self):
        match = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )

        create_comment(comment_id=1, user_id=1, match=match)
        create_comment(comment_id=10, user_id=10, match=match)

        md = create_temporary_match_data(
            team=self.team_a,
            enemy_team=self.team_b,
            comments=[
                create_temporary_comment(comment_id=10, user_id=10),
                create_temporary_comment(comment_id=2, user_id=1),
                create_temporary_comment(comment_id=11, user_id=10),
                create_temporary_comment(comment_id=100, user_id=100),
                create_temporary_comment(comment_id=2, user_id=1),
            ],
        )
        cp = NewCommentsComparer(match=match, tmd=md)
        self.assertListEqual(cp.compare(), [11, 100], "1 new comment expected")

    def test_2_registered_teams_of_match(self):
        match1 = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_a,
            enemy_team=self.team_b,
            team_made_latest_suggestion=None,
            has_side_choice=True,
        )
        match2 = Match.objects.create(
            match_id=1,
            match_day=1,
            match_type=Match.MATCH_TYPE_LEAGUE,
            team=self.team_b,
            enemy_team=self.team_a,
            team_made_latest_suggestion=None,
            has_side_choice=False,
        )

        md = create_temporary_match_data(
            team=self.team_a,
            enemy_team=self.team_b,
            comments=[
                create_temporary_comment(comment_id=1, user_id=1),
                create_temporary_comment(comment_id=10, user_id=10),
            ],
        )
        cp = NewCommentsComparer(match=match1, tmd=md)
        self.assertListEqual(cp.compare(), [10], "1 new comment expected")

        cp.update()

        cp = NewCommentsComparer(match=match2, tmd=md)
        self.assertListEqual(cp.compare(), [1], "1 new comment expected")

        cp.update()

        cp = NewCommentsComparer(match=match1, tmd=md)
        self.assertFalse(cp.compare(), "No comment expected")
