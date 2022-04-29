import simplematrixbotlib as botlib,yaml,json,logging,asyncio,nio,sys,pathlib
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
try: 
    prefix = config['server']['prefix']
except:
    prefix = config['server']['user']
creds = botlib.Creds(config['server']['url'], config['server']['user'], config['server']['password'])
bot = botlib.Bot(creds)
class Config(object):
    def __init__(self,room,**kwargs) -> None:
        if isinstance(room, dict):
            self.__dict__.update(room)
        else:
            self.room = room
            self.__dict__.update(kwargs)
loop = None
servers = []
async def save_servers():
    global servers
    sservers = []
    for server in servers:
        ndict = {k: v for k, v in server.__dict__.items() if not k.startswith('_')}
        sservers.append(ndict)
    with open('data.json', 'w') as f:
        json.dump(sservers,f, skipkeys=True, indent=4)
def is_valid_event(event):
    events = (nio.RoomMessageFormatted, nio.RedactedEvent)
    events += (nio.RoomMessageMedia, nio.RoomEncryptedMedia)
    return isinstance(event, events)
async def fetch_room_events(
    client,
    start_token: str,
    room,
    direction,
    limit
) -> list:
    events = []
    while len(events)<limit:
        response = await client.room_messages(
            room.room_id, start_token, limit=10, direction=direction
        )
        if len(response.chunk) == 0:
            break
        events.extend(event for event in response.chunk if is_valid_event(event))
        start_token = response.end
    return events
async def get_room_events(client, room, limit = 1):
    sync_resp = await client.sync(
        full_state=True, sync_filter={"room": {"timeline": {"limit": limit}}}
    )
    start_token = sync_resp.rooms.join[room].timeline.prev_batch
    # Generally, it should only be necessary to fetch back events but,
    # sometimes depending on the sync, front events need to be fetched
    # as well.
    events = await fetch_room_events(client,start_token,bot.api.async_client.rooms[room],nio.MessageDirection.back,limit)
    return events
def ColoredOutput(log_level):
    def set_color(level, code):
        level_fmt = "\033[1;" + str(code) + "m%s\033[1;0m" 
        logging.addLevelName( level, level_fmt % logging.getLevelName(level) )
    std_stream = sys.stdout
    isatty = getattr(std_stream, 'isatty', None)
    if isatty and isatty():
        levels = [logging.DEBUG, logging.CRITICAL, logging.WARNING, logging.ERROR]
        set_color(logging.WARNING, 34)
        set_color(logging.ERROR, 31)
        set_color(logging.CRITICAL, 45)
        for idx, level in enumerate(levels):
            set_color(level, 30 + idx )
    logging.basicConfig(stream=std_stream, level=log_level)
    logging.root.setLevel(log_level)
ColoredOutput(logging.root.getEffectiveLevel())