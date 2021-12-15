import time
import datetime
import pyfiglet
import logging
import logging.config
import os
import matplotlib
import matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv
matplotlib.use('Agg')
import subprocess

load_dotenv(find_dotenv())

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
import telegram

from _model import *

from fitbit_api.access_data import *

from tinydb import TinyDB, Query
# Database in json format
db = TinyDB("db.json")
db_query = Query()


# insert user in database
def insert_user(update):
    user = get_user(update)
    if user is not None and len(db.search(db_query.id == user.id)) == 0:
        db.insert({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name})
        logging.info(f"{user.id} added to database")

# search database for user
def search_user(update):
    user = get_user(update)
    return db.search(db_query.id == user.id)[0]

#get chat id
def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id

#get user information
def get_user(update):
    user: User = None

    _from = None

    if update.message is not None:
        _from = update.message.from_user
    elif update.callback_query is not None:
        _from = update.callback_query.from_user

    if _from is not None:
        user = User()
        user.id = _from.id
        user.username = _from.username if _from.username is not None else ""
        user.first_name = _from.first_name if _from.first_name is not None else ""
        user.last_name = _from.last_name if _from.last_name is not None else ""
        user.lang = _from.language_code if _from.language_code is not None else "n/a"
    return user

def start_command_handler(update, context):
    """Send a message when the command /start is issued."""
    insert_user(update)
    user = search_user(update)
    update.message.reply_text(f"Hi {user['first_name']}! I'm a IndHealth, thanks for joining !!!!")
    update.message.reply_text("I'm here to help you with your health summary")
    update.message.reply_text("Please type /help for more information")
    update.message.reply_text("\n\nTo get started, please type app name for example for fitbit /app fitbit and for xiomi /app xiomi")


def add_app_type(update, context):
    app_name = get_text_from_message(update).split(" ")[1]
    add_typing(update, context)

    if app_name == "fitbit" or app_name == "xiomi":
        user = search_user(update)
        db.update({'app_name': app_name}, db_query.id==user['id'])
        add_text_message(update, context, f"You selected app type {app_name}")

        url = call_authorization_url()
        add_text_message(update, context, f"Please enter your access token and user id after authenticating from {url}")
    else:
        add_text_message(update, context, "Please select a valid app type")

def add_access_token(update, context):
    access_token = get_text_from_message(update).split(" ")[1]
    user = search_user(update)
    db.update({'access_token': access_token}, db_query.id==user['id'])
    add_typing(update, context)
    add_text_message(update, context, f"Your access token is stored with us")

def add_user_id(update, context):
    user_id = get_text_from_message(update).split(" ")[1]
    user = search_user(update)
    db.update({'user_id': user_id}, db_query.id==user['id'])
    add_typing(update, context)
    add_text_message(update, context, f"Your user id is stored with us")


def get_today_running_steps(update, context):
    user = search_user(update)
    today_steps = get_walking_data(user['access_token'], user['user_id'])
    add_typing(update, context)
    if not today_steps==False:
        add_text_message(update, context, f"Today you have run {today_steps} steps")
        logging.info(f"User {user['id']} has run {today_steps} steps")
    else:
        add_text_message(update, context, f"Error while getting data")
        logging.info(f"Error while getting data for user {user['id']}")

def get_7d_weight_log(update, context):
    user = search_user(update)
    weight_7d = get_weight_log(user['access_token'], user['user_id'])
    add_typing(update, context)
    if not weight_7d==False:
        weight_7d_string = ""
        for i in weight_7d:
            weight_7d_string += i + ", "
        add_text_message(update, context, f"Your body weight over the last 7 days were {weight_7d_string}")
        logging.info(f"User {user['id']} body weight over the last 7 days were {weight_7d_string}")
    else:
        add_text_message(update, context, f"Error while getting data")
        logging.info(f"Error while getting data for user {user['id']}")


