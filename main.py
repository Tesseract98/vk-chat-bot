import logging as log

from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from Threads.ListenThread import ThreadLongpoll
from Threads.SendThread import ThreadSendMsg
from Tools.NecessaryMethods import load_json
from config.constants import TOKEN


def set_up_logging_properties(logging_level):
    log.basicConfig(filename='log_bot.log', level=logging_level,
                    format='%(asctime)s;%(levelname)s;%(message)s', datefmt='%Y-%m-%d %H:%M:%S')


LOGGING_LEVEL = log.INFO
set_up_logging_properties(LOGGING_LEVEL)

if __name__ == '__main__':
    vk = vk_api.VkApi(token=TOKEN)

    parameters = load_json()
    # Работа с сообщениями
    longpoll = VkLongPoll(vk)
    # create threads
    thread_send = ThreadSendMsg(vk, parameters)
    thread_send.start()
    thread_msg_queue = ThreadLongpoll(vk, longpoll, VkEventType, parameters)
    thread_msg_queue.start()

    log.info("Bot started")
