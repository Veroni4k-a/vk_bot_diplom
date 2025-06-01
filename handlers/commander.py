from handlers.command_enum import Command, Message
import re


class Commander:
    def __init__(self):
        # Для запоминания последней команды
        self.last_command = None
        # Для запоминания ответов пользователя
        self.last_ans = None

    def input(self, msg):

        if re.search('начать', msg):
            self.last_command = Command.start
            return Message.start_msg.value

        if self.last_command in [Command.info, Command.water, Command.light, Command.map, Command.traffic_movement]:
            if re.search('отключение воды', msg):
                self.last_command = Command.water
                return Message.water_msg.value
            elif re.search('отключение электричества', msg):
                self.last_command = Command.light
                return Message.light_msg.value
            elif re.search('карта уборки города', msg):
                self.last_command = Command.map
                return Message.map_msg.value
            elif re.search('транспорт', msg):
                self.last_command = Command.traffic_movement
                return Message.traffic_movement_msg.value

            elif re.search('0|назад', msg):
                self.last_command = None
                return Message.start_msg.value

            else:
                self.last_command = Command.info
                return Message.wrong_msg.value



        if self.last_command in [Command.dog,Command.zayavka, Command.adress,Command.geo]:
            if re.search('написать адрес вручную', msg):
                self.last_command = Command.adress
                return Message.adress_msg.value

            elif re.search('отправить геолокацию', msg):
                self.last_command = Command.geo
                return Message.geo_msg.value

            elif re.search('0|назад', msg):
                self.last_command = None
                return Message.start_msg.value

            else:
                self.last_command = Command.zayavka
                return Message.wrong_msg.value

        if self.last_command in [Command.zayavka, Command.dog, Command.tree, Command.rubsh, Command.traffic_movement_back, Command.light_problem, Command.traffic]:
            if re.search('отлов собак', msg):
                self.last_command = Command.dog
                return Message.dog_msg.value
            elif re.search('упало дерево', msg):
                self.last_command = Command.tree
                return Message.tree_msg.value
            elif re.search('уборка мусора', msg):
                self.last_command = Command.rubsh
                return Message.rubsh_msg.value
            elif re.search('брошенный транспорт', msg):
                self.last_command = Command.traffic_movement_back
                return Message.traffic_movement_back_msg.value
            elif re.search('проблемы с освещением', msg):
                self.last_command = Command.light_problem
                return Message.light_problem_msg.value
            elif re.search('поломка светофора', msg):
                self.last_command = Command.traffic
                return Message.traffic_msg.value

            elif re.search('0|назад', msg):
                self.last_command = None
                return Message.start_msg.value

            else:
                self.last_command = Command.zayavka
                return Message.wrong_msg.value

            # Это  команды для первой клавиатуры
        if re.search('1|получить информацию', msg)and self.last_command != Command.info:
            self.last_command = Command.info
            return Message.info_msg.value

        elif re.search('2|подать заявку', msg)and self.last_command != Command.info:
            self.last_command = Command.zayavka
            return Message.zayavka_msg.value




        # elif re.search('0|назад', msg):
        #     self.last_command = None
        #     return Message.start_msg.value
        if self.last_command == Command.info:
            self.last_command = Command.zayavka
            return Message.thx_msg.value

        # else:
        #     self.last_command = Command.info
        #     return Message.wrong_msg.value

        # Обработка команд информационных


        #Обработка команды "назад" для любого состояния
        # if re.search('0|назад', msg):
        #     self.last_command = None
        #     return Message.start_msg.value



        # if self.last_command in [Command.emergency_situations, Command.water, Command.light, Command.traffic,Command.tree,Command.info, Command.zayavka,Command.start]:
        #     if re.search('отключение воды', msg):
        #         self.last_command = Command.water
        #     return Message.water_msg.value
        #
        #
        # elif re.search('отключение воды', msg):
        #     self.last_command = Command.water
        #     return Message.water_msg.value
        #
        # elif re.search('упало дерево', msg):
        #     self.last_command = Command.tree
        #     return Message.tree_msg.value
        #
        # elif re.search('поломка светофора', msg):
        #     self.last_command = Command.traffic
        #     return Message.traffic_msg.value
        #
        # elif re.search('отключение света', msg):
        #     self.last_command = Command.light
        #     return Message.light_msg.value
        #
        # elif re.search('0|назад', msg):
        #     self.last_command = None
        #     return Message.start_msg.value
        #
        # else:
        #     self.last_command = Command.emergency_situations
        #     return Message.wrong_msg.value




        # if any(command in msg for command in Command.start.value):
        #    self.last_command = Command.start
        #    return Message.start_msg.value
        # if re.search('3|аварийные ситуации', msg):
        #         self.last_command = Command.emergency_situations
        #         return Message.emergency_situations_msg.value
        # elif re.search('4|внести предложение и идеи', msg):
        #         self.last_command = Command.suggestions
        #         return Message.suggestions_msg.value
        # elif re.search('5|отлов собак', msg):
        #         self.last_command = Command.dog_catching
        #         return Message.dog_catching_msg.value
        # elif re.search('6|движение транспорта', msg):
        #         self.last_command = Command.traffic_movement
        #         return Message.traffic_movement_msg.value
        # elif re.search('0|назад', msg):
        #         self.last_command = None
        #         return Message.start_msg.value

        # if self.last_command == Command.reg:
        #     self.last_command = None  # Сбросить команду после регистрации
        #     return Message.thx_msg.value

        # print(msg)
        return 'Я не знаю такой команды &#128532;'