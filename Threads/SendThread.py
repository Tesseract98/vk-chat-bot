from threading import Thread
import time
import datetime
from Tools.NecessaryMethods import change_db, logger_error, write_msg, dict_to_str, calculate
from config.constants import ID_ART, ID_SERG


class ThreadSendMsg(Thread):
    def __init__(self, parameters):
        Thread.__init__(self)
        self.parameters = parameters

    def run(self):
        change_per_month = self.parameters['change_per_month']
        while True:
            var = datetime.datetime.now()
            if (var + datetime.timedelta(days=1)).strftime('%d') < var.strftime('%d'):
                calculate(self.parameters['variable'], change_per_month)
                change_per_month['СКМ'] = self.parameters['variable']['СС']
                write_msg(ID_ART, dict_to_str(change_per_month))
                change_db(self.parameters)
            if (var - datetime.timedelta(days=1)).strftime('%d') > var.strftime('%d'):
                change_per_month['СНМ'] = self.parameters['variable']['СС']
                change_db(self.parameters)
            time.sleep(86400)
