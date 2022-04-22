from init import *
import spacy,importlib,importlib.util,importlib.machinery
plugins = []
class Client(Config):
    def __init__(self, room, **kwargs) -> None:
        super().__init__(room, **kwargs) 
@bot.listener.on_message_event
async def tell(room, message):
    global servers,plugins
    aClient = None
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix():
        for client in servers:
            if client.room == room.room_id:
                aClient = client
                break
    elif match.is_not_from_this_bot():
        for client in servers:
            if client.room == room.room_id:
                aClient = client
                break
    if not aClient:
        aClient = Client(room.room_id)
    if hasattr(aClient,'activeConversation'):
        aPlugin = aClient.activeConversation
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
async def PluginWatcher():
    global plugins
    PluginPath = pathlib.Path(__file__).parent / 'plugins'
    RelativePath = '.'+str(PluginPath.relative_to(pathlib.Path(__file__).parent.absolute()))
    while True:
        for file in PluginPath.glob('*.py'):
            package = file.name.replace('.py','')
            module = None
            for mod in plugins:
                if mod.__name__ == package:
                    module = mod
                    break
            if module:
                if module._lastchanged < file.lstat().st_mtime:
                    try:
                        module._lastchanged = file.lstat().st_mtime
                        loader = importlib.machinery.SourceFileLoader(package,str(file.absolute()))
                        module = loader.load_module()
                        sys.modules[package] = module
                    except BaseException as e:
                        logging.warning('Failed to reload Plugin %s: %s' % (package,str(e)))
            else:
                try:
                    loader = importlib.machinery.SourceFileLoader(package,str(file.absolute()))
                    module = loader.load_module()
                    module.__loader__ = loader
                    module._lastchanged = file.lstat().st_mtime
                    plugins.append(module)
                except BaseException as e:
                    logging.warning('Failed to load Plugin %s: %s' % (package,str(e)))
        await asyncio.sleep(1)
try:
    if pathlib.Path('data.json').exists():
        with open('data.json', 'r') as f:
            nservers = json.load(f)
            for server in nservers:
                servers.append(Client(server))
except BaseException as e: 
    logging.error('Failed to read data:'+str(e))
    exit(1)
@bot.listener.on_startup
async def startup(room):
    global loop,servers
    if not loop:
        loop = asyncio.get_running_loop()
        loop.create_task(PluginWatcher())
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
                is handled as a mention and forces thalia to answer
            speaking in channel:
                thalia trys to detect if she is target of the question or discussion and try to be gently in answering
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
