# Some code referenced from reference: https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/
from __future__ import absolute_import
from json import JSONDecodeError
import json
from typing import Iterator

import requests

from justlogswrapper import (
    Result,
    LIST,
    CHANNEL_LOGS,
    CHANNEL_DATE_LOGS,
    CHANNEL_USERNAME_DATE_LOGS,
    CHANNEL_USERNAME_LOGS,
    CHANNEL_USERNAME_RANDOM_LOGS,
    CHANNELS,
)


class JustLogApiError(Exception):
    pass


class jsLogsAdapter:
    def __init__(self, hostname: str = "https://logs.ivr.fi/", timeout: int = None):
        """
        :param hostname: https://logs.ivr.fi/ only tested hostname
        :param timeout: timeout for request using request module
        """
        self.base_url = hostname or "https://logs.ivr.fi"
        self.timeout = timeout

    def fetch_data(
        self, http_method: str, endpoint: str, params: dict = None, data: dict = None
    ) -> Result:
        """
        Makes the request and return a json object as dict
        :param endpoint: api endpoint or url
        :param params: query parameters ex: reversed, json
        """

        full_url = f"{self.base_url}{endpoint}"

        if "json" not in params:
            params["json"] = "json"

        # TRY TO PERFORM AN HTTP REQUEST,
        # print(params, full_url)
        try:
            resp_obj = requests.request(
                method=http_method,
                url=full_url,
                params=params,
                data=data,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            print(e)
            raise JustLogApiError("Request Failed") from e

        # CONVERT RESPONSE TO PYTHON OBJECT
        try:
            resp = resp_obj.json()
            # print(resp)
        except (ValueError, JSONDecodeError) as e:
            raise JustLogApiError("Bad JSON in response") from e

        # CHECK FOR STATUS CODE
        if 299 >= resp_obj.status_code >= 200:
            return Result(resp_obj.status_code, message=resp_obj.reason, data=resp)

        raise JustLogApiError(f"{resp_obj.status_code}: {resp_obj.reason}")

    def get(self, endpoint: str, params: dict = {}):
        return self.fetch_data(http_method="GET", endpoint=endpoint, params=params)


class JustLogApi:
    def __init__(self, hostname: str = "https://logs.ivr.fi/", timeout: int = 30):
        self.js_adapter = jsLogsAdapter(hostname, timeout)

    def channel_logs(self, channel: str, params: dict = {}) -> Result:
        """
        Get entire channel logs of current day

        :param channel: channel name to query
        :param params: query parameters
        """
        path = CHANNEL_LOGS.format(channel)

        return self.js_adapter.get(path, params)

    def date_channel_logs(
        self, channel: str, year: str, month: str, day: str, params: dict = {}
    ):
        """
        Get entire channel logs of given day
        """
        path = CHANNEL_DATE_LOGS.format(channel, year, month, day)

        return self.js_adapter.get(path, params)

    def user_logs(self, channel: str, username: str, params: dict = {}) -> Result:
        """
        Get user logs in channel of current month

        :param channel: channel name to query
        :param username: username to get logs of
        :param params: query parameters
        """

        if params.get("random", "False") == True:
            path = CHANNEL_USERNAME_RANDOM_LOGS.format(channel, username)
        else:
            path = CHANNEL_USERNAME_LOGS.format(channel, username)

        return self.js_adapter.get(path, params)

    def date_user_logs(
        self, channel: str, username: str, year: str, month: str, params: dict = {}
    ):
        """
        Get user logs in channel of given year month
        """
        path = CHANNEL_USERNAME_DATE_LOGS.format(channel, username, year, month)
        return self.js_adapter.get(path, params=params)

    def _list(self, channel: str = None, username: str = None):
        """
        Lists available logs of a user or channel, channel response also includes the day.
        get your userid or channel id here https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
        """
        path = LIST
        if not username:
            params = {"channel": channel}
        if username and channel:
            params = {"user": username, "channel": channel}

        return self.js_adapter.get(path, params=params)

    def channels(self):
        """
        List currently logged channels
        """
        path = CHANNELS
        return self.js_adapter.get(path)

    def get_all_channel_logs(self, channel: str) -> Iterator[dict]:
        return self.all_logs(channel=channel)

    def get_all_channel_user_logs(self, channel: str, username: str):
        return self.all_logs(channel=channel, username=username)

    def all_logs(self, channel: str, username: str = None) -> Iterator[dict]:
        logs = self._list(username=username, channel=channel).data["availableLogs"]

        if len(logs[0]) == 2:
            # gets logs per month
            for log in logs:
                result = self.date_user_logs(
                    channel,
                    username,
                    log["year"],
                    log["month"],
                )
                yield {"date": log, "result": result}
        else:
            for log in logs:
                result = self.date_channel_logs(
                    channel,
                    log["year"],
                    log["month"],
                    log["day"],
                )
                yield {"result": result, "date": log}

    # def get_channel_id(self, channel: str):
    #     """
    #     Gets channel id from /channel endpoint on host

    #     only works for channels being logged on channel
    #     """
    #     channels = self.channels().data["channels"]

    #     found = next((item for item in channels if item["name"] == channel), None)

    #     if found:
    #         return found["userID"]
    #     return None
