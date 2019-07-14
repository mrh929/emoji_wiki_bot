from requests_html import HTMLSession
from bs4 import BeautifulSoup
import telegram
from time import sleep

"""
    google functions message form:
    {
        'update_id': 11111111,
        'message': {
            'message_id': 370,
            'from': {
                'id': 123456789,
                'is_bot': False,
                'first_name': 'name',
                'username': 'name',
                 'language_code': 'zh-hans'
                 },
            'chat': {
                'id': 123456789,
                'first_name': 'name',
                'username': 'name',
                'type': 'private'
            },
            'date': 0123456789,
            'text': '?'
        }
    }


"""

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
    #post_list = Request_emoji_list("zombie")
    for each in post_list:
        bot.send_message(chat_id = chat_id, text = each)

def webhook(request):
    rdict = request.get_json()
    chat_id = rdict['message']['from']['id']
    message = rdict['message']['text']
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


    if(message == "/start"):
        bot.send_message(chat_id = chat_id, text = wel_str)
    elif(message[0] == '/'):
        Push_emoji_List(chat_id, Request_emoji(message))
    else:
        Push_emoji_List(chat_id, Request_emoji_list(message))


if (__name__ == "__main__"):
    global bot

    f = open("token.txt","r")
    token = f.read()
    bot = telegram.Bot(token)


    while(1):
        updates = bot.get_updates()
        if(updates != []):
            for update in updates:
                if(update.message.text == "/start"):
                    bot.send_message(chat_id = update.message.chat_id, text = "welcome to emoji wiki!\n\nUsage:\n[name] : search emoji\n /name : output a specific emoji")
                elif(update.message.text[0] == '/'):
                    Push_emoji_List(update.message.chat_id, Request_emoji(update.message.text))
                else:
                    Push_emoji_List(update.message.chat_id, Request_emoji_list(update.message.text))

                bot.get_updates(limit = 1, offset = update.update_id+1)
                #print(update.message.text, " ", update.message.chat_id)
        else:
            sleep(0.5)

