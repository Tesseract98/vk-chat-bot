import logging as log
import random
import re
from datetime import datetime
from threading import Thread

from Tools.NecessaryMethods import change_db
from Tools.NecessaryMethods import isAssureUser, dict_to_str, calculate


class ThreadLongpoll(Thread):
    def __init__(self, vk, longpoll, vk_event_type, parameters):
        Thread.__init__(self)
        self.__vk = vk
        self.longpoll = longpoll
        self.VkEventType = vk_event_type
        self.parameters = parameters

    def run(self):
        while True:
            try:
                for event in self.longpoll.listen():
                    # Если пришло новое сообщение
                    if event.type == self.VkEventType.MESSAGE_NEW:
                        # Если оно имеет метку для меня(то есть бота)
                        if event.to_me and isAssureUser(event.user_id):
                            self.process_new_message(event)
            except Exception as exc:
                log.error('!Server error!', exc_info=True)

    def process_new_message(self, event):
        variable = self.parameters['variable']
        change_per_month = self.parameters['change_per_month']

        # Сообщение от пользователя
        request = event.text
        print('message from', event.user_id)
        request_str_arr = request.split()
        try:
            var_re = re.match(r'сбросить(\d)', request.lower())
            if request.lower() == "привет":
                self.write_msg(event.user_id, dict_to_str(variable))
            elif len(request_str_arr) == 3 and (
                    request_str_arr[0] in variable or request_str_arr[0] in change_per_month):
                if request_str_arr[1] == '+':
                    if request_str_arr[0] in variable:
                        variable[request_str_arr[0]] += float(request_str_arr[-1])
                    else:
                        change_per_month[request_str_arr[0]] += float(request_str_arr[-1])
                elif request_str_arr[1] == '-':
                    if request_str_arr[0] in variable:
                        variable[request_str_arr[0]] -= float(request_str_arr[-1])
                    else:
                        change_per_month[request_str_arr[0]] -= float(request_str_arr[-1])
                calculate(variable, change_per_month)
                # write_msg(event.user_id, dict_to_str(variable))
                self.write_msg(event.user_id, "Успешно изменено")
                change_db(self.parameters)
            elif var_re:
                if var_re.group(1) == "1":
                    variable["СС"] = 0
                    variable["ОС"] = 0
                    variable["ОБ"] = 0
                elif var_re.group(1) == "2":
                    change_per_month["БА"] = 0
                    change_per_month["В"] = 0
                else:
                    self.write_msg(event.user_id, "Wrong сбросить")
                change_db(self.parameters)
                self.write_msg(event.user_id, "Сброс выполнен")
            else:
                self.write_msg(event.user_id, "Ответ непонятен...")
        except Exception as exc:
            self.write_msg(event.user_id, "!!!Неправильный символ!!!")
            log.error('!Server error!', exc_info=True)

    def write_msg(self, user_id, message):
        log.info('{}: user: id{}'.format(datetime.now().strftime("%d-%m-%Y %H:%M"), user_id))
        self.__vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(10, 1 << 32)})
