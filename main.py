import time
import random
import datetime
import pytz
import telepot
import telepot.namedtuple
import random
import _mysql
import pymysql
import urllib
import requests
import json

from config import *

def nopm(chat_id, from_user, msgid):
    nopmmsg = from_user + ", Please start me at PM first."
    bot.sendMessage(chat_id, nopmmsg, reply_to_message_id=msgid)

def handle(msg):
    msg2 = telepot.namedtuple.Message(**msg)
    chat_id = msg['chat']['id']
    chat_id2 = msg2.chat.id
    chat_type = msg['chat']['type']
    command2 = msg2.text
    if command2 == None:
        return
    else:
        command = command2
    from_user = msg['from']['first_name']
    from_user2 = msg2.from_.first_name
    from_id = msg['from']['id']
    from_id2 = msg2.from_.id
    from_username2 = msg2.from_.username
    if from_username2 == None:
        from_username = -1
    else:
        from_username = from_username2
    msgid = msg['message_id']
    msgid2 = msg2.message_id
    reply_to = msgid
    reply_to2 = msg2.message_id
    patcount = 0
    patdesc = "is patted defaultly by"
    to_user = 'None'

    if command[:1] == '/':
        using = '/'
    elif command[:1] == '!':
        using = '!'
    else:
        return

    db2 = pymysql.connect(MYSQL_SERVER, MYSQL_USERNAME, MYSQL_PW, MYSQL_DBNAME, charset='utf8')
    cursor = db2.cursor()
    cursor2 = db2.cursor()
    cursor.execute("set names utf8mb4")
    cursor.execute("set character set utf8mb4")
    cursor.execute("set character_set_connection=utf8mb4")

