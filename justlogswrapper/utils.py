from justlogswrapper import TwitchChat, Tags


def build_message(message: str) -> TwitchChat:

    t = message["tags"]
    tags = Tags(
        badge_info=t["badge_info"],
        badges=t["badges"],
        client_nonce=t["client_nonce"],
        color=t["color"],
        display_name=t["display_name"],
        emotes=t["emotes"],
        first_msg=t["first_msg"],
        flags=t["flags"],
        id=t["id"],
        mod=t["mod"],
        returning_chatter=t["returning_chatter"],
        room_id=t["room_id"],
        subscriber=t["subscriber"],
        tmi_sent_ts=t["tmi_sent_ts"],
        turbo=t["turbo"],
        user_id=t["user_id"],
        user_type=t["user_type"],
    )

    chat = TwitchChat(
        text=message["text"],
        username=message["username"],
        display_name=message["display_name"],
        channel=message["channel"],
        timestamp=message["timestamp"],
        id=message["id"],
        type=message["type"],
        raw=message["raw"],
        tags=tags,
    )

    return chat
