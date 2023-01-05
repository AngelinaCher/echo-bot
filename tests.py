from unittest import TestCase
from unittest.mock import patch, Mock

import vk_api

from bot import Bot


class Test1(TestCase):
    def test_ok(self):
        count = 5
        events = [{}] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot("", "")
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_called_with({})
                assert bot.on_event.call_count == count
