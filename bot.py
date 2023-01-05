#!/usr/bin/env/ python3
import logging
import random
from _token import token
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

group_id = 217774482

log = logging.getLogger('bot')


def configure_logging():
    formatter = logging.Formatter('%(asctime)s = %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename="bot.log", encoding="UTF-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info("Обратная отправка сообщения %s",
                     event.message.text)  # получения текста сообщения
            self.api.messages.send(
                peer_id=event.message.peer_id,
                random_id=random.randint(0, 2 ** 20),
                message=event.message.text)
        else:
            log.info("Пока невозможно обработать событие %s", event.type)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(group_id=group_id, token=token)
    bot.run()
