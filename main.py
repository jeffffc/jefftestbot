#coding: utf-8
import time
import random
import datetime
from ast import literal_eval

import pytz
import pymysql
import urllib
import requests
import json
import langcodes
from html.parser import HTMLParser
from config import *
import corgi
import gtrans
from telegraph import telegraph
import id
import re
import wwstats
import sfake
import make_sticker

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackQueryHandler, Job, RegexHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
import logging
from mwt import MWT

db2 = None
cursor = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MWT(timeout=60*60)


def start(bot, update):
    msg = update.message
    text = "Thank you for starting me! Use /help to get some brief help. Feel free to contact @jeffffc if you have questions."
    if msg.chat_id > 0:
        msg.reply_text(text)


def addtest(bot, update):
    msg = update.message
    if msg.reply_to_message:
        with open("testtest.txt", "a") as myfile:
            myfile.write(str(msg.reply_to_message.message_id) + "\n")
        msg.reply_text("Done.")

        
def showtest(bot, update):
    chat_id = update.message.chat.id
    with open("testtest.txt", "r") as myfile:
        data = myfile.read().splitlines()
    msgid = int(random.choice(data))
    bot.forward_message(chat_id, chat_id, msgid)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def calculatesfake(bot, update, args):
    msg = update.message
    add(msg)
    reply_to = msg.reply_to_message
    if args:
        try:
            num = int(args[0])
            answer = sfake.calc(num)
            msg.reply_markdown("```{}```".format(answer))
        except Exception:
            msg.reply_text("Not a number..")
    elif reply_to:
        try:
            num = int(reply_to.text)
            answer = sfake.calc(num)
            msg.reply_markdown("```{}```".format(answer))
        except Exception:
            msg.reply_text("Not a number..")
    else:
        msg.reply_markdown("Use `/sf <num>` or reply to a number.")


def achv(bot, update):
    msg = update.message
    add(msg)
    from_id = update.from_user.id
    try:
        msg1, msg2 = wwstats.check(from_id)
        bot.send_message(from_id, msg1, parse_mode='Markdown')
        bot.send_message(from_id, msg2, parse_mode='Markdown')
        if msg.chat_id > 0:
            msg.reply_text("I sent you your achivements in private.")
    except Exception:
        keyboard = [[InlineKeyboardButton("Start Me!", url="telegram.dog/"+BOT_USERNAME)]]
        markup = InlineKeyboardMarkup(keyboard)
        msg.reply_text("Please click 'Start Me' to receive my message!", reply_markup=markup)


def dict(bot, update, args):
    msg = update.message
    add(msg)
    bey = checkbanned(from_id)
    if bey == 1:
        return
    elif not args:
        msg.reply_markdown("Use `/dict <word>`", quote=True)
    elif len(args) > 1:
        msg.reply_markdown("Use `/dict <word>`", quote=True)
    else:
        word = args[0]
        result = dict_go(word)
        msg.reply_markdown(result, quote=True)


def dict_go(word):
    url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/{}/definitions".format(word.lower())
    randnum = random.randint(0,1)
    if randnum == 0:
        apikey = OXFORD_API_1
    else:
        apikey = OXFORD_API_2
    appid = OXFORD_ID
    try:
        r = requests.get(url, headers = {'app_id': appid, 'app_key': apikey})
        result = r.json()
        list = result['results'][0]['lexicalEntries']
        msg = "Definition(s) of word `{}`:\n".format(word)
        num = 1
        for each in list:
            msg += "{}: `{}`\n".format(num, each['entries'][0]['senses'][0]['definitions'][0])[:-1])
            num += 1
        return msg
    except Exception:
        msg = "Sorry, I cannot find the definitions of word `{}`.".format(word)
        return msg


def ud(bot, update, args):
    msg = update.message
    chat_id = msg.chat.id
    msgid = msg.message_id
    from_id = msg.from_user.id
    reply_to = msg.reply_to_message
    add(msg)
    bey = checkbanned(from_id)
    if bey == 1:
        return
    elif not args:
        msg.reply_markdown("Use `/ud <something here>`", quote=True)
    else:
        word = " ".join(args)
        result = ud_go(word)
        msg.reply_markdown(result, quote=True)


