from abc import abstractmethod

from modules.parsing.logs import BaseLog, LogSchedulingConfirmation, LogSchedulingAutoConfirmation, LogChangeTime
from modules.providers.prime_league import PrimeLeagueProvider
from utils.utils import timestamp_to_datetime


class __MatchDataMethods:

    @abstractmethod
    def get_enemy_lineup(self):
        pass

    @abstractmethod
    def get_match_closed(self):
        pass

    @abstractmethod
    def get_match_type(self):
        pass

    @abstractmethod
    def get_match_result(self):
        pass

    @abstractmethod
    def get_latest_suggestions(self):
        pass

    @abstractmethod
    def get_team_made_latest_suggestion(self):
        pass

    @abstractmethod
    def get_match_begin(self):
        pass

    @abstractmethod
    def get_latest_match_begin_log(self):
        pass

    @abstractmethod
    def get_enemy_team_id(self):
        pass

    @abstractmethod
    def get_match_day(self):
        pass

    @abstractmethod
    def get_comments(self):
        pass


class MatchDataProcessor(__MatchDataMethods, ):
    """
    Converting json data to functions and providing these.
    """

    def __init__(self, match_id: int, team_id: int, **kwargs):
        """
        :raises PrimeLeagueConnectionException, TeamWebsite404Exception
        :param match_id:
        :param team_id: team's point of view to the match. For example to determine enemy_team of the match.
        """
        self.data = PrimeLeagueProvider.get_match(match_id=match_id)
        self.team_id = team_id
        self.team_is_team_1 = self.data_match.get("team_id_1") == team_id
        self.logs = []
        self.__parse_logs()

    def __parse_logs(self):
        logs = self.data.get("logs", [])
        for i in reversed(logs):
            log = BaseLog.return_specified_log(
                timestamp=i.get("log_time"),
                user_id=i.get("user_id"),
                action=i.get("log_action"),
                details=i.get("log_details"),
            )
            if log is not None:
                self.logs.append(log)

    @property
    def data_match(self):
        return self.data.get("match", {})

    @property
    def data_stage(self):
        return self.data.get("stage", {})

    @property
    def data_group(self):
        return self.data.get("group", {})

    def get_enemy_lineup(self):
        """
        (id_, name, summoner_name, None)
        Returns: A list of player tuples. Structure of tuple: (user_id, user_name, summoner_name, None)

        """
        lineup = self.data.get("line_ups", [])
        return [(x["user_id"], x["user_name"], x["account_value"], None) for x in lineup if
                x["team_id"] != self.team_id]

    def get_match_closed(self):
        """
        possible match_status: ["upcoming", "pending", "finished"]
        """
        return self.data_match.get("match_status", None) == "finished"

    def get_match_result(self):
        """
        If match_result is set, the first number indicates the score that the team reached.
        Returns:
            `None`, if match_score_1 and match_score_2 are None else String
        """
        match_score_1 = self.data_match.get('match_score_1', None)
        match_score_2 = self.data_match.get('match_score_2', None)
        if not match_score_1 and not match_score_2:
            return None
        return f"{match_score_1}:{match_score_2}" if self.team_is_team_1 else f"{match_score_2}:{match_score_1}"

    def get_latest_suggestions(self):
        """
        :return: A list of suggestions, every suggestion is of type `datetime`. List can be empty.
        """
        suggestions = [
            self.data_match.get("match_scheduling_suggest_0"),
            self.data_match.get("match_scheduling_suggest_1"),
            self.data_match.get("match_scheduling_suggest_2"),
        ]
        return [timestamp_to_datetime(x) for x in suggestions if x]

    def get_team_made_latest_suggestion(self):
        """
        Returns: True if team made latest suggestion, else False. Returns None if no suggestion was made at all.
        """
        status = self.data_match.get("match_scheduling_status")
        if status == 0:
            return None
        status = True if status == 1 else False
        return status == self.team_is_team_1

    def get_match_begin(self):
        """
        Returns: datetime if set, else None
        """
        timestamp = self.data_match.get("match_time", None)
        if timestamp is None:
            return None
        return timestamp_to_datetime(timestamp)

    def get_match_begin_confirmed(self):
        """
        If this is 0, it means that an agreement was already made, so replying is not required anymore
        Returns: True, if match_scheduling_time is 0

        """
        return self.data_match.get("match_scheduling_time", None) == 0

    def get_latest_match_begin_log(self):
        """
        Returns: Return latest log if begin is set and a log exists, else None
        """
        for log in self.logs:
            if isinstance(log, (
                    LogSchedulingConfirmation,
                    LogSchedulingAutoConfirmation,
                    LogChangeTime,
            )):
                return log
        return None

    def get_enemy_team_id(self):
        """

        Returns: Integer or None

        """
        return self.data_match.get("team_id_2") if self.team_is_team_1 else self.data_match.get("team_id_1")

    def get_match_day(self):
        return self.data_match.get("match_playday")

    def get_match_type(self):
        return self.data_stage.get("stage_type")


    def get_comments(self):
        # TODO nicht verarbeitet
        return self.data.get("comments")