#    try:
#        started = bot.getChat(from_id)
#        if started:
#            print(started)
#            print("started")
#        else:
#            print("not started")
#    except:
#        print("error")

    try:
        if chat_type == 'group' or chat_type == 'supergroup':
            group_id = chat_id
            group_name = msg['chat']['title']
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
    except:
        print("Add/Update Group error")
    try:
        usersql = "select * from user where telegramid=%d" % from_id
        userexist = cursor.execute(usersql)
        if userexist == 0:
            newuser = 1
            adduser =  "insert into user (`name`,  `username`, `telegramid`, `patted`, `pattedby`) values ('%s', '%s', %d, 0, 0)" % (from_user, from_username, from_id)
            cursor.execute(adduser)
            db2.commit()
        else:
            newuser = 0
            updateuser = "update user set name='%s', username='%s' where telegramid=%d" % (from_user, from_username, from_id)
            cursor.execute(updateuser)
            db2.commit()
    except:
        print("ERROR at add/update user")

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

    if msg2.reply_to_message == None:
        reply_to = msgid
    else:
        reply_to = msg['reply_to_message']['message_id']
        reply_to2 = msg2.reply_to_message
        to_user = msg['reply_to_message']['from']['first_name']
        to_user_id = msg['reply_to_message']['from']['id']
        to_user_username = msg['reply_to_message']['from']['username']
        try:
            checkreplyuserexist = "select * from user where telegramid=%d" % to_user_id
            rowcount=cursor.execute(checkreplyuserexist)
            if rowcount == 0:
                addreplyuser="insert into user (name, username, telegramid) values ('%s', '%s', %d)" % (to_user, to_user_username, to_user_id)
                cursor.execute(addreplyuser)
                db2.commit()
            else:
                editreplyuser="update user set name='%s', username='%s' where telegramid=%d" % (to_user, to_user_username, to_user_id)
                cursor.execute(editreplyuser)
                db2.commit()
        except:
            print("ERROR at add/edit reply user")

    if command[:1] == '/' or command[:1] == '!':
        multiple_args = command.split(' ')
        if len(multiple_args) > 1:
            commandonly = 0
            splitstring = command.split(' ', 1)
            after_command = splitstring[1]
            real_command = splitstring[0][1:]
            if real_command[-13:] == BOT_USERNAME:
               real_command = real_command.split('@', 1)
               real_command = real_command[0]
               real_command = real_command.lower()
        else:
            commandonly = 1
            real_command = command[1:]
            real_command = real_command.split('@', 1)
            real_command = real_command[0]
            real_command = real_command.lower()
    else:
        real_command = 'NO'

    if real_command == 'NO':
        print('NOT COMMAND')
    else:
        if real_command == 'pat':
            patmsg = to_user
            patmsg += " "
            patmsg += patdesc
            patmsg += " "
            patmsg += from_user
            if to_user == 'None':
                bot.sendMessage(chat_id, '* pats pats *')
            else:
                bot.sendMessage(chat_id, patmsg, reply_to_message_id=reply_to)
                patcountadd=("update user set pattedby = (pattedby + 1) where telegramid=%d" % to_user_id)
                patbycountadd=("update user set patted = (patted + 1) where telegramid=%d" % from_id)
                try:
                    cursor.execute(patcountadd)
                    cursor.execute(patbycountadd)
                    db2.commit()
                except:
                    print("ERROR AT ADD PAT COUNT")
        elif real_command == 'myloc':
            if commandonly == 1:
                bot.sendMessage(chat_id, "Please use `/myloc <location>` to set your location.", reply_to_message_id=reply_to, parse_mode='Markdown')
                return
            setloc = after_command
            setlocsql = "update user set loc='%s' where telegramid=%d" % (setloc, from_id)
            cursor.execute(setlocsql)
            db2.commit()
            setmsg = "Your location is set to `%s`" % setloc
            bot.sendMessage(chat_id, setmsg, reply_to_message_id=reply_to, parse_mode='Markdown')
        elif real_command == 'send':
            if from_id != ADMIN_ID:
                bot.sendMessage(chat_id, ("You are not %s!" % ADMIN_NAME), reply_to_message_id=reply_to)
                return
            if msg2.reply_to_message == None:
                if commandonly == 1:
                    bot.sendMessage(chat_id, "Use `!send <id> <message>`", reply_to_message_id=reply_to, parse_mode='Markdown')
                    return
                personplusmessage = after_command
                if len(personplusmessage.split(" ")) <= 1:
                    bot.sendMessage(chat_id, "Use `!send <id> <message>`", reply_to_message_id=reply_to, parse_mode='Markdown')
                    return
                splitpersonplusmessage = after_command.split(" ", 1)
                sendperson = splitpersonplusmessage[0]
                sendmessage = splitpersonplusmessage[1]
                if sendperson.isdigit():
                    try:
                        bot.sendMessage(sendperson, sendmessage)
                        bot.sendMessage(chat_id, "Message sent", reply_to_message_id=msgid)
                    except:
                        bot.sendMessage(chat_id, "Send Failed", reply_to_message_id=msgid)
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
                 sendmessage = after_command
                 if reply_to2.forward_from != None:
                     sendperson = reply_to2.forward_from.id
                 try:
                     bot.sendMessage(sendperson, sendmessage)
                     bot.sendMessage(chat_id, "Message sent", reply_to_message_id=msgid)
                 except:
                     bot.sendMessage(chat_id, "Send Failed", reply_to_message_id=msgid)
        elif real_command == 'feedback':
            fbmessage = after_command
            fbsql = "insert into feedback (message, name, username, telegramid) values ('%s', '%s', '%s', %d)" % (fbmessage, from_user, from_username, from_id)
            cursor.execute(fbsql)
            db2.commit()
            bot.sendMessage(chat_id, "Feedback sent!", reply_to_message_id=reply_to)
        elif real_command == 'help':
            helpmsg = "Availble Commands:\n"
            helpmsg += "`/pat: [single use or by reply], pats someone`\n"
            helpmsg += "`/patstat: chat your pat history`\n"
            helpmsg += "`/myloc <location>: set your current location for using /now`\n"
            helpmsg += "`/now (<location>): return current weather for your already set location (or inputted location)`\n"
            helpmsg += "`/feedback <message>: send feedback to me!`"
            try:
                bot.sendMessage(from_id, helpmsg, parse_mode='Markdown')
                if chat_type != 'private':
                    bot.sendMessage(chat_id, "I've sent you the help message in private.", reply_to_message_id=reply_to)
            except:
                if chat_type != 'private':
