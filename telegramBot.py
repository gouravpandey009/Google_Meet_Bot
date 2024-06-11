from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import sqlite3
import datetime
from GoogleMeet import *


def start(update, context):
    main()
    update.message.reply_text("Starting the class")


def help(update, context):
    help_text = (
        "/start  :  Start automatic session\n"
        "/tt day s1 s2 s3 s4 s5  :  Change timetable for anyday\n"
        "/dtt  :  Drop temp tables\n"
        "/ctt  :  Create temp tables\n"
        "/timetable  :  View current day timetable\n"
    )
    update.message.reply_text(help_text)


def ttChange(update, context):
    conn = sqlite3.connect("checktt.db", check_same_thread=False)
    db = conn.cursor()
    data = update.message.text.split()

    if len(data) != 7:
        update.message.reply_text("Invalid format. Use: /tt day s1 s2 s3 s4 s5")
        return

    day, s1, s2, s3, s4, s5 = data[1:]

    print(day, s1, s2, s3, s4, s5)

    modifyTempTimeTable(day, s1, s2, s3, s4, s5)
    update.message.reply_text("Time table modified")
    subjects = printTimetable()
    print(subjects)

    day_name = datetime.datetime.now().strftime("%A")
    text = " - ".join(subjects)
    update.message.reply_text(f"{day_name}  :  {text}")
    sendDiscord("Time table modified")
    conn.close()


def dtt(update, context):
    conn = sqlite3.connect("checktt.db", check_same_thread=False)
    db = conn.cursor()
    dropTempTimeTable()
    conn.close()
    update.message.reply_text("Dropped all temp tables")


def ctt(update, context):
    conn = sqlite3.connect("checktt.db", check_same_thread=False)
    db = conn.cursor()
    createTempTimeTable()
    conn.close()
    update.message.reply_text("Created all temp tables")


def timetable(update, context):
    conn = sqlite3.connect("checktt.db", check_same_thread=False)
    db = conn.cursor()
    subjects = printTimetable()
    print(subjects)

    day_name = datetime.datetime.now().strftime("%A")
    text = " - ".join(subjects)
    update.message.reply_text(f"{day_name}  :  {text}")
    conn.close()


updater = Updater("7443149186:AAE8L-vv_jY3ygNf1LWzqbUp-rLNXFA_Ppo", use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tt", ttChange))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("dtt", dtt))
dp.add_handler(CommandHandler("ctt", ctt))
dp.add_handler(CommandHandler("timetable", timetable))

updater.start_polling()

print("Start doing your thing!")
