from vk_api.longpoll import VkLongPoll, VkEventType
from Threads.ListenThread import ThreadLongpoll
from Threads.SendThread import ThreadSendMsg
from Tools.NecessaryMethods import load_json
from config.constants import vk

if __name__ == '__main__':
    parameters = load_json()
    # Работа с сообщениями
    longpoll = VkLongPoll(vk)
    # create threads
    thread_send = ThreadSendMsg(parameters)
    thread_send.start()
    thread_msg_queue = ThreadLongpoll(longpoll, VkEventType, parameters)
    thread_msg_queue.start()
