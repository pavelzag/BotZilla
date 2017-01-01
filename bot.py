#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
import time
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
    logging.basicConfig(filename='botzilla_log_' + str(time.strftime("%d_%m_%Y")) + '.txt', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            worker(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def worker(bot):
    global update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        logging.debug('The text that was receieved was: ' + str(update))
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
        if num_of_bugs == 1:
            amtstring = ' is '
        else:
            amtstring = ' are '
        if not isinstance(bugs_messages_to_send, str):
            logging.debug('The text that was sent was: ' + 'There' + amtstring + str(num_of_bugs) +
                                                                 ' ' + requested_status.lower() + ' bugs')
            bot.sendMessage(chat_id=update.message.chat_id, text='There' + amtstring + str(num_of_bugs) +
                                                                 ' ' + requested_status.lower() + ' bugs')
            for bug in bugs_messages_to_send:
                logging.debug('The text that was sent was: ' + bug)
                bot.sendMessage(chat_id=update.message.chat_id, text=bug)
        else:
            logging.debug('The text that was sent was: ' + bugs_messages_to_send)
            bot.sendMessage(chat_id=update.message.chat_id, text=bugs_messages_to_send)
        update_id = update.update_id + 1


if __name__ == '__main__':
    main()