def ud_go(word):
    url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + urllib.parse.quote(word.lower(), safe='')
    apikey = UD_API
    try:
        r = requests.get(url, headers = {"X-Mashape-Key": UD_API, "Accept": "text/plain"})
        result = r.json()
        if result['result_type'] == 'no_results':
            msg = "Sorry. No results for `{}`.".format(word)
            return msg
        list = result['list']
        msg = "Query of `{}` on Urban Dictionary:\n".format(word)
        num = 1
        limit = 1
        for each in list:
            msg += "{}: `{}`\n".format(num, each['definition'])
            break  # Jono: I'd rather use list[0] than a loop then, but idk what u r doing
        return msg
    except Exception:
        msg = "Sorry, I found nothing about `{}` on Urban Dictionary.".format(word)
        return msg


def showinfo(bot, update):
    msg = update.message
    info = id.showinfo(msg)
    msg.reply_markdown(info)


def tg(bot, update):
    msg = update.message
    if msg.reply_to_message:
        url = telegraph(msg.reply_to_message)
        msg.reply_text(url)
    else:
        msg.reply_text("Reply to a message")


def repeat(bot, update):
    msg = update.message
    try:
        text = msg.text.split(" ", 1)[1]
    except IndexError:
        return
    msg.chat.send_action('typing')
#   escape_chars = '\*_`\['
#   text = re.sub(r'([%s])' % escape_chars, r'\\\1', msg)
    time.sleep(3)
    try:
        msg.reply_markdown(text, disable_web_page_preview=True)
    except BadRequest as e:
        error = str(BadRequest)
        if error.startswith("Can't parse entities:"):
            msg.reply_text(error)
        else:
            raise


def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def corgii(bot, update):
	msg = update.message
    chat_id = msg.chat.id
    msgid = msg.message_id
    add(msg)
    msg.chat.send_action('upload_photo')
    link = corgi.corgi()
    msg.reply_photo(photo=link, caption="BUTTIFUL!", quote=True)


def add(msg):
    chat_type = msg.chat.type
    chat_id = msg.chat.id
    msgid = msg.message_id
    from_id = msg.from_user.id
    reply_to = msg.reply_to_message
    from_user_name = msg.from_user.full_name
#    from_user_e = db2.escape_string(from_user_name) # Jono: Duplicate?
    from_username = msg.from_user.username
    from_user_e = db2.escape_string(from_user_name)

    try:
        if chat_type in ('group', 'supergroup'):
            group_id = chat_id
            group_name = db2.escape_string(msg.chat.title)
            checkgroupexist = "select * from `group` where groupid=%d" % group_id
            groupcount = cursor.execute(checkgroupexist)
            if groupcount == 0:
                newgroup = 1
                addgroup = "insert into `group` (`name`, `groupid`) values ('%s', %d)" % (group_name, group_id)
                cursor.execute(addgroup)
                db2.commit()
            else:
                newgroup = 0
                updategroup = "update `group` set name='%s' where groupid=%d" % (group_name, group_id)
                cursor.execute(updategroup)
                db2.commit()
    except Exception:
        print("Add/Update Group error")
    try:
        adduser = "insert into user (`name`, `telegramid`, `username`) values ('%s', %d, '%s')" % (from_user_e, from_id, from_username)
        cursor.execute(adduser)
        db2.commit()
    except Exception:
        updateuser = "update user set name='%s', username='%s' where telegramid=%d" % (from_user_e, from_username, from_id)
        cursor.execute(updateuser)
        db2.commit()

    if reply_to:
        to_user = reply_to.from_user
        to_user_name = to_user.full_name
        to_user_name_e = db2.escape_string(to_user_name)
        to_user_id = to_user.id
        to_user_username = to_user.username
        try:
            addreplyuser = "insert into user (name, username, telegramid) values ('%s', '%s', %d)" % (to_user_name_e, to_user_username, to_user_id)
            cursor.execute(addreplyuser)
            db2.commit()
        except Exception:
            editreplyuser = "update user set name='%s', username='%s' where telegramid=%d" % (to_user_name_e, to_user_username, to_user_id)
            cursor.execute(editreplyuser)
            db2.commit()


@run_async
def stickers(bot, update):
	msg = update.message
    add(msg)
    if msg.chat_id < 0:
        return
    elif not msg.reply_to_message:
        msg.reply_text("Reply to an image")
    elif not msg.reply_to_message.photo:
        msg.reply_text("The replied message contains no image.")
	else:
        photo_id = msg.reply_to_message.photo[-1].file_id
        sendmsg = "Downloading and Checking your image..."
        sent = msg.reply_text(sendmsg)
        url = bot.get_file(photo_id).file_path
        sendmsg += "\nResizing your image..."
        sent.edit_text(sendmsg)
        sendpath = make_sticker.convert(url)
        sendmsg += "\nDone!"
       	sent.edit_text(sendmsg)
        msg.chat.send_action("upload_document")
        msg.reply_document(open(sendpath, 'rb'))


