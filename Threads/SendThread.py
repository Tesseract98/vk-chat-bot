import datetime
import logging as log
import random
import time
from threading import Thread

from Tools.NecessaryMethods import change_db, dict_to_str, calculate
from config.constants import ID_ART


class ThreadSendMsg(Thread):
    def __init__(self, vk, parameters):
        Thread.__init__(self)
        self.__vk = vk
        self.parameters = parameters

    def run(self):
        change_per_month = self.parameters['change_per_month']
        while True:
            var = datetime.datetime.now()
            if (var + datetime.timedelta(days=1)).strftime('%d') < var.strftime('%d'):
                calculate(self.parameters['variable'], change_per_month)
                change_per_month['СКМ'] = self.parameters['variable']['СС']
                self.write_msg(ID_ART, dict_to_str(change_per_month))
                change_db(self.parameters)
            if (var - datetime.timedelta(days=1)).strftime('%d') > var.strftime('%d'):
                change_per_month['СНМ'] = self.parameters['variable']['СС']
                change_db(self.parameters)
            time.sleep(86400)

    def write_msg(self, user_id, message):
        log.info('{}: user: id{}'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), user_id))
        self.__vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(10, 1 << 32)})
