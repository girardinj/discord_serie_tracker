
import time
from tkinter import E


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

        return ret

    def increment(self, channel_id, increment_episode):
        if self.client_ready:
            try:
                c_id = int(channel_id)
                self.client.increment(c_id, increment_episode)
            except TypeError:
                return {'message': 'error converting id'}

    def create_text_channel(self, channel_name):
        if self.client_ready:
            self.client.create_text_channel(channel_name)

    def manual_update_episode(self, channel_id, season_no, number_no):
        if self.client_ready:
            try:
                c_id = int(channel_id)
                s_no = int(season_no)
                n_no = int(number_no)
                self.client.manual_update_episode(c_id, s_no, n_no)
            except TypeError:
                return {'message': 'error converting values'}
    # TODO: change if self.client.ready with decorators !
