from justlogswrapper import *
import json


log_get = JustLogApi(timeout=1200)


def test_channel_logs():
    r = log_get.channel_logs("xqc")
    print(r.status_code)
    print(r.message)


def test_date_channel_logs():
    r = log_get.date_channel_logs("xqc", "2023", "1", "5")
    print(r.status_code)
    print(r.message)


def test_user_logs():
    r = log_get.user_logs("xqc", "leamsi_1")
    print(r.status_code)
    print(r.message)


def test_channels():
    r = log_get.channels()
    print(r.status_code)
    print(r.message)
    print(r.data)


def test_list():
    r = log_get._list(channel_id="39daph")
    print(r.status_code)
    print(r.message)
    print(r.data)


def test_channel_id():
    r = log_get.get_channel_id("xqc")
    # print(r.status_code)
    # print(r.message)
    # print(r.data)


def test_download_all_logs():
    resp = log_get.download_all_channel_logs("39daph")
    for log in resp:
        print(log)
        with open(
            log["date"]["year"]
            + "-"
            + log["date"]["month"]
            + log["date"]["day"]
            + ".txt",
            "a",
        ) as f:
            f.write(json.dumps(log["result"].data, indent=4))


def test_download_channel_user_logs():
    resp = log_get.download_all_channel_user_logs("39daph", "supertf")
    for log in resp:
        with open(log["date"]["year"] + "-" + log["date"]["month"] + ".txt", "a") as f:
            f.write(json.dumps(log["result"].data, indent=4))


# test_channel_logs()
# test_user_logs()
# test_channels()
# test_list()
# test_channel_id()
# log_yield_er()
test_download_all_logs()
# test_download_channel_user_logs()
