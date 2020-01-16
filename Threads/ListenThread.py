import datetime
import re
from threading import Thread
from Tools.NecessaryMethods import logger_error, write_msg, change_with_sign
from Tools.NecessaryMethods import isAssureUser


class ThreadLongpoll(Thread):
    def __init__(self, longpoll, vk_event_type, day_global, parameters):
        Thread.__init__(self)
        self.longpoll = longpoll
        self.VkEventType = vk_event_type
        self.day_global = day_global
        self.parameters = parameters

    def run(self):
        pattern_for_aim = re.compile(r'[+\-](\d?)')
        while True:
            try:
                day = self.day_global
                flag_aim = False
                parameters = self.parameters
                for event in self.longpoll.listen():
                    # Если пришло новое сообщение
                    if event.type == self.VkEventType.MESSAGE_NEW:
                        if day != datetime.datetime.day:
                            flag_aim = True
                            day = datetime.datetime.day
                        # Если оно имеет метку для меня( то есть бота)
                        if event.to_me and isAssureUser(event.user_id):
                            # Сообщение от пользователя
                            request = event.text
                            print('message from', event.user_id)
                            regex_search = re.search(pattern_for_aim, request)
                            try:
                                if request.lower() == "привет":
                                    write_msg(event.user_id, "Bonjorno")
                                elif request.lower() == "пока":
                                    write_msg(event.user_id, "Пока :(")
                                elif regex_search:
                                    regex_search = regex_search.group()
                                    try:
                                        change_with_sign(event, regex_search[0], parameters, int(regex_search[1]))
                                    except IndexError as exc:
                                        if flag_aim:
                                            change_with_sign(event, regex_search[0], parameters=parameters)
                                            flag_aim = False
                                        else:
                                            write_msg(event.user_id, "Цель на сегодня уже была отмечена выполненной")
                                else:
                                    write_msg(event.user_id, "Ответ непонятен...")
                            except Exception as exc:
                                write_msg(event.user_id, "!!!Неправильный символ!!!")
                                logger_error('Wrong symbol: ', exc)
            except Exception as exc:
                print('Server error:', exc)
                logger_error('!Server error!')
