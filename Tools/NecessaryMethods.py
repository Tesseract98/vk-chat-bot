import codecs
from json import dumps, loads

from config.constants import ID_ART, ID_SERG


def isAssureUser(user_id):
    return user_id == ID_ART or user_id == ID_SERG


def load_json():
    with codecs.open('data_base.json', 'r', encoding='utf-8', errors='replace') as file:
        temp_dict = loads(file.read())
        return temp_dict


def change_db(values: dict):
    with open('data_base.json', 'w') as file:
        file.write(dumps(values))


def dict_to_str(parameter: dict):
    var_str = ""
    for i in parameter:
        var_str += "{}:{}\n".format(i, parameter[i])
    return var_str


def calculate(variable, change_per_month):
    change_per_month['ОЧС'] = change_per_month['ЧСВ'] + change_per_month['ЧСП']
    try:
        change_per_month['ПП'] = change_per_month['ЧСВ'] * 100 / change_per_month['ОЧС']
    except ZeroDivisionError:
        change_per_month['ПП'] = 0
    change_per_month['БА'] = 0.01 * change_per_month['В']
