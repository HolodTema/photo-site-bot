import uuid
import json


class ApplicationUnit:
    def __init__(self, name, phone, message, date):
        self.id = str(uuid.uuid4())
        self.name = name
        self.phone = phone
        self.message = message
        self.date = date

    def to_json_string(self):
        return str(json.dumps(self.__dict__))

    def __str__(self):
        return