def money(bot, update, groupdict):
    amount = str(groupdict['amount']).replace(",", "")
    a = groupdict['a'].upper()
    b = groupdict['b'].upper()
    url = "http://apilayer.net/api/live?access_key={}&currencies={},{}".format(CURRENCY_API_1, a, b)
    url2 = "http://apilayer.net/api/live?access_key={}&currencies={},{}".format(CURRENCY_API_2, a, b)
#    url = "http://api.fixer.io/latest"
#    url += "?base=" + a + "&symbols=" + b
    try:
        response = requests.get(url)
    except:
        response = requests.get(url2)
    result = response.json()
#    rate = result['rates'][b]
#    after = "%.3f" % (float(amount)*rate)
#    msg = "`" + amount + " " + a + "` = `" + str(after) + b + "`"
    xa = "USD{}".format(a)
    xb = "USD{}".format(b)
    aftera = result['quotes'][xa]
    afterb = result['quotes'][xb]
    after = "%.3f" % float(float(amount) * float(afterb) / float(aftera))
    with open("currency.json", 'r') as currencyjson:
        currency = json.load(currencyjson)
    afull = currency[a]
    bfull = currency[b]
    msg = "`{} {}({})` = `{} {}({})`".format(amount, afull, a, after, bfull, b)
    update.message.reply_text(msg, parse_mode='Markdown')


def t(to_lang, text):
    if to_lang != 'English':
        to_langcode = str(langcodes.find(to_lang))
        # a = trans.trans2(to_langcode, text)
        a = gtrans.trans(text, to_langcode)
    else:
        a = gtrans.trans(text)
    original_langcode = a[0]
    x = langcodes.Language.get(original_langcode)
    lang = x.language_name()
    if x.region_name() != None:
        lang += " (" + x.region_name() + ")"
    if x.script_name() != None:
        lang += " - " + x.script_name()
    translated = a[1]
    output = "Translated from: %s\n" % lang
    if to_lang != 'English':
        y = langcodes.Language.get(to_langcode)
        outputlang = y.language_name()
        if y.region_name() != None:
            lang += " (" + y.region_name() + ")"
        if y.script_name() != None:
            lang += " - " + y.script_name()
        output += "Translated to: %s\n" % outputlang
    output += "`%s`" % translated

    return output


def translatee(bot, update, args):
    chat_id = update.message.chat.id
    msgid = update.message.message_id
    from_id = update.message.from_user.id
    reply_to = update.message.reply_to_message

    add(update.message)
    bey = checkbanned(from_id)
    if bey == 1:
        return

    if not args:
        if reply_to is not None:
            tr = t('English', reply_to.text)
            bot.sendMessage(chat_id, tr, parse_mode='Markdown', reply_to_message_id=msgid)
        else:
            bot.sendMessage(chat_id, "Reply to a message to translate, or use `/t <something here>`", reply_to_message_id=msgid, parse_mode='Markdown')
    else:
        if reply_to is not None:
            to_lang = 'English'
            if len(args) == 1:
                to_lang = args[0]
                tr = t(to_lang, reply_to.text)
                bot.sendMessage(chat_id, tr, parse_mode='Markdown', reply_to_message_id=msgid)
                return
        to_lang = 'English'
        if args[0][0] == "*":
            to_lang = args[0][1:]
            args.pop(0)
        before = " ".join(args)
        after = t(to_lang, before)
        bot.sendMessage(chat_id, after, reply_to_message_id=msgid, parse_mode='Markdown')


