from init import *
import spacy,importlib,importlib.util,importlib.machinery,nlp
ColoredOutput(logging.DEBUG)
plugins = []
class Client(Config):
    def __init__(self, room, **kwargs) -> None:
        super().__init__(room, **kwargs) 
@bot.listener.on_message_event
async def tell(room, message):
    global servers,plugins
    aClient = None
    ForceAnser = None
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix():
        ForceAnser = True
        for client in servers:
            if client.room == room.room_id and message.sender == client.sender:
                aClient = client
                break
    elif match.is_not_from_this_bot():
        ForceAnser = False
        for client in servers:
            if client.room == room.room_id and message.sender == client.sender:
                aClient = client
                break
    if not ForceAnser == None:
        aClient = Client(room.room_id,sender=message.sender)
    else: return
    aPlugin = None
    res = None
    analysed_en = nlp.analyse_sentence(message.body,'en')
    analysed = nlp.analyse_sentence(message.body,'de')
    if analysed:
        undef_token = 0
        for token in analysed:
            if token.pos_ == 'X':
                undef_token += 0.5
        if undef_token > 0 or (len(analysed)<=(message.body.count(" "))):
            undef_token_en = 0
            for token in analysed_en:
                if token.pos_ == 'X':
                    undef_token_en += 0.5
            if undef_token_en < undef_token:
                analysed = analysed_en
    logging.debug('language: {lang}'.format(lang=analysed.lang_))
    logging.debug(    '{text:<12}{pos:<6}{tag:<6}{lemma:<10}{label:<6}{dep:<6}{childs:<25}{entid:<7}{vector:<8}'.format(text='text',vector='vector',pos='pos',tag='tag',lemma='lemma',label='label',entid='entid',dep='dep',childs='childs'))
    for token in analysed:
        logging.debug('{text:<12}{pos:<6}{tag:<6}{lemma:<10}{label:<6}{dep:<6}{childs:<25}{entid:<7}{vector:<8}'.format(text=token.text,vector=str(round(token.vector_norm,4)),pos=token.pos_,tag=token.tag_,lemma=token.lemma_,label=token.ent_type_,entid=token.ent_id_,dep=token.dep_,childs=str([child for child in token.children])))
    if hasattr(aClient,'activeConversation') and aClient.activeConversation != {}:
        aPlugin = aClient.activeConversation['_plugin']
        res = await aPlugin.CheckSentence(analysed,aClient,ForceAnser)
        if res:
            aClient.activeConversation['_plugin'] = aPlugin
        else:
            aPlugin = None
    if not aPlugin:
        aClient.activeConversation = {}
        for plugin in plugins:
            try:
                res = await plugin.CheckSentence(analysed,aClient,ForceAnser)
                if res:
                    aClient.activeConversation['_plugin'] = plugin
                    servers.append(aClient)
                    break
            except BaseException as e:logging.warning(str(e))
    if res:
        await bot.api.send_text_message(room.room_id,res['text'])
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
        for file in PluginPath.glob('**/*.py'):
            package = str(file.relative_to(pathlib.Path(__file__).parent)).replace('.py','').replace('/','.')
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
