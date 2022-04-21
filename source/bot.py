#https://github.com/DS4A-team34/ds4a_application/blob/736c69e002cf4a46f83cbd8c522ee6b0029f0793/common6.py
from init import *
import spacy
nlp = spacy.load("de_core_news_sm")
@bot.listener.on_message_event
class Client(Config):
    def __init__(self, room, **kwargs) -> None:
        super().__init__(room, **kwargs) 
async def tell(room, message):
    global servers,lastsend
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix():
        for server in servers:
            if server['room'] == room.room_id:
                pass
    elif match.is_not_from_this_bot():
        for server in servers:
            if server['room'] == room.room_id:
                pass
async def check_server(server):
    global servers
    while True:
        try:
            pass
        except BaseException as e:
            if 'Connection' in str(e): pass
            else:
                await bot.api.send_text_message(server['room'],str(e))
        await asyncio.sleep(1)
try:
    with open('data.json', 'r') as f:
        nservers = json.load(f)
        for server in nservers:
            servers.append(Server(server))
except BaseException as e: 
    logging.error('Failed to read config.yml:'+str(e))
    exit(1)
@bot.listener.on_startup
async def startup(room):
    global loop,servers
    loop = asyncio.get_running_loop()
    for server in servers:
        if server['room'] == room:
            loop.create_task(check_server(server))
@bot.listener.on_message_event
async def bot_help(room, message):
    bot_help_message = f"""
    Help Message:
        prefix: {prefix}
        commands:
            speaking to bot:
                is used as rcon console command when you are in the admins list
            speaking in channel:
                is send as server global chat message if supported
            listen:
                command: listen server rcon_port [password] [Query Port]
                description: add ark server
            help:
                command: help, ?, h
                description: display help command
                """
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix() and (
       match.command("help") 
    or match.command("?") 
    or match.command("h")):
        await bot.api.send_text_message(room.room_id, bot_help_message)
bot.run()