#def google(commandonly, querytype, querytext, chat_id, msgid):
#    querytype = update.message.chat
#    if commandonly == 1:
#         bot.sendMessage(chat_id, "Please use `!gg <QUERY>` to search.", reply_to_message_id=reply_to, parse_mode='Markdown')
#         return
#    url = "https://www.googleapis.com/customsearch/v1?"
#    apikey = GOOGLE_API
#    cseid = CSE_ID
#    url += "key=" + apikey
#    url += "&cx=" +  CSE_ID
#    url += "&q=" + urllib.parse.quote(querytext)
#    if querytype == 'text':
#        print("Searching text")
#    elif querytype == 'image':
#        print("Searching image")
#        url += "&searchType=image"
#    print(url)
#    response = requests.get(url)
#    result = response.json()
#    s_title = result['items'][0]['title']
#    s_link = result['items'][0]['link']
#    gmsg = "Search Result for <code>%s</code>:\n" % querytext
#    gmsg += "<code>%s</code>\n" % s_title
#    gmsg += "<a href='%s'>Click here</a>" % s_link
#    print(gmsg)
#    bot.sendMessage(chat_id, gmsg, reply_to_message_id=msgid, parse_mode='HTML', disable_web_page_preview='True')


def pat(bot, update):
    chat_id = update.message.chat.id
    msgid = update.message.message_id
    from_id = update.message.from_user.id
    from_user_name = update.message.from_user.first_name
    if update.message.from_user.last_name is not None:
        from_user_name += " " + update.message.from_user.last_name
    chat_type = update.message.chat.type
    reply_to = update.message.reply_to_message
    if reply_to is not None:
        reply_to_id = reply_to.message_id
        to_user = reply_to.from_user
        to_user_id = to_user.id
        to_user_name = to_user.first_name
        if to_user.last_name is not None:
            to_user_name += " " + to_user.last_name

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    sql = "select count(patid) from patdb"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            patcount = row[0]
    except:
        print("ERROR at count pat desc")

    patnum = random.randint(1, patcount)

    sql2 = "select patdesc from patdb where patid = '%d'" % (patnum)
    try:
        cursor.execute(sql2)
        data = cursor.fetchall()
        for row in data:
            patdesc = row[0]
    except:
        print("ERROR")
    if reply_to is None:
        bot.sendMessage(chat_id, '* pats pats *')
    else:
        patmsg = to_user_name
        patmsg += " "
        patmsg += patdesc
        patmsg += " "
        patmsg += from_user_name
        bot.sendMessage(chat_id, patmsg, reply_to_message_id=reply_to_id)
        patcountadd=("update user set pattedby = (pattedby + 1) where telegramid=%d" % to_user_id)
        patbycountadd=("update user set patted = (patted + 1) where telegramid=%d" % from_id)
        try:
            cursor.execute(patcountadd)
            cursor.execute(patbycountadd)
            db2.commit()
        except:
            print("ERROR AT ADD PAT COUNT")


def feedback(bot, update, args):
    chat_id = update.message.chat.id
    msgid = update.message.message_id
    from_id = update.message.from_user.id
    from_name = update.message.from_user.full_name
    if update.message.from_user.last_name is not None:
        from_name += " " + update.message.from_user.last_name
    from_username =  update.message.from_user.username
    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if not args:
        update.message.reply_text("Use `/feedback <Message here>` to send feedback to me!", parse_mode='Markdown')
    else:
        msg = "FEEDBACK FROM: %s (%d)\n" % (from_name, from_id)
        msg += " ".join(args)
        bot.sendMessage(chat_id=ADMIN_ID, text=msg)
        fbmessage = db2.escape_string(" ".join(args))
        fbsql = "insert into feedback (message, name, username, telegramid) values ('%s', '%s', '%s', %d)" % (fbmessage, from_name, from_username, from_id)
        cursor.execute(fbsql)
        db2.commit()
        bot.sendMessage(chat_id, "Feedback sent!", reply_to_message_id=msgid)


def jsql(bot, update, args):
    chat_id = update.message.chat.id
    msgid = update.message.message_id
    from_id = update.message.from_user.id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if from_id != ADMIN_ID:
        bot.sendMessage(chat_id, ("You are not %s!" % ADMIN_NAME), reply_to_message_id=msgid)
        return
    try:
        enteredsql = " ".join(args)
        print(enteredsql)
        cursor.execute(enteredsql)
        db2.commit()
        result = cursor.fetchone()
        sqlmsg = "PERFORMING SQL QUERY:\n"
        colnames= [i[0] for i in cursor.description]
        sqlmsg += "`" + str(colnames) + "`\n"
        while result is not None:
           sqlmsg = sqlmsg + "`" + str(result) + "`"
           sqlmsg = sqlmsg + "\n"
           result = cursor.fetchone()
        sqlmsg = sqlmsg + "`num of affected rows: "+ str(cursor.rowcount) + "`"
        bot.sendMessage(chat_id, sqlmsg, reply_to_message_id=msgid, parse_mode="Markdown")
    except pymysql.MySQLError as e:
        code, errormsg = e.args
        sqlerror = "`MySQL ErrorCode: %s\nErrorMsg: %s`" % (code, errormsg)
        bot.sendMessage(chat_id, sqlerror, reply_to_message_id=msgid, parse_mode='Markdown')


