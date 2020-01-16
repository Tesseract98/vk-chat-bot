from threading import Thread
import time
import datetime
from Tools.NecessaryMethods import change_db, logger_error, write_msg
from Tools.ConstantsValue import digits, len_digits_lst
from config.constants import ID_ART


class ThreadSendMsg(Thread):
    def __init__(self, parameters, day_global):
        Thread.__init__(self)
        self.day_global = day_global
        self.parameters = parameters

    def run(self):
        day = self.day_global
        parameters = self.parameters
        while True:
            var = datetime.datetime.now()
            if var.strftime('%d') != day:
                day = var.strftime('%d')
                parameters['date'] = day
                change_db(parameters)
            if '11:17' <= var.strftime('%H:%M') <= '11:18':
                write_msg(ID_ART, '{0}'.format('STOP!'))
                # write_msg(ID_SERG, '{0} \general_amount {1}'.format(digits[parameters['index']], 'STOP!'))
                time.sleep(360)
            if '16:00' <= var.strftime('%H:%M') <= '16:01':
                write_msg(ID_ART, '{0} \n {1}'.format(digits[parameters['index']], 'Думай головой!!!'))
                # write_msg(ID_SERG, '{0} \general_amount {1}'.format(digits[parameters['index']], 'Думай головой!!!'))
                if parameters['index'] + 1 < len_digits_lst:
                    # parameters['index'] += 1
                    change_db(parameters)
                else:
                    logger_error('Not enough unique values, list overload')
                time.sleep(790)
            time.sleep(41)
