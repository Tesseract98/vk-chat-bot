import datetime
import logging
import random
from json import dumps, loads
from ChatBotVk.ConstantsValue import digits, len_digits_lst, vk
from ChatBotVk.config.constants import ID_SERG, ID_ART

logging.basicConfig(filename='log_bot.log', level=logging.INFO)


def isAssureUser(user_id):
    # return user_id == ID_ART or user_id == ID_SERG
    return user_id == ID_ART


def load_json():
    with open('data_base.json', 'r') as file:
        temp_dict = loads(file.read())
        return temp_dict


def change_db(values: dict):
    with open('data_base.json', 'w') as file:
        file.write(dumps(values))


def logger_error(err: str, exc=None):
    full_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    if exc:
        logging.error('{}: {}, {}'.format(full_date, err, exc))
    else:
        logging.error('{}: {}'.format(full_date, err))


def write_msg(user_id, message):
    logging.info('{}: user: id{}'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), user_id))
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(10, 12132132)})


def change_with_sign(event, sign: str, parameters, digit=0):
    if sign == '+':
        var = parameters['index'] + digit
        if var < len_digits_lst:
            parameters['index'] = var
            if digit > 0:
                write_msg(event.user_id, "Текущее значение = {}".format(digits[var]))
            elif digit == 0:
                write_msg(event.user_id, "План {} выполнен.\n Кто красавчик, ты красавчик :)".format(digits[var]))
                parameters['index'] += 1
            change_db(parameters)
        else:
            write_msg(event.user_id,
                      "!Выход за пределы масива! Текущее значение = {}".format(digits[parameters['index']]))
    elif sign == '-':
        var = parameters['index'] - digit
        if var >= 0:
            if digit > 0:
                parameters['index'] = var
                write_msg(event.user_id, "Текущее значение = {}".format(digits[var]))
            elif digit == 0:
                write_msg(event.user_id, "План {} не выполнен.\n Эх, ну ничего, завтра получится :(".format(digits[var]))
            change_db(parameters)
        else:
            write_msg(event.user_id,
                      "!Выход за пределы массива! Текущее значение = {}".format(digits[parameters['index']]))
    else:
        logger_error('Wrong condition')
