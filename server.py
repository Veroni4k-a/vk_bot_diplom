import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from handlers.command_enum import Enum,Message,Command
from handlers.commander import Commander
from form.user_form import UserForm
from form.light import LightForm
from form.car_form import CarForm
from form.dog_form import DogForm
import datetime
import pytz
import psycopg2


class Server:
    def __init__(self, api_token, db_config):
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432")
        self.cursor = self.connection.cursor()


        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkLongPoll(self.vk)
        self.vk_api = self.vk.get_api()

        # Connect to the database


        # Dictionary to store user forms
        self.user_forms = {}
        self.dog_forms= {}
        self.rubbish_forms = {}
        self.car_forms= {}
        self.light_forms = {}
        self.traffic_forms = {}

        self.user_states = {}

    def send_message(self, send_id, message, keyboard=None):
        """Отправка сообщения пользователю"""
        return self.vk_api.messages.send(
            user_id=send_id,
            message=message,
            random_id=random.randint(0, 2048),
            keyboard=keyboard  # Передаем клавиатуру
        )

    def load_keyboard(self, file_path):
        """Загрузка клавиатуры из JSON-файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл клавиатуры не найден: {file_path}")
            return None

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                message_text = event.text.lower()  # Приводим текст к нижнему регистру

                print(f"Получено сообщение от {user_id}: {event.text}")

                # Проверяем состояние пользователя
                if user_id not in self.user_states:
                    self.user_states[user_id] = 'main_menu'  # Устанавливаем начальное состояние

                # Обработка состояния стартового меню
                if self.user_states[user_id] == 'main_menu':
                    kbd_main = self.load_keyboard("keyboard/keyboard.json")
                    response_message = "Выберите действие:\n1. Получить информацию\n2. Подать заявки"
                    self.send_message(user_id, response_message, kbd_main)

                    if message_text in ["получить информацию", "информация"]:
                        kbd_info = self.load_keyboard("keyboard/keyboard_information.json")
                        response_message_info = "В данном разделе Вы можете получить информацию без отправки заявок."
                        self.send_message(user_id, response_message_info, kbd_info)
                        self.user_states[user_id] = 'info_menu'
                        continue

                    if message_text in ["подать заявку", "заявки"]:
                        kbd_zayavka = self.load_keyboard("keyboard/keyboard_zayavka.json")
                        response_message_zayavka = "Вот информация, которую вы запрашивали, выберите какую заявку желаете оставить:"
                        self.send_message(user_id, response_message_zayavka, kbd_zayavka)
                        self.user_states[user_id] = 'zayavka_menu'  # Переход в новое состояние
                        continue

                if self.user_states.get(user_id) == 'info_menu':
                    if message_text in ["11", "отключение воды"]:

                        self.send_message(user_id,Message.water_msg.value)
                        continue

                    if message_text in ["12", "отключение электричества"]:

                        self.send_message(user_id,Message.light_msg.value)
                        continue

                    if message_text in ["13", "карта уборки города"]:

                        self.send_message(user_id,Message.map_msg.value)
                        continue
                    if message_text in ["14", "транспорт"]:

                        self.send_message(user_id,Message.traffic_movement_msg.value)
                        continue

                    if message_text and message_text.lower() == "в главное меню":
                        self.user_states[user_id] = 'main_menu'  # Изменяем состояние на 'main_menu'
                        kbd_main = self.load_keyboard("keyboard/keyboard.json")  # Загружаем клавиатуру главного меню
                        main_menu_msg = "Вы вернулись в главное меню. Чем могу помочь?"  # Сообщение о возвращении
                        self.send_message(user_id, main_menu_msg, kbd_main)  # Отправляем сообщение и клавиатуру
                        continue

                # Обработка состояния подачи заявок
                if self.user_states[user_id] == 'zayavka_menu':

                    if message_text and message_text.lower() == "в главное меню":
                        self.user_states[user_id] = 'main_menu'  # Изменяем состояние на 'main_menu'
                        kbd_main = self.load_keyboard("keyboard/keyboard.json")  # Загружаем клавиатуру главного меню
                        main_menu_msg = "Вы вернулись в главное меню. Чем могу помочь?"  # Сообщение о возвращении
                        self.send_message(user_id, main_menu_msg, kbd_main)  # Отправляем сообщение и клавиатуру
                        continue


                    if event.text and event.text.lower() == "отлов собак":
                        if user_id not in self.dog_forms:
                            self.dog_forms[user_id] = DogForm()  # Initialize UserForm instance
                        dog = self.dog_forms[user_id]
                        kbd_empty = self.load_keyboard("keyboard/keaboard_empty.json")
                        response_message = "Введите ваше ФИО:"
                        dog.state = 'waiting_for_full_name'
                        self.send_message(user_id, response_message,kbd_empty)
                        continue

                    if user_id in self.dog_forms:
                        dog = self.dog_forms[user_id]

                        if dog.state == 'waiting_for_full_name':
                            dog.set_full_name(event.text)
                            response_message = "Введите ваш телефон:"
                            dog.state = 'waiting_for_phone'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif dog.state == 'waiting_for_phone':
                            dog.set_phone(event.text)
                            response_message = "Введите описание:"
                            dog.state = 'waiting_for_description'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif dog.state == 'waiting_for_description':
                            dog.set_description(event.text)
                            response_message = "Отправьте породу собаки."
                            dog.state = 'waiting_for_breed'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif dog.state == 'waiting_for_breed':
                            dog.set_breed(event.text)
                            response_message = "Отправьте свою геолокацию (вложение)."
                            dog.state = 'waiting_for_location'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)




                        elif dog.state == 'waiting_for_location':
                            result = self.vk_api.messages.getById(message_ids=event.message_id, group_id=216213993)
                            geo = result['items'][0]['geo']['coordinates']
                            latitude, longitude = geo['latitude'], geo['longitude']
                            print(latitude, longitude)
                            dog.set_location(latitude, longitude)
                            if dog.is_dog_completed():

                                self.save_to_db_dog(dog)
                                response_message = "Форма успешно заполнена!"
                                print(f'refge')
                                del self.dog_forms[user_id]

                                self.user_states[user_id] = 'zayavka_menu'
                                kbd_zav = self.load_keyboard("keyboard/keyboard_zayavka.json")
                                self.send_message(user_id, response_message, kbd_zav)
                                # Remove the form after completion
                            else:
                                response_message = "Произошла ошибка при заполнении формы."

                                del self.dog_forms[user_id]
                                kbd_main = self.load_keyboard("keyboard/keyboard.json")
                                self.send_message(user_id, response_message,
                                                  kbd_main)  # Отправляем сообщение с клавиатурой


                    if event.text and event.text.lower() == "упало дерево":
                        if user_id not in self.user_forms:
                            self.user_forms[user_id] = UserForm()  # Initialize UserForm instance
                        form = self.user_forms[user_id]
                        kbd_empty = self.load_keyboard("keyboard/keaboard_empty.json")
                        response_message = "Введите ваше ФИО:"
                        form.state = 'waiting_for_full_name'
                        self.send_message(user_id, response_message,kbd_empty)
                        continue

                    # Process the form based on the current state
                    if user_id in self.user_forms:
                        form = self.user_forms[user_id]

                        if form.state == 'waiting_for_full_name':
                            form.set_full_name(event.text)
                            response_message = "Введите ваш телефон:"
                            form.state = 'waiting_for_phone'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif form.state == 'waiting_for_phone':
                            form.set_phone(event.text)
                            response_message = "Введите описание:"
                            form.state = 'waiting_for_description'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif form.state == 'waiting_for_description':
                            form.set_description(event.text)
                            response_message = "Отправьте свою геолокацию (вложение)."
                            form.state = 'waiting_for_location'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)


                        elif form.state == 'waiting_for_location':
                            result = self.vk_api.messages.getById(message_ids=event.message_id, group_id=216213993)
                            geo = result['items'][0]['geo']['coordinates']
                            latitude, longitude = geo['latitude'], geo['longitude']
                            print(latitude, longitude)
                            form.set_location(latitude, longitude)
                            if form.is_completed():

                                self.save_to_db(form)
                                response_message = "Форма успешно заполнена!"
                                print(f'refge')
                                del self.user_forms[user_id]

                                self.user_states[user_id] = 'zayavka_menu'
                                kbd_zav = self.load_keyboard("keyboard/keyboard_zayavka.json")
                                self.send_message(user_id, response_message, kbd_zav)
                            else:
                                response_message = "Произошла ошибка при заполнении формы."

                                del self.user_forms[user_id]
                                kbd_main = self.load_keyboard("keyboard/keyboard.json")
                                self.send_message(user_id, response_message,
                                                  kbd_main)

                    if event.text and event.text.lower() == "уборка мусора":
                        if user_id not in self.rubbish_forms:
                            self.rubbish_forms[user_id] = UserForm()  # Initialize UserForm instance
                        rubbish = self.rubbish_forms[user_id]
                        kbd_empty = self.load_keyboard("keyboard/keaboard_empty.json")
                        response_message = "Введите ваше ФИО:"
                        rubbish.state = 'waiting_for_full_name'
                        self.send_message(user_id, response_message,kbd_empty)
                        continue

                    # Process the rubbish based on the current state
                    if user_id in self.rubbish_forms:
                        rubbish = self.rubbish_forms[user_id]

                        if rubbish.state == 'waiting_for_full_name':
                            rubbish.set_full_name(event.text)
                            response_message = "Введите ваш телефон:"
                            rubbish.state = 'waiting_for_phone'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif rubbish.state == 'waiting_for_phone':
                            rubbish.set_phone(event.text)
                            response_message = "Расскажите с какой проблемой Вы стокнулись:"
                            rubbish.state = 'waiting_for_description'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif rubbish.state == 'waiting_for_description':
                            rubbish.set_description(event.text)
                            response_message = "Отправьте свою геолокацию (вложение)."
                            rubbish.state = 'waiting_for_location'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)




                        elif rubbish.state == 'waiting_for_location':
                            result = self.vk_api.messages.getById(message_ids=event.message_id, group_id=216213993)
                            geo = result['items'][0]['geo']['coordinates']
                            latitude, longitude = geo['latitude'], geo['longitude']
                            print(latitude, longitude)
                            rubbish.set_location(latitude, longitude)
                            if rubbish.is_completed():

                                self.save_to_db_rubbish(rubbish)
                                response_message = "Форма успешно заполнена!"
                                print(f'refge')
                                del self.rubbish_forms[user_id]

                                self.user_states[user_id] = 'zayavka_menu'
                                kbd_zav = self.load_keyboard("keyboard/keyboard_zayavka.json")
                                self.send_message(user_id, response_message, kbd_zav)
                            else:
                                response_message = "Произошла ошибка при заполнении формы."

                                del self.rubbish_forms[user_id]
                                kbd_main = self.load_keyboard("keyboard/keyboard.json")
                                self.send_message(user_id, response_message,
                                                  kbd_main)



                    if event.text and event.text.lower() == "брошенный транспорт":
                        if user_id not in self.car_forms:
                            self.car_forms[user_id] = CarForm()  # Initialize UserForm instance
                        car = self.car_forms[user_id]
                        kbd_empty = self.load_keyboard("keyboard/keaboard_empty.json")
                        response_message = "Введите ваше ФИО:"
                        car.state = 'waiting_for_full_name'
                        self.send_message(user_id, response_message,kbd_empty)
                        continue

                    if user_id in self.car_forms:
                        car = self.car_forms[user_id]

                        if car.state == 'waiting_for_full_name':
                            car.set_full_name(event.text)
                            response_message = "Введите ваш телефон:"
                            car.state = 'waiting_for_phone'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif car.state == 'waiting_for_phone':
                            car.set_phone(event.text)
                            response_message = "Введите описание:"
                            car.state = 'waiting_for_description'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif car.state == 'waiting_for_description':
                            car.set_description(event.text)
                            response_message = "Отправьте номер брошенного транспорта \nЕсли его нет или плохо видно, то напишите об этом."
                            car.state = 'waiting_for_number'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)

                        elif car.state == 'waiting_for_number':
                            car.set_number(event.text)
                            response_message = "Отправьте свою геолокацию (вложение)."
                            car.state = 'waiting_for_location'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)


                        elif car.state == 'waiting_for_location':
                            result = self.vk_api.messages.getById(message_ids=event.message_id, group_id=216213993)
                            geo = result['items'][0]['geo']['coordinates']
                            latitude, longitude = geo['latitude'], geo['longitude']
                            print(latitude, longitude)
                            car.set_location(latitude, longitude)
                            if car.is_car_completed():

                                self.save_to_db_car(car)
                                response_message = "Форма успешно заполнена!"
                                print(f'refge')
                                del self.dog_forms[user_id]

                                self.car_forms[user_id] = 'zayavka_menu'
                                kbd_zav = self.load_keyboard("keyboard/keyboard_zayavka.json")
                                self.send_message(user_id, response_message, kbd_zav)
                            else:
                                response_message = "Произошла ошибка при заполнении формы."

                                del self.car_forms[user_id]
                                kbd_main = self.load_keyboard("keyboard/keyboard.json")
                                self.send_message(user_id, response_message,
                                                  kbd_main)

                    if event.text and event.text.lower() == "проблемы с освещением":
                        if user_id not in self.light_forms:
                            self.light_forms[user_id] = LightForm()  # Initialize UserForm instance
                        light = self.light_forms[user_id]
                        kbd_empty = self.load_keyboard("keyboard/keaboard_empty.json")
                        response_message = "Введите ваше ФИО:"
                        light.state = 'waiting_for_full_name'
                        self.send_message(user_id, response_message,kbd_empty)
                        continue

                    if user_id in self.light_forms:
                        light = self.light_forms[user_id]

                        if light.state == 'waiting_for_full_name':
                            light.set_full_name(event.text)
                            response_message = "Введите ваш телефон:"
                            light.state = 'waiting_for_phone'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif light.state == 'waiting_for_phone':
                            light.set_phone(event.text)
                            response_message = "Введите описание:"
                            light.state = 'waiting_for_description'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif light.state == 'waiting_for_description':
                            light.set_description(event.text)
                            response_message = "Напишите время отключения:"
                            light.state = 'waiting_for_light'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif light.state == 'waiting_for_light':
                            light.set_light(event.text)
                            response_message = "Отправьте свою геолокацию (вложение)."
                            light.state = 'waiting_for_location'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)


                        elif light.state == 'waiting_for_location':
                            result = self.vk_api.messages.getById(message_ids=event.message_id, group_id=216213993)
                            geo = result['items'][0]['geo']['coordinates']
                            latitude, longitude = geo['latitude'], geo['longitude']
                            print(latitude, longitude)
                            light.set_location(latitude, longitude)
                            if light.is_light_completed():

                                self.save_to_db_light(light)
                                response_message = "Форма успешно заполнена!"
                                print(f'refge')
                                del self.light_forms[user_id]

                                self.user_states[user_id] = 'zayavka_menu'
                                kbd_zav = self.load_keyboard("keyboard/keyboard_zayavka.json")
                                self.send_message(user_id, response_message, kbd_zav)
                                # Remove the form after completion
                            else:
                                response_message = "Произошла ошибка при заполнении формы."

                                del self.light_forms[user_id]
                                kbd_main = self.load_keyboard("keyboard/keyboard.json")
                                self.send_message(user_id, response_message,
                                                  kbd_main)

                    if event.text and event.text.lower() == "поломка светофора":
                        if user_id not in self.traffic_forms:
                            self.traffic_forms[user_id] = UserForm()  # Initialize UserForm instance
                        traffic = self.traffic_forms[user_id]
                        kbd_empty = self.load_keyboard("keyboard/keaboard_empty.json")
                        response_message = "Введите ваше ФИО:"
                        traffic.state = 'waiting_for_full_name'
                        self.send_message(user_id, response_message,kbd_empty)
                        continue

                        # Process the form based on the current state
                    if user_id in self.traffic_forms:
                        traffic = self.traffic_forms[user_id]

                        if traffic.state == 'waiting_for_full_name':
                            traffic.set_full_name(event.text)
                            response_message = "Введите ваш телефон:"
                            traffic.state = 'waiting_for_phone'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif traffic.state == 'waiting_for_phone':
                            traffic.set_phone(event.text)
                            response_message = "Введите описание, где, когда и при каких обстоятельствах произошла поломка:"
                            traffic.state = 'waiting_for_description'
                            self.send_message(user_id, response_message,kbd_empty)

                        elif traffic.state == 'waiting_for_description':
                            traffic.set_description(event.text)
                            response_message = "Отправьте свою геолокацию (вложение)."
                            traffic.state = 'waiting_for_location'
                            kbd_geo = self.load_keyboard("keyboard/keyboard_geo.json")
                            self.send_message(user_id, response_message, kbd_geo)



                        elif traffic.state == 'waiting_for_location':
                            result = self.vk_api.messages.getById(message_ids=event.message_id, group_id=216213993)
                            geo = result['items'][0]['geo']['coordinates']
                            latitude, longitude = geo['latitude'], geo['longitude']
                            print(latitude, longitude)
                            traffic.set_location(latitude, longitude)
                            if traffic.is_completed():

                                self.save_to_db_traffic(traffic)
                                response_message = "Форма успешно заполнена!"
                                print(f'refge')
                                del self.traffic_forms[user_id]

                                self.user_states[user_id] = 'zayavka_menu'
                                kbd_zav = self.load_keyboard("keyboard/keyboard_zayavka.json")
                                self.send_message(user_id, response_message, kbd_zav)
                            else:
                                response_message = "Произошла ошибка при заполнении формы."

                                del self.traffic_forms[user_id]
                                kbd_main = self.load_keyboard("keyboard/keyboard.json")
                                self.send_message(user_id, response_message,
                                                  kbd_main)


    def save_to_db_dog(self, dog):
        """Save user data to the database"""
        insert_query = """
                     INSERT INTO dog_forms (full_name, phone, description,breed, latitude, longitude) 
                     VALUES (%s, %s, %s, %s, %s,%s);
                 """

        latitude, longitude = map(float, dog.location)

        data_to_insert = (dog.full_name, dog.phone, dog.description, dog.breed,
                          latitude, longitude)

        # Execute insert query
        try:
            if self.cursor is not None:
                self.cursor.execute(insert_query, data_to_insert)
                self.connection.commit()
                print("Data saved successfully.")
            else:
                print("Cursor is not initialized.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection_dog(self):
        """Close database connection"""
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

    def save_to_db(self, form):
        """Save user data to the database"""
        insert_query = """
               INSERT INTO user_forms (full_name, phone, description, latitude, longitude) 
               VALUES (%s, %s, %s, %s, %s);
           """

        latitude, longitude = map(float, form.location)

        data_to_insert = (form.full_name, form.phone, form.description,
                          latitude, longitude)

        # Execute insert query
        try:
            if self.cursor is not None:
                self.cursor.execute(insert_query, data_to_insert)
                self.connection.commit()
                print("Data saved successfully.")
            else:
                print("Cursor is not initialized.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection(self):
        """Close database connection"""
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

    def save_to_db_rubbish(self, rubbish):
        """Save user data to the database"""
        insert_query = """
               INSERT INTO rubbish_forms (full_name, phone, description, latitude, longitude) 
               VALUES (%s, %s, %s, %s, %s);
           """

        latitude, longitude = map(float, rubbish.location)

        data_to_insert = (rubbish.full_name, rubbish.phone, rubbish.description,
                          latitude, longitude)

        # Execute insert query
        try:
            if self.cursor is not None:
                self.cursor.execute(insert_query, data_to_insert)
                self.connection.commit()
                print("Data saved successfully.")
            else:
                print("Cursor is not initialized.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection_rubbish(self):
        """Close database connection"""
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

    # Форма с машинами заполнение в бд
    def save_to_db_car(self, car):
        """Save user data to the database"""
        insert_query = """
               INSERT INTO car_forms (full_name, phone, description,number_avto, latitude, longitude) 
               VALUES (%s, %s, %s, %s, %s,%s);
           """

        latitude, longitude = map(float, car.location)

        data_to_insert = (car.full_name, car.phone, car.description,car.number,
                          latitude, longitude)

        # Execute insert query
        try:
            if self.cursor is not None:
                self.cursor.execute(insert_query, data_to_insert)
                self.connection.commit()
                print("Data saved successfully.")
            else:
                print("Cursor is not initialized.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection_car(self):
        """Close database connection"""
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

    # Форма с проблемами по свету заполнение в бд

    def save_to_db_light(self, light):
        """Save user data to the database"""
        insert_query = """
               INSERT INTO light_forms (full_name, phone, description,light, latitude, longitude) 
               VALUES (%s, %s, %s, %s, %s, %s);
           """

        latitude, longitude = map(float, light.location)

        data_to_insert = (light.full_name, light.phone, light.description,light.light,
                          latitude, longitude)

        # Execute insert query
        try:
            if self.cursor is not None:
                self.cursor.execute(insert_query, data_to_insert)
                self.connection.commit()
                print("Data saved successfully.")
            else:
                print("Cursor is not initialized.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection_light(self):
        """Close database connection"""
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()





    # Форма с светофором заполнение в бд
    def save_to_db_traffic(self, traffic):
        """Save user data to the database"""
        insert_query = """
               INSERT INTO traffic_forms (full_name, phone, description, latitude, longitude) 
               VALUES (%s, %s, %s, %s, %s);
           """

        latitude, longitude = map(float, traffic.location)

        data_to_insert = (traffic.full_name, traffic.phone, traffic.description,
                          latitude, longitude)

        # Execute insert query
        try:
            if self.cursor is not None:
                self.cursor.execute(insert_query, data_to_insert)
                self.connection.commit()
                print("Data saved successfully.")
            else:
                print("Cursor is not initialized.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection_traffic(self):
        """Close database connection"""
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()