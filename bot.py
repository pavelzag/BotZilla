#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import telegram
import dbconnector
from telegram.error import NetworkError, Unauthorized
from time import sleep
import configuration
import bugzilla_call
import bugs_handler


TOKEN = configuration.get_config(parameter_type='telegram-creds', parameter_name='token')
update_id = None


def main():
    global update_id
    bot = telegram.Bot(TOKEN)
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    while True:
        try:
            worker(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def is_registration(update):
    text = update.message.text.lower()
    if 'register' in text:
        return True
    else:
        return False


def extract_user_to_register(update):
    text = update.message.text.lower()
    return text.split("register ",1)[1]


def worker(bot):
    global update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        if is_registration(update):
            print('registration')
            user_name = extract_user_to_register(update)
            result = dbconnector.add_user(update.message.from_user.id, user_name)
            logging.debug(result)
            sys.stdout.flush()
            bot.sendMessage(chat_id=update.message.chat_id, text=result)
            update_id = update.update_id + 1
        else:
            print('not registration')
            logging.debug('The text that was receieved was: <' + str(update.message.text) + ' >')
            sys.stdout.flush()
            requested_user_name, requested_status, requested_assigned_to, requested_component = \
                bugzilla_call.query_params(update)
            bugzilla_query = bugzilla_call.query_builder(
                component=requested_component,
                status=requested_status,
                reporter=requested_user_name,
                assigned_to=requested_assigned_to)
            bugs_list = bugzilla_call.send_query(bugzilla_query)
            bugs_messages_to_send = bugs_handler.bug_msg_builder(bugs_list)
            if not type(bugs_messages_to_send) == str:
                num_of_bugs = len(bugs_messages_to_send)
            else:
                num_of_bugs = 0
            print('sending ' + str(num_of_bugs) + ' messages')
            sys.stdout.flush()
            if num_of_bugs == 1:
                amtstring = ' is '
            else:
                amtstring = ' are '
            if not isinstance(bugs_messages_to_send, str):
                logging.debug('The text that was sent was: ' + 'There' + amtstring + str(num_of_bugs) +
                                                                     ' ' + requested_status.lower() + ' bugs')
                sys.stdout.flush()
                bot.sendMessage(chat_id=update.message.chat_id, text='There' + amtstring + str(num_of_bugs) +
                                                                     ' ' + requested_status.lower() + ' bugs')
                for bug in bugs_messages_to_send:
                    logging.debug('The text that was sent was: ' + bug)
                    sys.stdout.flush()
                    bot.sendMessage(chat_id=update.message.chat_id, text=bug)
            else:
                logging.debug('The text that was sent was: ' + bugs_messages_to_send)
                sys.stdout.flush()
                bot.sendMessage(chat_id=update.message.chat_id, text=bugs_messages_to_send)
            update_id = update.update_id + 1


if __name__ == '__main__':
    main()
