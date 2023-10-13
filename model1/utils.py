class DLLNode:
    def __init__(self, key, val):
        self.val = val
        self.key = key
        self.prev = None
        self.next = None
        self.freq=1

class LRU_Cache:
    def __init__(self, capacity):
        # capacity:  capacity of cache
        # Initialize all variable
        self.capacity = capacity
        self.map = {}
        self.head = DLLNode(0, 0)
        self.tail = DLLNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.count = 0

    def deleteNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def addToHead(self, node):
        node.next = self.head.next
        node.next.prev = node
        node.prev = self.head
        self.head.next = node
    
    def get(self, key):
        if key in self.map:
            node = self.map[key]
            result = node.val
            self.deleteNode(node)
            self.addToHead(node)
            print('Got the value : {} for the key: {}'.format(result, key, node.freq))
            return result
        print('Did not get any value for the key: {}'.format(key))
        return -1
    
    def set(self, key, value):
        print('going to set the (key, value) : ( {}, {})'.format(key, value))
        if key in self.map:
            node = self.map[key]
            node.val = value
            self.deleteNode(node)
            self.addToHead(node)
        else:
            node = DLLNode(key, value)
            self.map[key] = node
            if self.count < self.capacity:
                self.count += 1
                self.addToHead(node)
            else:
                del self.map[self.tail.prev.key]
                self.deleteNode(self.tail.prev)
                self.addToHead(node)

class LFU_Cache:
    def __init__(self, capacity):
        # capacity: capacity of cache
        # Initialize all variables
        self.capacity = capacity
        self.map = {}  # Stores key-node mapping
        self.freq_map = {}  # Stores frequency-doubly linked list mapping
        self.min_freq = 0  # Track the minimum frequency
        self.head = DLLNode(0, 0)  # Doubly linked list head
        self.tail = DLLNode(0, 0)  # Doubly linked list tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def deleteNode(self, node):
        # Helper method to delete a node from a doubly linked list
        node.prev.next = node.next
        node.next.prev = node.prev

    def addToHead(self, node):
        # Helper method to add a node to the head of a doubly linked list
        node.next = self.head.next
        node.next.prev = node
        node.prev = self.head
        self.head.next = node

    def increaseFrequency(self, node):
        # Increase the frequency of a node
        node.freq += 1
        self.deleteNode(node)
        if node.freq not in self.freq_map:
            self.freq_map[node.freq] = DLLNode(0, 0)
        self.addToHead(node)

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            result = node.val
            self.increaseFrequency(node)
            print('Got the value: {} for the key: {} and frequency: {}'.format(result, key, node.freq))
            return result
        print('Did not get any value for the key: {}'.format(key))
        return -1

    def set(self, key, value):
        print('Going to set the (key, value): ({}, {})'.format(key, value))
        if key in self.map:
            node = self.map[key]
            node.val = value
            self.increaseFrequency(node)
        else:
            # Create a new node
            node = DLLNode(key, value)
            self.map[key] = node
            if len(self.map) > self.capacity:
                # Remove the least frequently used item
                while self.min_freq not in self.freq_map or self.freq_map[self.min_freq].next == self.tail:
                    self.min_freq += 1
                to_remove = self.freq_map[self.min_freq].next
                del self.map[to_remove.key]
                self.deleteNode(to_remove)
            self.min_freq = 1
            if self.min_freq not in self.freq_map:
                self.freq_map[self.min_freq] = DLLNode(0, 0)
            self.addToHead(node)