def get_7d_weight_vis(update, context):
    user = search_user(update)
    weight_7d = get_weight_log(user['access_token'], user['user_id'])

    last_7d_dates = [] 
    today = datetime.date.today()
    for i in range(0,7):
        last_7d_dates.append(today - datetime.timedelta(days=i))

    sample = [1,2,3,4,5,6,7]

    add_typing(update, context)
    if not weight_7d==False:
        weight_7d_list = []
        for i in weight_7d:
            weight_7d_list.append(float(i))
        
        plt.figure(figsize=(16, 6))
        plt.plot(last_7d_dates, weight_7d_list)  # create figure & 1 axis
        plt.ylabel('Weight')
        plt.xlabel('Date')
        plt.savefig("name.png")
        ans = subprocess.check_output(['postimg', 'name.png', '--html'])
        ans = ans.decode('utf-8')
        index_start = ans.index("https://")
        index_end =  ans.index("png")
        index_end = index_end + 3
        img_link = ans[index_start:index_end]

        print("Generated and forwarded the Visualiation", img_link)       
        add_text_message(update, context, f"Here is your body weight data for the last 7 days")
        add_text_message(update, context, f"Visualization Link: {img_link}")


        # logging.info(f"User {user['id']} body weight over the last 7 days were {weight_7d_list}")
    else:
        add_text_message(update, context, f"Error while getting data")
        logging.info(f"Error while getting data for user {user['id']}")





def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Type /start")

def new_member(update, context):
    logging.info(f"new_member : {update}")
    add_typing(update, context)
    add_text_message(update, context, f"New user")

def main_handler(update, context):
    if update.message is not None:
        add_typing(update, context)
        add_text_message(update, context, f"Not a valid command")


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=telegram.ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)

def add_text_message(update, context, message):
    context.bot.send_message(chat_id=get_chat_id(update, context), text=message)

def add_suggested_actions(update, context, response):
    options = []

    for item in response.items:
        options.append(InlineKeyboardButton(item, callback_data=item))

    reply_markup = InlineKeyboardMarkup([options])

    context.bot.send_message(
        chat_id=get_chat_id(update, context),
        text=response.message,
        reply_markup=reply_markup,
    )


def get_text_from_message(update):
    return update.message.text

def get_text_from_callback(update):
    return update.callback_query.data

def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" ', update)
    logging.exception(context.error)


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # command handlers
    dp.add_handler(CommandHandler("help", help_command_handler))
    dp.add_handler(CommandHandler("start", start_command_handler))

    # app command handlers
    dp.add_handler(CommandHandler("app", add_app_type))
    dp.add_handler(CommandHandler("access_token", add_access_token))
    dp.add_handler(CommandHandler("user_id", add_user_id))

    # summary command handlers
    dp.add_handler(CommandHandler("today_steps", get_today_running_steps))

    dp.add_handler(CommandHandler("weight_logs", get_7d_weight_log))
    dp.add_handler(CommandHandler("weight_logs_graph", get_7d_weight_vis))


    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

    # suggested_actions_handler
    dp.add_handler(
        CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True)
    )

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if DefaultConfig.MODE == "webhook":

        updater.start_webhook(
            listen="0.0.0.0",
            port=int(DefaultConfig.PORT),
            url_path=DefaultConfig.TELEGRAM_TOKEN,
        )
        updater.bot.setWebhook(DefaultConfig.WEBHOOK_URL + DefaultConfig.TELEGRAM_TOKEN)

        logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    else:
        updater.start_polling()
        logging.info(f"Start polling mode")

    updater.idle()


class DefaultConfig:
    PORT = int(os.environ.get("PORT", 3978))
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=DefaultConfig.LOG_LEVEL,
        )


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("IndHealthBot")
    print(ascii_banner)   

    # Enable logging
    DefaultConfig.init_logging()

    #start server
    main()

"""
Sample Tokens

access_token = 
eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzgyWkMiLCJzdWIiOiI5UURNTlEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNjQwMTE4NjY0LCJpYXQiOjE2Mzk1NTg5OTF9.NeLoWtkiOeXOaKjsdl7_8xps89wuORliVf-EuyOZSAY
user_id = 
9QDMNQ

"""