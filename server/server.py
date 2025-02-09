from fastapi import FastAPI, Body, status
from models.ApplicationUnit import ApplicationUnit
from util.FileHelper import FileHelper
from bot.bot import Bot
import datetime


class Server:
    def __init__(self, app: FastAPI, bot: Bot):
        self.app = app
        self.file_helper = FileHelper()
        self.bot = bot

        @self.app.post("/api/applications")
        def create_application_unit(data=Body()):
            date = datetime.now().strftime("%d%m%Y_%H:%M")
            application_unit = ApplicationUnit(data['name'], data['phone'], data['message'], date)
            self.file_helper.put_application_unit_to_history(application_unit)
            self.bot.mail_new_application_unit(application_unit)
