from vk_api.longpoll import VkLongPoll, VkEventType
from ChatBotVk.ConstantsValue import vk
from ChatBotVk.ListenThread import ThreadLongpoll
from ChatBotVk.SendThread import ThreadSendMsg
from ChatBotVk.NecessaryMethods import load_json


if __name__ == '__main__':
    parameters = load_json()
    parameters['date'] = '0'
    # Работа с сообщениями
    longpoll = VkLongPoll(vk)
    day_global = parameters['date']
    # create threads
    thread_send = ThreadSendMsg(parameters, day_global)
    thread_send.start()
    thread_msg_queue = ThreadLongpoll(longpoll, VkEventType, day_global, parameters)
    thread_msg_queue.start()
