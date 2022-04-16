from tokenize import group
import telebot
from vk_hendler import find_posts
import json
import threading
import time

from vars import TG_TOKEN, group_name
TOKEN=TG_TOKEN
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["addteg"])
def get_text_messages(message):
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if message.chat.id not in data["subs"]:
            bot.send_message(message.chat.id, "Вы еще не подписаны на группу, используйте /subscribe")
            return
        if len(message.text.split()) <= 1:
            bot.send_message(message.chat.id, "Введите тэг как аргумент!")
            return
        else:
            if str(message.chat.id) in data["tags"].keys():
                if message.text.split()[1][0] == "#":
                    data["tags"][str(message.chat.id)].append(message.text.split()[1])
                else:
                    data["tags"][str(message.chat.id)].append("#" + message.text.split()[1])
            else:
                if message.text.split()[1][0] == "#":
                    data["tags"][str(message.chat.id)] = [message.text.split()[1]]
                else:
                    data["tags"][str(message.chat.id)] = ["#" + message.text.split()[1]]
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    str_tegs = ' '.join(data["tags"][str(message.chat.id)])
    bot.send_message(message.chat.id, f"Теперь вы будете видеть новости с тэгами {str_tegs}")

@bot.message_handler(commands=["removeteg"])
def get_text_messages(message):
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if message.chat.id not in data["subs"]:
            bot.send_message(message.chat.id, "Вы еще не подписаны на группу, используйте /subscribe")
            return
        if len(message.text.split()) <= 1:
            bot.send_message(message.chat.id, "Введите тэг как аргумент!")
            return
        else:
            if str(message.chat.id) in data["tags"].keys():
                if message.text.split()[1][0] == "#":
                    data["tags"][str(message.chat.id)].remove(message.text.split()[1])
                else:
                    data["tags"][str(message.chat.id)].remove("#" + message.text.split()[1])
            else:
                bot.send_message(message.chat.id, "Вы не подписаны на этот тэг!")
                return
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    str_tegs = ' '.join(data["tags"][str(message.chat.id)])
    bot.send_message(message.chat.id, f"Теперь вы будете видеть новости с тэгами {str_tegs}")

@bot.message_handler(commands=["cleartegs"])
def get_text_messages(message):
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if message.chat.id not in data["subs"]:
            bot.send_message(message.chat.id, "Вы еще не подписаны на группу, используйте /subscribe")
            return
        if str(message.chat.id) in data["tags"].keys():
            del data["tags"][str(message.chat.id)]
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    bot.send_message(message.chat.id, f"Теперь вы будете видеть все новости!")

@bot.message_handler(commands=["unsubscribe"])
def get_text_messages(message):
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if message.chat.id not in data["subs"]:
            bot.send_message(message.chat.id, "Вы не были подписаны!")
            return
        else:
            data["subs"].remove(message.chat.id)
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    bot.send_message(message.chat.id, "Вы отписаны!")

@bot.message_handler(commands=["help"])
def get_text_messages(message):
    bot.send_message(message.chat.id, """Команды:
/help - получить помощь
/subscribe - подписаться на новости
/unsubscribe - отписаться от новостей
/addteg <тэг> - добавить тэг для отслеживания
/removeteg <тэг> - убрать тэг для отслеживания
/cleartegs - очистить отслеживаемые тэги
/showtegs - посмотреть свои тэги
/info - получить данные об организаторах""")

@bot.message_handler(commands=["showtegs"])
def get_text_messages(message):
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        if message.chat.id not in data["subs"]:
            bot.send_message(message.chat.id, "Вы еще не подписаны на группу, используйте /subscribe")
            return
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)
    if str(message.chat.id) in data["tags"].keys():
        str_tegs = ' '.join(data["tags"][str(message.chat.id)])
        bot.send_message(message.chat.id, f"Вам будут видны новости с тэгами {str_tegs}")
    else:
        bot.send_message(message.chat.id, "Вы не добавляли тэгов, вам видны все новости!")

@bot.message_handler(commands=["info"])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Данные об организаторах:\nhttps://vk.com/skublik")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start" or message.text == "/subscribe":
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if message.chat.id not in data["subs"]:
                data["subs"].append(message.chat.id)
            else:
                bot.send_message(message.chat.id, "Вы уже подписаны! Используйте /unsubscribe для отписки")
                return
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file)
        bot.send_message(message.chat.id, "Вы подписаны!")

def get_posts():
    while True:
        data = find_posts(group_name)
        with open("data.json", "r", encoding="utf-8") as file:
            subs = json.load(file)["subs"]
        for id in subs:
            for item in data:
                is_here = False
                with open("data.json", "r", encoding="utf-8") as file:
                    tags = json.load(file)["tags"]
                    if str(id) in tags.keys():
                        tags_list = tags[str(id)]
                        for tag in tags_list:
                            if tag in item[0].split():
                                is_here = True
                                break
                    if str(id) not in tags.keys() or is_here:
                        if len(item[1]) == 1:
                                bot.send_photo(id, photo=item[1][0], caption=item[0])
                        elif len(item[1]) > 1:
                                bot.send_message(id, item[0])
                                for url in item[1]:
                                    bot.send_photo(id, photo=url)
                        else:
                                bot.send_message(id, item[0])
        time.sleep(5)

if __name__ == '__main__':
    thr1 = threading.Thread(target = get_posts)
    thr2 = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    thr1.start()
    try:
        thr2.start()
    except Exception:
        time.sleep(2)
        print("Reconnect...")
        thr2.start()