#                    bot.sendMessage(chat_id, "Please start me in PM first.", reply_to_message_id=msgid)
                    nopm(chat_id, from_user, msgid)
        elif real_command == 'patstat':
            cursor2 = db2.cursor(pymysql.cursors.DictCursor)
            checkpatcount=("select patted, pattedby from user where telegramid=%d" % from_id)
            cursor2.execute(checkpatcount)
            patcount = cursor2.fetchall()
            for row in patcount:
               pats = row["patted"]
               patsby = row["pattedby"]
               patcountstr="Hello %s!\nYou have patted others `%d` times and got patted by others `%d` times." % (from_user, pats, patsby)
               bot.sendMessage(chat_id, patcountstr, reply_to_message_id=reply_to, parse_mode="Markdown")
        elif real_command == 'sql':
            if from_id != ADMIN_ID:
                bot.sendMessage(chat_id, ("You are not %s!" % ADMIN_NAME), reply_to_message_id=reply_to)
                return
            try:
                enteredsql=after_command
                cursor.execute(enteredsql)
                db2.commit()
                result = cursor.fetchone()
                sqlmsg = "PERFORMING SQL QUERY:\n"
                while result is not None:
                   sqlmsg = sqlmsg + "`" + str(result) + "`"
                   sqlmsg = sqlmsg + "\n"
                   result = cursor.fetchone()
                sqlmsg = sqlmsg + "`num of affected rows: "+ str(cursor.rowcount) + "`"
                bot.sendMessage(chat_id, sqlmsg, reply_to_message_id=reply_to, parse_mode="Markdown")
            except pymysql.MySQLError as e:
                code, errormsg = e.args
                sqlerror = "`MySQL ErrorCode: %s\nErrorMsg: %s`" % (code, errormsg)
                bot.sendMessage(chat_id, sqlerror, reply_to_message_id=reply_to, parse_mode='Markdown')
        elif real_command == 'now':
            try:
                 if commandonly == 1:
                     checkloc="select loc from user where telegramid=%d" % from_id
                     cursor.execute(checkloc)
                     db2.commit()
                     result = cursor.fetchall()
                     for row in result:
                         userloc = row[0]
                     db2.commit()
                     if userloc == None:
                         bot.sendMessage(chat_id, "Please use `!myloc <location>` to set default location or use `!now <location>`.", reply_to_message_id=reply_to, parse_mode='Markdown')
                         return
                     else:
                         after_command = userloc
                 url = "http://dataservice.accuweather.com/locations/v1/search"
                 ran = random.randint(0,1)
                 if ran == 0:
                     apikey = ACCU_API_1
                 else:
                     apikey = ACCU_API_2
                 url += "?apikey=" + apikey
                 url += "&q=" +  after_command
                 url = url.replace(" ", "%20")
                 url = url.replace(",", "%2C")
                 response = requests.get(url)
                 result = response.json()
                 locationkey = result[0]['Key']
                 place = result[0]['LocalizedName'] + ", " + result[0]['AdministrativeArea']['LocalizedName'] + ", " + result[0]['Country']['LocalizedName']
                 url = "http://dataservice.accuweather.com/currentconditions/v1/"
                 url += locationkey
                 url += "?apikey=" + apikey
                 response = requests.get(url)
                 result = response.json()
                 weather = result[0]['WeatherText']
                 ctemp = str(result[0]['Temperature']['Metric']['Value']) + "°" + result[0]['Temperature']['Metric']['Unit']
                 ftemp = str(result[0]['Temperature']['Imperial']['Value']) + "°" + result[0]['Temperature']['Imperial']['Unit']
                 wmsg = "Current weather for: %s" % place
                 wmsg += "\nTemperature:\t%s or %s" % (ctemp, ftemp)
                 wmsg += "\nDescription:\t%s" % weather
                 bot.sendMessage(chat_id, wmsg, reply_to_message_id=reply_to)
            except:
                print("LOL")
                bot.sendMessage(chat_id, "Something wrong with your location...", reply_to_message_id=reply_to)
    db2.close()
    printmsg = "New Command '%s%s' from '%s (%d)'" % (using, real_command, from_user, from_id)
    printmsg += "\n"
    printmsg += "Chat type: '%s'\t" % chat_type
    if chat_type != 'private':
        if newgroup == 1:
            printmsg += 'NEW '
        printmsg += "Group: %s (%d)" % (group_name, group_id)
    printmsg += "\n"
    if commandonly == 0:
        printmsg += "After Command:\t%s\n" % after_command
    tz = pytz.timezone(ADMIN_TIMEZONE)
    timenow = str(datetime.datetime.now(tz))
    printmsg = timenow + "\n" + printmsg
    print(printmsg)
    with open("log.txt", "a") as logging:
        logging.write(printmsg + "\n")

bot = telepot.Bot(BOT_TOKEN)
db2 = pymysql.connect(MYSQL_SERVER, MYSQL_USERNAME, MYSQL_PW, MYSQL_DBNAME, charset='utf8')
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
    db2.close()
except:
    print("Default Pat String exists already.")
bot.message_loop(handle)
print('I am listening ...')

while 1:
    time.sleep(10)
