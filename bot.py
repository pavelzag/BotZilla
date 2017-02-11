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
import normalizer


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


def what_message(update):
    text = update.message.text.lower()
    if 'register' in text:
        return 'register'
    elif 'remove' in text:
        return 'remove'
    elif 'default_product' in text:
        return 'default_product'
    else:
        return ''


def is_mine(update):
    text = update.message.text.lower()
    if "my" in text:
        return True
    else:
        return False


def extract_field(update, type):
    text = update.message.text.lower()
    if ':' in text:
        text = text.replace(':', '')
    try:
        return text.split(type + " ", 1)[1]
    except IndexError:
        return ''


def worker(bot):
    global update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        if 'register' == what_message(update):
            message_type = 'register'
            user_name = extract_field(update, type=message_type)
            result = dbconnector.add_user(update.message.from_user.id, user_name)
            logging.debug(result)
            bot.sendMessage(chat_id=update.message.chat_id, text=result)
        elif 'remove' == what_message(update):
            message_type = 'remove'
            user_name = extract_field(update, type=message_type)
            result = dbconnector.remove_user(update.message.from_user.id, user_name)
            logging.debug(result)
            bot.sendMessage(chat_id=update.message.chat_id, text=result)
        elif 'default_product' == what_message(update):
            message_type = 'default_product'
            default_product = extract_field(update, type=message_type)
            print('Setting default product to ' + default_product)
            normalized_product = normalizer.normalize_product_new(default_product)
        else:
            if is_mine(update):
                registered_requested_user_name = dbconnector.get_user(update.message.from_user.id)
            else:
                registered_requested_user_name = ''
            logging.debug('The text that was received was: <' + str(update.message.text) + ' >')
            requested_user_name, requested_status, requested_assigned_to, requested_component, \
                requested_product = bugzilla_call.query_params(update)
            if not requested_product and requested_component:
                logging.debug('No product selected')
                bot.sendMessage(chat_id=update.message.chat_id, text='No product selected')
                update_id = update.update_id + 1
                return
            if registered_requested_user_name:
                requested_user_name = registered_requested_user_name
            bugzilla_query = bugzilla_call.query_builder(
                product=requested_product,
                component=requested_component,
                status=requested_status,
                reporter=requested_user_name,
                assigned_to=requested_assigned_to)
            bugs_list = bugzilla_call.send_query(bugzilla_query)
            bugs_messages_to_send = bugs_handler.bug_msg_builder(bugs_list)
            num_of_bugs = bugs_handler.bugs_count(bugs_messages_to_send)
            print('sending ' + str(num_of_bugs) + ' messages')
            amtstring = bugs_handler.amt_string(num_of_bugs)
            if not isinstance(bugs_messages_to_send, str):
                text_to_send = 'There' + amtstring + str(num_of_bugs) + ' ' + requested_status.lower() + ' bugs'
                logging.debug('The text that was sent was: ' + text_to_send)
                bot.sendMessage(chat_id=update.message.chat_id, text=text_to_send)
                for bug in bugs_messages_to_send:
                    logging.debug('The text that was sent was: ' + bug)
                    bot.sendMessage(chat_id=update.message.chat_id, text=bug)
            else:
                logging.debug('The text that was sent was: ' + bugs_messages_to_send)
                bot.sendMessage(chat_id=update.message.chat_id, text=bugs_messages_to_send)
        update_id = update.update_id + 1


if __name__ == '__main__':
    main()
