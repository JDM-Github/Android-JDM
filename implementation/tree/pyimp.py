class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        if not self.root:
            self.root = Node(val)
            return
        
        q = [self.root]
        while q:
            node = q.pop(0)
            if not node.left:
                node.left = Node(val)
                return
            elif not node.right:
                node.right = Node(val)
                return
            else:
                q.append(node.left)
                q.append(node.right)
                
    def print_tree(self):
        if not self.root:
            return
        
        q = [self.root]
        while q:
            node = q.pop(0)
            print(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
