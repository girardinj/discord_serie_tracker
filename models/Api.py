
import time


class Api:
    def __init__(self, client):
        self.client = client
        self.client_ready = False

    def init_html(self):
        while not self.client.is_ready():
            time.sleep(0.5)
        print('html initialized')
        self.client_ready = True

    def test(self):
        print('test')
    
    def load_channels(self):
        ret = {'channels': []}

        for channel in self.client.get_text_channels():
            ret['channels'].append({'name': str(channel.name), 'id': str(channel.id)})

        print(ret)
        return ret

    def increment(self, channel_id, increment_episode):
        if self.client_ready:
            self.client.increment(int(channel_id), increment_episode)

    def create_text_channel(self, channel_name):
        if self.client_ready:
            self.client.create_text_channel(channel_name)
