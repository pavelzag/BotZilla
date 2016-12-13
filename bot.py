import json
import requests
import time
import urllib
import bugzilla_call
import bugs_handler
import configuration


TOKEN = configuration.get_config(parameter_type='telegram-creds',parameter_name='token')
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates, url):
    for update in updates["result"]:
        # text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(url, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            requested_user_name = bugzilla_call.extract_user(updates=updates)
            requested_status = bugzilla_call.extract_status(updates=updates)
            reply = bugzilla_call.query_builder(status=requested_status, reporter=requested_user_name)
            bugs_list = bugzilla_call.send_query(reply)
            bugs_messages = bugs_handler.bug_msg_builder(bugs_list)
            if isinstance(bugs_messages, str):
                echo_all(updates, bugs_messages)
            else:
                for bug in bugs_messages:
                    echo_all(updates,bug)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
