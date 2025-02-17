from datetime import datetime
from models.ApplicationUnit import ApplicationUnit

class FileHelper:

    def get_bot_password(self):
        return open("config/bot_password.txt", "r").readline().strip()
    def get_history_count(self):
        return open("config/history_count.txt", "r").readline().strip()

    def increment_history_count(self):
        prev_count = int(self.get_history_count())
        prev_count += 1
        file = open("config/history_count.txt", "w")
        file.write(str(prev_count))
        file.close()

    def get_token(self):
        return open("config/token.txt", "r").readline().strip()

    def put_application_unit_to_history(self, application_unit: ApplicationUnit):
        history_count = self.get_history_count()
        filename = "app_" + history_count + "_" + application_unit.date +".json"
        file = open(filename, 'a')
        file.write(application_unit.to_json_string())
        file.close()
        self.increment_history_count()