def patstat(bot, update):
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    msgid = update.message.message_id
    from_user_name = update.message.from_user.first_name
    if update.message.from_user.last_name is not None:
        from_user_name += " " + update.message.from_user.last_name
    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    cursor2 = db2.cursor(pymysql.cursors.DictCursor)
    checkpatcount=("select patted, pattedby from user where telegramid=%d" % from_id)
    cursor2.execute(checkpatcount)
    patcount = cursor2.fetchall()
    for row in patcount:
       pats = row["patted"]
       patsby = row["pattedby"]
       patcountstr="Hello %s!\nYou have patted others `%d` times and got patted by others `%d` times." % (from_user_name, pats, patsby)
       bot.sendMessage(chat_id, patcountstr, reply_to_message_id=msgid, parse_mode="Markdown")


def myloc(bot, update, args):
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    msgid = update.message.message_id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if not args:
        bot.sendMessage(chat_id, "Please use `/myloc <location>` to set your location.", reply_to_message_id=msgid, parse_mode='Markdown')
        return
    else:
        setloc = db2.escape_string(" ".join(args))
        setlocsql = "update user set loc='%s' where telegramid=%d" % (setloc, from_id)
        cursor.execute(setlocsql)
        db2.commit()
        setmsg = "Your location is set to `%s`" % setloc
        bot.sendMessage(chat_id, setmsg, reply_to_message_id=msgid, parse_mode='Markdown')


@run_async
def now(bot, update, args):
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    msgid = update.message.message_id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return
    try:
        if args:
            loc = " ".join(args)
        elif not args:
            checkloc="select loc from user where telegramid=%d" % from_id
            cursor.execute(checkloc)
            db2.commit()
            result = cursor.fetchall()
            for row in result:
                userloc = row[0]
            db2.commit()
            if userloc == None:
                bot.sendMessage(chat_id, "Please use `/myloc <location>` to set default location or use `/now <location>`.", reply_to_message_id=msgid, parse_mode='Markdown')
                return
            else:
                loc = userloc

        '''
        url = "http://dataservice.accuweather.com/locations/v1/search"
        ran = random.randint(0,1)
        if ran == 0:
            apikey = ACCU_API_1
        else:
            apikey = ACCU_API_2
        url += "?apikey=" + apikey
        url += "&q=" +  urllib.parse.quote(loc)
        response = requests.get(url)
        result = response.json()
        locationkey = result[0]['Key']
        place = result[0]['LocalizedName'] + ", " + result[0]['AdministrativeArea']['LocalizedName'] + ", " + result[0]['Country']['LocalizedName']
        localtzname = result[0]['TimeZone']['Name']
        localtz = pytz.timezone(localtzname)
        local = str(datetime.datetime.now(localtz))
        url = "http://dataservice.accuweather.com/currentconditions/v1/"
        url += locationkey
        url += "?apikey=" + apikey
        response = requests.get(url)
        result = response.json()
        localdate = local.split(" ", 1)[0]
        localtimeandzone = local.split(" ", 1)[1]
        localtime = localtimeandzone[:8]
        localzone = localtimeandzone[-6:]
        weather = result[0]['WeatherText']
        ctemp = str(result[0]['Temperature']['Metric']['Value']) + "°" + result[0]['Temperature']['Metric']['Unit']
        ftemp = str(result[0]['Temperature']['Imperial']['Value']) + "°" + result[0]['Temperature']['Imperial']['Unit']
        '''
        url = "http://api.apixu.com/v1/current.json"
        url += "?key=" + APIXU_API
        url += "&q=" + urllib.parse.quote(loc)
        response = requests.get(url)
        result = response.json()
        place = "{}, {}, {}".format(result['location']['name'], result['location']['region'], result['location']['country'])
        ctemp = "{} °C".format(result['current']['temp_c'])
        ftemp = "{} °F".format(result['current']['temp_f'])
        weather = result['current']['condition']['text']
        localtime = str(result['location']['localtime'])
        localzone = datetime.datetime.now(pytz.timezone(result['location']['tz_id'])).strftime('%z')
        wmsg = "Currently at: %s" % place
        wmsg += "\nTemperature:`\t%s or %s`" % (ctemp, ftemp)
        wmsg += "\nDescription:`\t%s`" % weather
        wmsg += "\nLocal Time:`\t%s (UTC%s)`" % (localtime, localzone)
        bot.sendMessage(chat_id, wmsg, reply_to_message_id=msgid, parse_mode='Markdown')
    except:
        print("Looks like some nub used /now Mars")
        bot.sendMessage(chat_id, "Something wrong with your location... or something wrong with me...", reply_to_message_id=msgid)


