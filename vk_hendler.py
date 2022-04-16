import requests
import json
import datetime

from vars import VK_TOKEN

def find_posts(name):
    ret_posts = []
    TOKEN = VK_TOKEN
    params = {
        "access_token": TOKEN,
        "screen_name": name,
        "v": 5.131
    }
    id = requests.get("https://api.vk.com/method/utils.resolveScreenName", params=params).json()["response"]["object_id"]
    params = {
        "access_token": TOKEN,
        "owner_id": -id,
        "domain": "https://vk.com/fushkaland",
        "count": 5,
        "v": 5.131
    }
    posts = requests.get("https://api.vk.com/method/wall.get", params=params).json()
    for post in posts["response"]["items"][::-1]:
        post: dict = post
        if "is_pinned" not in post.keys():
            with open("data.json", "r", encoding="utf-8") as file:
                date = json.load(file)["last_time"]
            if datetime.datetime.fromtimestamp(date) < datetime.datetime.fromtimestamp(post["date"]):
                text = post["text"]
                images = []
                if "attachments" in post.keys():
                    for image in post["attachments"]:
                        if "photo" in image.keys():
                            images.append(image["photo"]["sizes"][-1]["url"])
                with open("data.json", "r", encoding="utf-8") as file:
                    all = json.load(file)
                    all["last_time"] = post["date"]
                with open("data.json", "w", encoding="utf-8") as file:
                    json.dump(all, file)
                ret_posts.append([text, images])
    return ret_posts