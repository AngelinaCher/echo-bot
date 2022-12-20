#!/usr/bin/env/ python3
import random
import requests
from _token import token
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

group_id = 217774482


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.session = requests.Session()

        self.vk = vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            print("Получено событие")
            try:
                self.on_event(event)
            except Exception as err:
                print(err)

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            print(event.message.text)  # получения текста сообщения
            self.api.messages.send(
                peer_id=event.message.peer_id,
                random_id=random.randint(0, 2 ** 20),
                message=event.message.text)
        else:
            print("Пока невозможно обработать событие", event.type)


if __name__ == '__main__':
    bot = Bot(group_id=group_id, token=token)
    bot.run()