def checkbanned(from_id):
    from_id = int(from_id)
    bansql = "select banned from user where telegramid=%d" % from_id
    cursor.execute(bansql)
    try:
        banned = cursor.fetchall()
        for row in banned:
            ban = row[0]
        db2.commit()
        return ban
    except:
        return -1


def jban(bot, update, args):
    from_id = update.message.from_user.id
    chat_id = update.message.from_user.id
    msgid = update.message.message_id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if from_id != ADMIN_ID:
        bot.sendMessage(chat_id, "You are not %s!" % ADMIN_NAME, reply_to_message_id=msgid)
        return

    if not args:
        bot.sendMessage(chat_id, "Use `/jban <id>`", reply_to_message_id=msgid, parse_mode="Markdown")
    elif args[0]:
        banid = args[0]
        print(banid)
        if banid.isdigit():
            banid = int(banid)
            if checkbanned(banid) == 1:
                print("ban already")
                update.message.reply_text("User banned already")
            elif checkbanned(banid) == -1:
                print("id wrong")
                update.message.reply_text("ID wrong")
            else:
                print("now banning")
                bannow = "update user set banned=1 where telegramid=%d" % banid
                try:
                    cursor.execute(bannow)
                    db2.commit()
                    print("banned")
                    update.message.reply_text("Ban Successful.")
                except:
                    print("fail")
                    update.message.reply_text("Failed. Try again.")
        else:
            print("not id")
            update.message.reply_text("not an id")


def junban(bot, update, args):
    from_id = update.message.from_user.id
    chat_id = update.message.from_user.id
    msgid = update.message.message_id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if from_id != ADMIN_ID:
        update.message.reply_text("You are not %s!" % ADMIN_NAME)
        return

    if not args:
        update.message.reply_text("Use `/junban <id>`", parse_mode='Markdown')
    elif args[0]:
        unbanid = args[0]
        if unbanid.isdigit():
            unbanid = int(unbanid)
            if checkbanned(unbanid) == 0:
                update.message.reply_text("User was not banned")
            elif checkbanned(unbanid) == -1:
                update.message.reply_text("ID Wrong")
            else:
                unbannow = "update user set banned=0 where telegramid=%d" % unbanid
                try:
                    cursor.execute(unbannow)
                    db2.commit()
                    update.message.reply_text("Unban Successful")
                except:
                    update.message.reply_text("Failed, try again.")
        else:
            print("not id")
            update.message.reply_text("Not ID")


def jbanlist(bot, update):
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    msgid = update.message.message_id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if from_id != ADMIN_ID:
        bot.sendMessage(chat_id, "You are not %s!" % ADMIN_NAME, reply_to_message_id=msgid)
        return

    banlistsql = "select name, username, telegramid from user where banned=1"
    cursor.execute(banlistsql)
    db2.commit()
    result=cursor.fetchone()
    sqlmsg = "Banned users:\n"
    if not result:
        sqlmsg  = "No banned users"
    while result:
        sqlmsg+="`"+str(result)+"`\n"
        result=cursor.fetchone()
    bot.sendMessage(chat_id, sqlmsg, reply_to_message_id=msgid, parse_mode='Markdown')


