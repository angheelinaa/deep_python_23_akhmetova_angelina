class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, limit=42):
        self.cache = {}
        self.limit = limit
        self.head = None
        self.tail = None

    def get(self, key):
        if key not in self.cache:
            return None

        node = self.cache[key]
        self.remove_node(node)
        self.move_to_head(node)
        return node.value

    def set(self, key, value):
        if key in self.cache:
            self.remove_node(self.cache[key])
        node = Node(key, value)
        self.move_to_head(node)
        self.cache[key] = node

        if len(self.cache) > self.limit:
            node_to_remove = self.tail
            self.remove_node(node_to_remove)
            del self.cache[node_to_remove.key]

    def remove_node(self, node):
        if node == self.head:
            self.head = node.next
        elif node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        node.prev = None
        node.next = None

    def move_to_head(self, node):
        if self.head is None:
            self.head = node
        elif self.tail is None:
            self.tail = self.head
            self.head = node
            self.head.next = self.tail
            self.tail.prev = self.head
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
