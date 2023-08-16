import telebot
from telebot import types
import webbrowser
import requests
from bs4 import BeautifulSoup
import datetime


class Doing:
    choose = 0


bot = telebot.TeleBot('6401310279:AAEF8hEUuSpNUFmH76Wz6eUaY009UK_uX3U')
url = 'https://livetv.sx/allupcoming/'
sports_list = ['i']
sports_matchs = []
match_li = [ ]
text_now_day = 0
had = Doing()


@bot.message_handler(commands=['help', 'main'])
def otvetstart(massage):
    bot.send_message(massage.chat.id, '<b>Привет!</b>', parse_mode='html')


@bot.message_handler(commands=['mass'])
def otvetstart(massage):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    ##print(soup)
    data = soup.find_all("a", class_="main")
    ind = 1
    markup = types.InlineKeyboardMarkup()
    callone = 'star'
    for i in data:
        if i.find("b") != None:

            sports = i.find("b").text
            sports_adress = "https://livetv.sx" + i.get("href")
            sports_list.append([sports, sports_adress])
            sender = callone + str(ind)
            btn = types.InlineKeyboardButton(sports, callback_data=sender)
            markup.add(btn)
            ind += 1
    bot.send_message(massage.chat.id, 'Выберите вид спорта',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def matchlist(callback):
    if callback.data != None:
        print(callback.data)
        print(evolcallback(callback.data), '54 stroka')
        print(evocallchislo(callback.data), '55 stroka')

        if evolcallback(callback.data) == 'link':
            print(match_li, "vot")
            if callback.data != None:
                print(callback.data)
                url_m = match_li[int(evocallchislo(callback.data))-1][1]
            print(match_li[int(evocallchislo(callback.data))])
            bot.send_message(callback.message.chat.id, url_m)


        if evolcallback(callback.data) == 'gams':
            if callback.data != None:
                print(callback.data)
                url_match = sports_matchs[int(evocallchislo(callback.data))-1][1]
            print(sports_matchs[int(evocallchislo(callback.data))])
            day = datetime.datetime.now()
            today = int(day.strftime('%d'))
            page = requests.get(url_match)
            soup = BeautifulSoup(page.content, 'lxml')
            data = soup.find_all("table", class_="lnktbj")
            
            now_table = data
            m = 1
            ##match_li = []
            murkup_match = types.InlineKeyboardMarkup()
            for i in data:
                if i.find("a", title="Открыть в новом окне") != None:
                    match_links = i.find('a', title="Открыть в новом окне").get('href')
                    match_text = 'Источник ' + str(m)
                    match_adr = "https:" + match_links
                    match_li.append([match_text, match_adr])
                    link_colback = "link" + str(m)
                    btn = types.InlineKeyboardButton(
                                    match_text, callback_data=link_colback)
                    murkup_match.add(btn)
                    m += 1
                    print(match_adr, match_text)
            if match_li == []:
                bot.send_message(callback.message.chat.id, "Нет трансляций на выбранный матч")
            else:
                bot.send_message(callback.message.chat.id, 'Выберите трансляцию',
                            reply_markup=murkup_match)
        ##print(match_li, 'vot 2')

        
        if evolcallback(callback.data) == 'star':
            had.choose = 1
            if callback.data != None:
                url_match = sports_list[int(evocallchislo(callback.data))][1]
            day = datetime.datetime.now()
            today = int(day.strftime('%d'))
            page = requests.get(url_match)
            soup = BeautifulSoup(page.content, 'lxml')
            data = soup.find_all("td")
            now_table = data[0]
            m = 1
            murkup_match = types.InlineKeyboardMarkup()
            for i in data:
                if i.find("span", class_='evdesc') != None:
                    r = 0
                    text_day_site = i.find('span', class_='evdesc').text
                    if check_int(text_day_site, today):
                        now_table = i
                        matchs = now_table.find("a", class_="live")
                        match_text = matchs.text
                        match_adr = "https://livetv.sx" + matchs.get("href")
                        if len(sports_matchs) > 0:
                            for i in range(len(sports_matchs)):
                                if sports_matchs[i][0] == match_text:
                                    r = 1
                            if r == 0:
                                sports_matchs.append([match_text, match_adr])
                                sender = 'gams' + str(m)
                                btn = types.InlineKeyboardButton(
                                    match_text, callback_data=sender)
                                murkup_match.add(btn)
                                m += 1
                        else:
                            sports_matchs.append([match_text, match_adr])
                            sender = 'gams' + str(m)
                            btn = types.InlineKeyboardButton(
                                match_text, callback_data=sender)
                            murkup_match.add(btn)
                            m += 1
                    continue
            bot.send_message(callback.message.chat.id, 'Выберите матч',
                            reply_markup=murkup_match)
        


@bot.callback_query_handler
def match_page(message):
    print(message.data)


def check_int(textik, segodnya):
    text_now_day = 0
    one_symbol = split(textik)[0]
    ret_text = ''
    if one_symbol == '1' or one_symbol == '2' or one_symbol == '3' or one_symbol == '4' or one_symbol == '5' or one_symbol == '6' or one_symbol == '7' or one_symbol == '8' or one_symbol == '9':
        ret_text = ret_text + one_symbol
        one_symbol = split(textik)[1]
        if one_symbol == '1' or one_symbol == '2' or one_symbol == '3' or one_symbol == '4' or one_symbol == '5' or one_symbol == '6' or one_symbol == '7' or one_symbol == '8' or one_symbol == '9' or one_symbol == '0':
            ret_text = ret_text + one_symbol
        text_now_day = int(ret_text)
        if text_now_day == segodnya:
            if split(textik)[2] != ' ':
                return False
            return True
    return False


def split(s):
    return [char for char in s]


def evolcallback(s):
    f = split(s)
    return f[0] + f[1] + f[2] + f[3]


def evocallchislo(s):
    f = split(s)
    i = 4
    r = f[4]
    if len(f) > 5:
        for i in range(5, len(f)):
            print(i)
            r += f[i]
    return r

@bot.message_handler(commands=['hello'])
def otvetstart(massage):
    bot.send_message(
        massage.chat.id, f'Привет, {massage.from_user.first_name}!')


@bot.message_handler(commands=['site'])
def opensite(message):
    webbrowser.open(
        'https://livetv606.me/eventinfo/144099110_lester_siti_liverpul/#_')


bot.polling(none_stop=True)
