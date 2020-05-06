import requests
import json
import time
from discord_webhook import DiscordWebhook

requestURL = "https://scrape.pastebin.com/api_scraping.php?limit=100"
webhookURL = ""


def get_recent_pastes():
    response = requests.get(requestURL)

    if response.status_code is not 200:
        print(f"Failed to get recent pastes, status code: {response.status_code}")
        return []

    return json.loads(response.content.decode("UTF-8"))


def make_link(key):
    return f"https://pastebin.com/{key}\n"


last_hundred_pastes = []

while True:
    recent_pastes = get_recent_pastes()

    if len(recent_pastes) == 0:
        time.sleep(60)
        continue

    to_update = []
    for element in recent_pastes:
        key = element["key"]

        if key not in last_hundred_pastes:
            if len(last_hundred_pastes) == 100:
                last_hundred_pastes.pop(0)

            last_hundred_pastes.append(key)
            to_update.append(key)

    if len(to_update) == 0:
        continue

    webhookContent = ""

    for key in to_update:
        webhookContent += make_link(key)

    webhook = DiscordWebhook(url=webhookURL, content=webhookContent)
    webhook.execute()
    time.sleep(60)
