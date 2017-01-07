import urllib.parse
#import urllib.request import Request, urlopen
from requests import get
from config import *
import requests
import mimetypes
import random

def corgi():
    url = "https://www.googleapis.com/customsearch/v1?"
    apikey = GOOGLE_API
    cseid = CSE_ID
    url += "key=" + apikey
    url += "&cx=" +  CSE_ID
    url += "&q=" + urllib.parse.quote("Corgi Butts")
    url += "&searchType=image&num=10"
    randmonth = random.randint(1,12)
    url += "&dateRestrict=m" + str(randmonth)
#    print(url)
    response = requests.get(url)
    result = response.json()

#    print(result)
    f = open("result.txt", "w")
    f.write(str(result))
    f.close()
    randnum = random.randint(0,9)
    imglink = result['items'][randnum]['link']
#    req = Request(imglink, headers={'User-Agent': 'Mozilla/5.0'})
    mime = mimetypes.guess_extension(result['items'][0]['mime'])
    filename = "corgi" + mime
#    with open(filename, "wb") as file:
#        response = get(imglink)
#        file.write(response.content)
#    urllib.request.urlretrieve(imglink, filename)
#    s_link = result['items'][0]['link']
#    gmsg = "Search Result for <code>%s</code>:\n" % querytext
#    gmsg += "<code>%s</code>\n" % s_title
#    gmsg += "<a href='%s'>Click here</a>" % s_link
#    print(gmsg)
#    bot.sendMessage(chat_id, gmsg, reply_to_message_id=msgid, parse_mode='HTML', disable_web_page_preview='True')
    return imglink
