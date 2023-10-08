class DLLNode:
    def __init__(self, key, val):
        self.val = val
        self.key = key
        self.prev = None
        self.next = None

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
            print('Got the value : {} for the key: {}'.format(result, key))
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

    
