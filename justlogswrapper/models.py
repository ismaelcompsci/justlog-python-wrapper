from uuid import UUID
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel

"""
reference: https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/

ENDPOINTS: 
X   /channel/{channel}
X   /channel/{channel}/random  
X   /channel/{channel}/user/{username}
X   /channel/{channel}/user/{username}/random
X   /channel/{channel}/user/{username}/{year}/{month}
    # /channel/{channel}/userid/{userid}
    # /channel/{channel}/userid/{userid}/random
    # /channel/{channel}/userid/{userid}/{year}/{month}
X   /channel/{channel}/{year}/{month}/{day}  
    # /channelid/{channelid}/random
    # /channelid/{channelid}/user/{username}
    # /channelid/{channelid}/user/{username}/{year}/{month}
    # /channelid/{channelid}/user/{user}/random
    # /channelid/{channelid}/userid/{userid}
    # /channelid/{channelid}/userid/{userid}/random
    # /channelid/{channelid}/userid/{userid}/{year}/{month}
X   /list
X   /channels
"""
CHANNEL_LOGS = "/channel/{}"
CHANNEL_DATE_LOGS = "/channel/{}/{}/{}/{}"
CHANNEL_RANDOM = "/channel/{}/random"

CHANNEL_USERNAME_LOGS = "/channel/{}/user/{}"
CHANNEL_USERNAME_RANDOM_LOGS = "/channel/{}/user/{}/random"
CHANNEL_USERNAME_DATE_LOGS = "/channel/{}/user/{}/{}/{}"

LIST = "/list"
CHANNELS = "/channels"


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        """
        Result returned from jsLogs query's

        :param status_code: HTTP STATUS CODE
        :param message: Human readable result
        :param data: Python list of dictionaries
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Tags(BaseModel):
    badge_info: str
    badges: str
    client_nonce: str = None
    color: str
    display_name: str
    emotes: str
    first_msg: int
    flags: str
    id: UUID
    mod: int
    returning_chatter: int
    room_id: int
    subscriber: int
    tmi_sent_ts: str
    turbo: int
    user_id: int
    user_type: str


class TwitchChat(BaseModel):
    text: str
    username: str
    display_name: str
    channel: str
    timestamp: datetime
    id: UUID
    type: int
    raw: str
    tags: Tags
