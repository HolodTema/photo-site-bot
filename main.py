from bot.bot import Bot
from server.server import Server
from fastapi import FastAPI

bot = Bot()
bot.run()

app = FastAPI()
server = Server(app, bot)
