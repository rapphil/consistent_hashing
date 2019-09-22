

class Server(object):
    def __init__(self, ip):
        self._ip = ip
        self._mem = {}

    def get(self, key):
        return self._mem.get(key)

    def set(self, key, value):
        self._mem[key] = value

    def __str__(self):
        return str(self._ip)
