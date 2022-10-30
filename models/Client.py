import discord
import re

class Pattern():
    def __init__(self, whole_pattern: str, *args):
        self.a = []
        self.b = {}

        index = 1
        for arg in args:
            index_p = whole_pattern.find(arg)
            if index_p == -1:
                continue
            
            self.a.append(whole_pattern[:index_p])
            self.a.append(whole_pattern[index_p:index_p + len(arg)])
            self.b[index] = arg
            index += 2
            
            whole_pattern = whole_pattern[index_p + len(arg):]
        
        self.a.append(str(whole_pattern))

    def get(self, d):
        message = ''
        
        for i in range(len(self.a)):
            if i in self.b.keys():
                key = self.b[i]
                try:
                    message += str(d[key])
                except KeyError:
                    raise KeyError('keys must be the same as the thing to change. Example: \'s[season]\' -> {\'[season]\' : 3]} will return \'s3\'')
            else:
                message += self.a[i]

        return message

class Client(discord.Client):
    def __init__(self, SETTINGS):
        super().__init__(intents=discord.Intents.default())
        self.SETTINGS = SETTINGS
        self.channels = {}
        self.load_message_pattern()
    
    def load_message_pattern(self):
        self.message_pattern = Pattern(self.SETTINGS['FORMAT'], '[season]', '[episode]')

    def run(self):
        super().run(self.SETTINGS['TOKEN'])

    async def on_ready(self):
        print('ready')
        guild_id = self.SETTINGS['GUILD_ID']
        self.guild = self.get_guild(guild_id)
        if self.guild is None:
            print('guild does not exist! guild id:', guild_id)
        for channel in self.guild.channels:
            if isinstance(channel, discord.TextChannel):
                self.channels[channel.id] = channel
        
    def test(self, s):
        if (self.is_ready()):
            print('test from:', s)
            #self.create_text_channel('newchannel1')
            self.increment(1036104243712635000, True)

    def send_message(self, message: str, channel_id: int):
        channel = self.get_channel(channel_id)
        if channel is not None:
            print('sending', message)
            self.loop.create_task(channel.send(content=message))
            print('sent\n')
        else:
            print('channel does not exist! channel:', channel_id)

    def create_text_channel(self, channel_name: str):
        if self.guild is not None:
            self.loop.create_task(self._create_text_channel(self.guild, channel_name))
        else:
            print('guild does not exist!')

    async def _create_text_channel(self, guild, channel_name):
        rules = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False)
        }
        channel = await guild.create_text_channel(channel_name, overwrites=rules)

        message = self.SETTINGS['FORMAT']
        message = message.replace('[season]', '1')
        message = message.replace('[episode]', '1')

        self.loop.create_task(channel.send(content=message))
        self.channels[channel.id] = channel

    def delete_channel(self, channel_id: int):
        if channel_id in self.channels.keys():
            self.loop.create_task(self.channels[channel_id].delete())
        else:
            print('the specified channel is not in the list!')

    def increment(self, channel_id: int, increment_episode):
        if channel_id in self.channels.keys():
            channel = self.channels[channel_id]
            self.loop.create_task(self._increment(channel, increment_episode))
        else:
            print('wrong channel id')

    async def _increment(self, channel, increment_episode):
        async for message in channel.history(limit=50, oldest_first=False):
            if message.author is self.guild.me:
                message_content = message.content

                pattern_episode_no = self.SETTINGS['FORMAT']
                pattern_episode_no = pattern_episode_no.replace('[season]', '\d+')
                pattern_episode_no = pattern_episode_no.replace('[episode]', '(\d+)')
                pattern_episode_no = f'^{pattern_episode_no}$'
               
                pattern_season_no = self.SETTINGS['FORMAT']
                pattern_season_no = pattern_season_no.replace('[season]', '(\d+)')
                pattern_season_no = pattern_season_no.replace('[episode]', '\d+')
                pattern_season_no = f'^{pattern_season_no}$'

                try:
                    episode_no = int(re.match(pattern_episode_no, message_content).group(1))
                    season_no = int(re.match(pattern_season_no, message_content).group(1))
                    if increment_episode:
                        new_message = self.message_pattern.get({'[season]': season_no, '[episode]': episode_no + 1})
                    else:
                        new_message = self.message_pattern.get({'[season]': season_no + 1, '[episode]': 1})
                    await message.edit(content=new_message)
                except ValueError:
                    await channel.send('old message corrupted, rip', delete_after=5)
                    #await channel.send('0')
                break

