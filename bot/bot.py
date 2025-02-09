from util.FileHelper import FileHelper
import telebot
from models.ApplicationUnit import ApplicationUnit

class Bot:
    MAX_ATTEMPTS = 10

    def __init__(self):
        file_helper = FileHelper()
        self.token = file_helper.get_token()
        self.password = file_helper.get_bot_password()
        self.bot = telebot.TeleBot(self.token)
        self.user_status_dict = dict()
        self.attempts_dict = dict()

        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.user_status_dict[message.chat.id] = False
            self.bot.send_message(message.chat.id, "Введи пароль:")

        @self.bot.message_handler(content_types="text")
        def handle_any_message(message):
            if message.chat.id in self.attempts_dict.keys() and self.attempts_dict[message.chat.id] > self.MAX_ATTEMPTS:
                self.bot.send_message(message.chat.id, "Превышено число попыток ввода пароля.\n\nЕсли вы действительный админ, обратитесь к создателю бота с этой проблемой.")
            else:
                if (message.chat.id not in self.user_status_dict.keys()) or (not (self.user_status_dict[message.chat.id])):
                    if message.text == self.password:
                        self.user_status_dict[message.chat.id] = True
                        self.bot.send_message(message.chat.id, "Добро Пожаловать!\nЯ буду присылать все анкеты, которые заполнят на сайте.")
                    else:
                        self.bot.send_message(message.chat.id, "Неверный пароль")
                        if message.chat.id not in self.attempts_dict.keys():
                            self.attempts_dict[message.chat.id] = 1
                        else:
                            self.attempts_dict[message.chat.id] += 1

    def run(self):
        self.bot.infinity_polling()

    def mail_new_application_unit(self, application_unit: ApplicationUnit):
        msg = f"""
        Кто-то заполнил новую анкету на сайте:
    
        id анкеты: ${application_unit.id}
        Дата отправки: ${application_unit.date}
        Имя: ${application_unit.name}
        Телефон: ${application_unit.phone}
        Cообщение: ${application_unit.message}
        """
        users_to_send = [key for key in self.user_status_dict.keys() if self.user_status_dict[key]]
        for user in users_to_send:
            self.bot.send_message(user, msg)
