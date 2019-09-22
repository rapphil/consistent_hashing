from hashlib import sha256

from consistent_hashing.server import Server


def _hash(data):
    hasher = sha256()
    hasher.update(data)
    digest = hasher.digest()

    return digest[-1] + digest[-2] << 8


class Client(object):

    RING_SIZE = 10000

    def __init__(self, server_ips):
        self._servers = [Server(ip) for ip in server_ips]
        self._server_ring = []
        self._init_ring()

    def _init_ring(self):

        self._server_ring = [None for i in range(self.RING_SIZE)]
        for server in self._servers:
            hash1 = _hash(str(server).encode())
            pos1 = hash1 % self.RING_SIZE
            pos2 = _hash(str(pos1).encode()) % self.RING_SIZE
            pos3 = _hash(str(pos2).encode()) % self.RING_SIZE
            pos4 = _hash(str(pos3).encode()) % self.RING_SIZE
            pos5 = _hash(str(pos4).encode()) % self.RING_SIZE
            pos6 = _hash(str(pos5).encode()) % self.RING_SIZE
            self._server_ring[pos1] = server
            self._server_ring[pos2] = server
            self._server_ring[pos3] = server
            self._server_ring[pos4] = server
            self._server_ring[pos5] = server
            self._server_ring[pos6] = server

    def _get_server(self, key):
        pos = _hash(key.encode()) % self.RING_SIZE
        while self._server_ring[pos] == None:
            pos += 1
            pos %= self.RING_SIZE
        return self._server_ring[pos]

    def add_server(self, ip):
        self._servers.append(Server(ip))
        self._init_ring()

    def remove_server(self, ip):
        server = list(filter(lambda x: str(x) == ip, self._servers))
        if len(server) == 1:
            self._servers.remove(server[0])
        self._init_ring()

    def get(self, key):
        server = self._get_server(key)
        return server.get(key)

    def set(self, key, value):
        server = self._get_server(key)
        server.set(key, value)

    def print_servers(self):
        for idx, server in enumerate(self._server_ring):
            if server:
                print(idx, server)
