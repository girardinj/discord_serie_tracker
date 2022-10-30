
class Api:
    def __init__(self, client):
        self.client = client

    def test(self):
        self.client.test('from api')


