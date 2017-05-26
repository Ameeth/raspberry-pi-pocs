import json
class MyEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation.

    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)

class TvChannel:
    def __init__(self, channelName, channelNo, genre):
        self.channelName = channelName
        self.channelNo = channelNo
        self.genre = genre
    def __json__(self):
        return {'channelName': self.channelName, 'channelNo': self.channelNo, 'genre': self.genre}
