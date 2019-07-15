from requests_html import HTMLSession
from bs4 import BeautifulSoup
import telegram


def __get_mid_text(text, left_text, right_text, start=0):#获取中间文本
    left = text.find(left_text, start)
    if left == -1:
        return ('', -1)
    left += len(left_text)
    right = text.find(right_text, left)
    if right == -1:
        return ('', -1)
    return (text[left:right], right)

def Request_emoji_list(emoji_text):
    session = HTMLSession()
    url = "https://emojipedia.org/search/?q=" + emoji_text
    response = session.get(url)
    #response.html.render()#渲染


    soup = BeautifulSoup(response.html.html, 'lxml')
    all_emoji = soup.find(name = "ol")
    #print(all_emoji)

    ret = []
    for each_emoji in all_emoji.find_all(name = 'li'):
        div_h2 = each_emoji.find('a') #emoji名字
        #div_p = each_emoji.find('p') #emoji描述

        short_cut = str(div_h2['href']).replace('-','_')
        short_cut = short_cut[:-1]
        ret.append("{}\n{}".format(div_h2.text, short_cut))
        #div_p.text暂时不用
    return ret

def Request_emoji(emoji_text):
    emoji_text = emoji_text.replace('_','-') + '/'

    session = HTMLSession()
    url = "https://emojipedia.org" + emoji_text
    response = session.get(url)

    emoji, status = __get_mid_text(response.html.html,"value=\"","\" readonly")
    if(status == -1):
        return ["emoji not found."]
    return [emoji]


def Push_emoji_List(chat_id, post_list):
    for each in post_list:
        bot.send_message(chat_id = chat_id, text = each)

def webhook(request):
    rdict = request.get_json()

    try:
        chat_id = rdict['message']['from']['id']
        message = rdict['message']['text']
    except KeyError:
        return

    global bot
    # type your token
    bot = telegram.Bot("")
    wel_str ="""welcome to emoji wiki!

All resources are from
	https://emojipedia.org/

Usage:
[name]  : search emoji about [name]
/[name] : output an emoji named [name]

"""

    try:
        if(message == "/start"):
            bot.send_message(chat_id = chat_id, text = wel_str)
        elif(message[0] == '/'):
            Push_emoji_List(chat_id, Request_emoji(message))
        else:
            Push_emoji_List(chat_id, Request_emoji_list(message))
        return
    except:
        bot.send_message(chat_id = chat_id, text = "An error occurred!")
        return