
from consistent_hashing.client import Client


def test_client_simple():
    c = Client(["9.9.9.9"])
    c.set("foo", "bar")
    assert c.get("foo") == "bar"

def test_consistent_hashing_remove_server():
    c = Client(["9.9.9." + str(i) for i in range(1,11)])
    NUN_KEYS = 100000
    for i in range(NUN_KEYS):
        key = f"key{i}"
        value = f"value{i}"
        c.set(key, value)

    for i in range(NUN_KEYS):
        key = f"key{i}"
        value = f"value{i}"
        assert c.get(key) == value

    misses = 0
    misses_keys = []

    c.remove_server("9.9.9.1")

    for i in range(NUN_KEYS):
        key = f"key{i}"
        value = f"value{i}"
        v = c.get(key)
        if v:
            assert v == value
        else:
            misses += 1

    assert NUN_KEYS / 10.0 / 2 < misses < NUN_KEYS / 10.0 * 2

def test_consistent_hashing_add_server():
    c = Client(["9.9.9." + str(i) for i in range(1,11)])
    NUN_KEYS = 100000
    for i in range(NUN_KEYS):
        key = f"key{i}"
        value = f"value{i}"
        c.set(key, value)

    for i in range(NUN_KEYS):
        key = f"key{i}"
        value = f"value{i}"
        assert c.get(key) == value

    misses = 0
    misses_keys = []

    c.add_server("9.9.9.11")

    for i in range(NUN_KEYS):
        key = f"key{i}"
        value = f"value{i}"
        v = c.get(key)
        if v:
            assert v == value
        else:
            misses += 1

    assert NUN_KEYS / 11.0 / 2 < misses < NUN_KEYS / 11.0 * 2
