import argparse
import logging
import logging.config
from config import conf, CustomFilter


def command_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true")
    parser.add_argument("-f", action="store_true")
    return parser


class Node:
    def __init__(self, key, value):
        root.debug("creating the new node '%s: %s'", key, value)
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, limit=42):
        root.debug("creating the new cache with limit %s", limit)
        self.cache = {}
        self.limit = limit
        self.head = None
        self.tail = None

    def get(self, key):
        if key not in self.cache:
            root.warning("get the nonexistent key '%s'", key)
            return None

        root.info("get the existent key '%s'", key)
        node = self.cache[key]
        self.remove_node(node)
        self.move_to_head(node)
        return node.value

    def set(self, key, value):
        if key in self.cache:
            root.info("set value '%s' for the existent key '%s'", value, key)
            self.remove_node(self.cache[key])
            node = Node(key, value)
            self.move_to_head(node)
            self.cache[key] = node
        else:
            root.info("set value '%s' for the nonexistent key '%s'", value, key)
            node = Node(key, value)
            self.move_to_head(node)
            self.cache[key] = node

        if len(self.cache) > self.limit:
            root.debug("set node '%s : %s' to cache over the limit", key, value)
            node_to_remove = self.tail
            self.remove_node(node_to_remove)
            del self.cache[node_to_remove.key]

    def remove_node(self, node):
        if node == self.head:
            root.debug("remove the head node '%s : %s'", node.key, node.value)
            self.head = node.next
        elif node == self.tail:
            root.debug("remove the tail node '%s : %s'", node.key, node.value)
            self.tail = node.prev
            self.tail.next = None
        else:
            root.debug("remove node '%s : %s'", node.key, node.value)
            node.prev.next = node.next
            node.next.prev = node.prev
        node.prev = None
        node.next = None

    def move_to_head(self, node):
        if self.head is None:
            root.debug("move node '%s : %s' to head when head is None",
                       node.key, node.value)
            self.head = node
        elif self.tail is None:
            root.debug("move node '%s : %s' to head when tail is None",
                       node.key, node.value)
            self.tail = self.head
            self.head = node
            self.head.next = self.tail
            self.tail.prev = self.head
        else:
            root.debug("move node '%s : %s' to head", node.key, node.value)
            node.next = self.head
            self.head.prev = node
            self.head = node


def operations_with_cache():
    cache = LRUCache(2)
    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"

    cache.set("k1", "newval1")

    assert cache.get("k1") == "newval1"


def add_stream_handler():
    conf["loggers"].update({
        "": {
            "level": "DEBUG",
            "handlers": ["file_handler", "stream_handler"]
        }
    })
    logging.config.dictConfig(conf)


def add_filter(logger):
    for handler in logger.handlers:
        handler.addFilter(CustomFilter())


if __name__ == "__main__":
    parser_args = command_line_parser()
    args = parser_args.parse_args()

    logging.config.dictConfig(conf)
    root = logging.getLogger()

    if args.s:
        add_stream_handler()

    if args.f:
        add_filter(root)

    operations_with_cache()
