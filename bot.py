#!/usr/bin/env/ python3
import logging
import random

try:
    import settings
except ImportError:
    exit('Do cp setting.py.default setting.py and set your settings')

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

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
    """
    Echo bot for vk.com.
    Use python 3.10
    """

    def __init__(self, group_id, token):
        """
        :param group_id: group id from a group in VK.
        :param token: secret token from the group in VK
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """ start bot """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """
        processes bot text messages and sends back
        :param event: VkBotMessageEvent object
        :return: None
        """
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
    bot = Bot(group_id=settings.GROUP_ID, token=settings.TOKEN)
    bot.run()