def nopm(bot, chat_id, from_name, msgid):
    nopmmsg = from_name + ", Please start me at PM first."
    keyboard = [[InlineKeyboardButton("Start Me!", callback_data = 'start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(chat_id, nopmmsg, reply_to_message_id=msgid, reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    queryid = query.id
    query_from_id = query.from_user.id
    query_from_first = query.from_user.first_name
    query_from_last = query.from_user.last_name
    if query_from_last is not None:
        query_from_name = query_from_first + " " + query_from_last
    else:
        query_from_name = query_from_first
    msg = query.message
    chat_id = msg.chat.id
    msgid = msg.message_id
    tomsg = query.message.reply_to_message
#    from_id = chat_data['from_id']

    if query.data == 'start':
        starturl="telegram.me/" + BOT_USERNAME + "?start=help"
        bot.answerCallbackQuery(queryid, url = starturl)

    if query.data == 'achv':
        starturl="telegram.me/" + BOT_USERNAME + "?start=achv"
        bot.answerCallbackQuery(queryid, url=starturl)


def help(bot, update):
    chat_type = update.message.chat.type
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    from_name = update.message.from_user.first_name
    msgid = update.message.message_id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    helpmsg = "Availble Commands:\n"
    helpmsg += "`/pat: [single use or by reply], pats someone`\n"
    helpmsg += "`/patstat: chat your pat history`\n"
    helpmsg += "`/myloc <location>: set your current location for using /now`\n"
    helpmsg += "`/now (<location>): return current weather for your already set location (or inputted location)`\n"
    helpmsg += "`/feedback <message>: send feedback to me!`\n"
    helpmsg += "`/t <text>: (or by reply), translate to english`"
#    print(helpmsg)
#    try:
    bot.sendMessage(from_id, helpmsg, parse_mode='Markdown')
    if chat_type != 'private':
        bot.sendMessage(chat_id, "I've sent you the help message in private.", reply_to_message_id=msgid)
#    except:
#        if chat_type != 'private':
#            nopm(bot, chat_id, from_name, msgid)


def calc_callback(bot, update, args):
    if not args:
        return
    query = "".join(args)
    try:
        answer = literal_eval(query)
        msg = "The answer is `{}`.".format(answer)
    except:
        msg = "Error occured. Try again."
    update.message.reply_text(msg, parse_mode='Markdown')


def send(bot, update, args):
    chat_type = update.message.chat.type
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    from_name = update.message.from_user.first_name
    msgid = update.message.message_id
    reply_to = update.message.reply_to_message
    if reply_to:
        to_user_id = reply_to.from_user.id

    add(update.message)

    bey = checkbanned(from_id)
    if bey == 1:
        return

    if from_id != ADMIN_ID:
        bot.sendMessage(chat_id, ("You are not %s!" % ADMIN_NAME), reply_to_message_id=msgid)
        return

    if not reply_to:
        if not args:
            bot.sendMessage(chat_id, "Use `/send <id> <message>`", reply_to_message_id=msgid, parse_mode='Markdown')
            return
        if len(args) <= 1:
            bot.sendMessage(chat_id, "Use `/send <id> <message>`", reply_to_message_id=msgid, parse_mode='Markdown')
            return
        sendperson = args[0]
        args.pop(0)
        sendmessage = " ".join(args)
#        personplusmessage = after_command

        if sendperson.isdigit():
            try:
                bot.sendMessage(sendperson, sendmessage)
                bot.sendMessage(chat_id, "Message sent", reply_to_message_id=msgid)
            except:
                bot.sendMessage(chat_id, "Send Failed", reply_to_message_id=msgid)
        elif sendperson[1:].isdigit():
                bot.sendMessage(sendperson, sendmessage)
                bot.sendMessage(chat_id, "Message sent")
        else:
            sendperson = sendperson[1:]
            personsql="select telegramid from user where username='%s'" % sendperson
            cursor.execute(personsql)
            db2.commit()
            result = cursor.fetchall()
            for row in result:
                item = row[0]
            db2.commit()
            try:
                bot.sendMessage(item, sendmessage)
                bot.sendMessage(chat_id, "Message sent", reply_to_message_id=msgid)
            except:
                bot.sendMessage(chat_id, "Send Failed", reply_to_message_id=msgid)
    else:
        sendperson = to_user_id
        sendmessage = " ".join(args)
        if reply_to.forward_from is not None:
            sendperson = reply_to.forward_from.id
        try:
            bot.sendMessage(sendperson, sendmessage)
            bot.sendMessage(chat_id, "Message sent", reply_to_message_id=msgid)
        except:
            bot.sendMessage(chat_id, "Send Failed", reply_to_message_id=msgid)


@run_async
def search_id_callback(bot, update, args):
    if not args:
        update.message.reply_text("Please provide an id or username.")
        return
    inputtext = args[0]
    sent = update.message.reply_text("Please wait...")
    try:
        inputtext = int(inputtext)
    except:
        pass
    r = requests.get(
        "http://api.jpwr.ga/bot226774066:AAFPoonQPpn8QmtR99_TPUS-mqwmWdAuJAA/getchat?chat_id={}".format(
            inputtext)).json()
    msg = ""
    msg += "ID: `{}`\n".format(r['result']['id'])
    if "first_name" in r['result']:
        msg += "First Name: {}\n".format(escape_markdown(r['result']['first_name']))
    if "last_name" in r['result']:
        msg += "Last Name: {}\n".format(escape_markdown(r['result']['last_name']))
    if 'username' in r['result']:
        msg += "Username: @{}\n".format(escape_markdown(r['result']['username']))
    if "title" in r['result']:
        msg += "Title: *{}*\n".format(escape_markdown(r['result']['title']))
    if "about" in r['result']:
        msg += "About: _{}_".format(escape_markdown(r['result']['about']))
    sent.edit_text(msg, parse_mode='Markdown')


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\[\]'
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def save_message(bot, update):
    reply_to_msg = update.message.reply_to_message
    try:
        reply_to_msg.forward(update.message.from_user.id)
    except:
        update.message.reply_text("You have not started me in private...")


def main():
    global db2, cursor
    db2 = pymysql.connect(MYSQL_SERVER, MYSQL_USERNAME, MYSQL_PW, MYSQL_DBNAME, charset='utf8', autocommit=True)
    cursor = db2.cursor()

    cursor.execute("set names utf8mb4")
    cursor.execute("set character set utf8mb4")
    cursor.execute("set character_set_connection=utf8mb4")

    cursor.execute(SQL_CREATE_TABLE_1)
    cursor.execute(SQL_CREATE_TABLE_2)
    cursor.execute(SQL_CREATE_TABLE_3)
    cursor.execute(SQL_CREATE_TABLE_4)
    db2.commit()


    try:
        cursor.execute(SQL_DEFAULT_PAT)
        db2.commit()
#        db2.close()
    except:
        print("Default Pat String exists already.")

    updater = Updater(BOT_TOKEN)

    job = updater.job_queue
    nexthour = datetime.datetime.now().replace(microsecond=0).replace(second=0).replace(minute=0) + datetime.timedelta(hours=1)
#    job.run_repeating(amaat, datetime.timedelta(hours=1), first=nexthour)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("jbanlist", jbanlist))
    dp.add_handler(CommandHandler("junban", junban, pass_args=True))
    dp.add_handler(CommandHandler("jban", jban, pass_args=True))
    dp.add_handler(CommandHandler("now", now, pass_args=True))
    dp.add_handler(CommandHandler("jsql", jsql, pass_args=True))
    dp.add_handler(CommandHandler("patstat", patstat))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("feedback", feedback, pass_args=True))
    dp.add_handler(CommandHandler("t", translatee, pass_args=True))
    dp.add_handler(CommandHandler("myloc", myloc, pass_args=True))
#    dp.add_handler(CommandHandler("pat", pat))
    dp.add_handler(CommandHandler("pat", pat))
    dp.add_handler(CommandHandler("send", send, pass_args=True))
    dp.add_handler(CommandHandler("corgi", corgii))
    dp.add_handler(CommandHandler("re", repeat))
    dp.add_handler(CommandHandler("tg", tg))
    # dp.add_handler(CommandHandler("z", showinfo))
    dp.add_handler(CommandHandler("dict", dict, pass_args=True))
    dp.add_handler(CommandHandler("achv", achv))
    dp.add_handler(CommandHandler("ud", ud, pass_args=True))
    dp.add_handler(CommandHandler("sf", calculatesfake, pass_args=True))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addtest", addtest))
    dp.add_handler(CommandHandler("showtest", showtest))
    dp.add_handler(CommandHandler("sticker", stickers))
    dp.add_handler(CommandHandler("calc", calc_callback, pass_args=True))
    dp.add_handler(CommandHandler("search", search_id_callback, pass_args=True))

    dp.add_handler(CommandHandler("s", save_message, filters=(Filters.reply & Filters.group)))

    money_regex="^[\s]*(?P<amount>[0-9,.]+)[\s]*(?P<a>[A-Za-z]+)[\s]+[tT][oO][\s]+(?P<b>[A-Za-z]+)$"
    dp.add_handler(RegexHandler(money_regex, money, pass_groupdict=True))

    dp.add_handler(CallbackQueryHandler(button))

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    print("Bot has started... Polling for messages...")


if __name__ == '__main__':
    main()
