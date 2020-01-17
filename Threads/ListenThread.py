from threading import Thread
from Tools.NecessaryMethods import logger_error, write_msg, change_db
from Tools.NecessaryMethods import isAssureUser, dict_to_str


class ThreadLongpoll(Thread):
    def __init__(self, longpoll, vk_event_type, parameters):
        Thread.__init__(self)
        self.longpoll = longpoll
        self.VkEventType = vk_event_type
        self.parameters = parameters

    def run(self):
        while True:
            try:
                parameters = self.parameters
                for event in self.longpoll.listen():
                    # Если пришло новое сообщение
                    if event.type == self.VkEventType.MESSAGE_NEW:
                        # Если оно имеет метку для меня( то есть бота)
                        if event.to_me and isAssureUser(event.user_id):
                            # Сообщение от пользователя
                            request = event.text
                            # print('message from', event.user_id)
                            request_str_arr = request.split()
                            try:
                                if request.lower() == "привет":
                                    write_msg(event.user_id, dict_to_str(parameters))
                                elif len(request_str_arr) == 3 and request_str_arr[0] in parameters:
                                    if request_str_arr[1] == '+':
                                        parameters[request_str_arr[0]] += float(request_str_arr[-1])
                                    elif request_str_arr[1] == '-':
                                        parameters[request_str_arr[0]] -= float(request_str_arr[-1])
                                    parameters['БА'] = 0.01 * parameters['В']
                                    write_msg(event.user_id, dict_to_str(parameters))
                                    change_db(parameters)
                                else:
                                    write_msg(event.user_id, "Ответ непонятен...")
                            except Exception as exc:
                                write_msg(event.user_id, "!!!Неправильный символ!!!")
                                logger_error('Wrong symbol: ', exc)
            except Exception as exc:
                # print('Server error:', exc)
                logger_error('!Server error!')
