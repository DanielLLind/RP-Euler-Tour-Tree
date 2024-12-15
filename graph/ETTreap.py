import random


class Node:
    def __init__(self, key, priority,value = 0):
        self.key = key
        self.priority = priority
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class Treap:
    def __init__(self):
        self.root = None
        self.anchor = 0
        self.size = 0
    
    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root
    

    def _insert(self, node, key, priority, value):
        if node is None:
            return Node(key, priority, value)

        if ((key + self.anchor) % self.size) < ((node.key + self.anchor) % self.size):
            node.left = self._insert(node.left, key, priority, value)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, key, priority, value)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)

        return node

    def insert(self, key, prio, value = 0):
        priority = prio 
        self.size = self.size + 1

        self.root = self._insert(self.root, key, priority, value)
        print(self.validate(self.root))

    def printTree(self):
        result = ''
        result += str(self.root.key) + ' '
        result += self.printTreeR(self.root.left)
        result += self.printTreeR(self.root.right)
        return result

    def printTreeR(self, node):
        if node is None:
            return ""
        return str(node.key) + ' ' + self.printTreeR(node.left) + self.printTreeR(node.right)
    
    def printTreeArr(self):
        result = []
        self._printTreeArr(self.root,result)
        return result

    def _printTreeArr(self,node,nodes):
        if node is None:
            return
        nodes.append((node.key,node.value))
        if node.left:
            self._printTreeArr(node.left,nodes)
        if node.right:
            self._printTreeArr(node.right,nodes)

    def getEdges(self):
        edges = []
        self.collectEdges(self.root, edges)
        return edges

    def collectEdges(self, node, edges):
        if node is None:
            return
        if node.left:
            edges.append((node.key, node.left.key))
            self.collectEdges(node.left, edges)
        if node.right:
            edges.append((node.key, node.right.key))
            self.collectEdges(node.right, edges)      

    def getEdgesDi(self):
        edges = []
        self.getEdgesRec(self.root, edges)
        return edges
    
    def getEdgesRec(self, node, edges):
        if node is None:
            return
        if node.left:
            edges.append(((node.key,node.left.key),True))
            self.getEdgesRec(node.left,edges)
        if node.right:
            edges.append(((node.key,node.right.key),False))
            self.getEdgesRec(node.right,edges)


    def getRoot(self):
        return self.root
    
    def _split(self, node, key):
        if node is None:
            return None, None

        if key <= node.key:
            left, node.left = self._split(node.left, key)
            return left, node
        else:
            node.right, right = self._split(node.right, key)
            return node, right

    def split(self, key):
        left, right = self._split(self.root, key)
        left_tree = Treap()
        right_tree = Treap()
        left_tree.root = left
        right_tree.root = right
        return left_tree, right_tree
    
    def split2(self,key):
        prio = self.root.priority + 10000
        self.insert(key,prio,-1)
        left_tree = Treap()
        right_tree = Treap()
        left_tree.root = self.root.left
        right_tree.root = self.root.right
        self.size = self.size - 1
        left_tree.size = self.size
        right_tree.size = self.size
        left_tree.anchor = self.anchor
        right_tree.anchor = self.anchor
        print(self.validate(left_tree.root))
        print(self.validate(right_tree.root))
        return left_tree, right_tree
    
    def _join(self, T1, T2):
        if T1 is None:
            return T2
        if T2 is None:
            return T1

        if T1.priority > T2.priority:
            T1.right = self._join(T1.right, T2)
            return T1
        else:
            T2.left = self._join(T1, T2.left)
            return T2

    def join(self, t1, t2):
        t = Treap()
        t.root = self._join(t1.root, t2.root)
        t.size = t1.size
        t.anchor = t1.anchor
        print(self.validate(t.root))
        return t
    
    def _deleteLeaf(self,node,key):
        if node.key == key:
            return None
        if ((key + self.anchor) % self.size) < ((node.key + self.anchor) % self.size):
            node.left = self._deleteLeaf(node.left,key)
        elif ((key + self.anchor) % self.size) > ((node.key + self.anchor) % self.size):
            node.right = self._deleteLeaf(node.right,key)
        return node

    def deleteLeaf(self,key):
        self.root = self._deleteLeaf(self.root,key)

    def join2(self,t1,t2,key):
        if t1 is None:
            return t2
        if t2 is None:
            return t1
        t = Treap()
        node = Node(key,-1,-1)
        t.root = node
        t.root.left = t1.root
        t.root.right = t2.root
        t.size = t1.size
        t.anchor = t1.anchor
        #node = t.root
        node = t.root
        while (node.left or node.right):
            if not node.left:
                a = t._rotate_left(node)
                if a.priority > t.root.priority:
                    t.root = a
                #node = node.left
            elif not node.right:
                a = t._rotate_right(node)
                if a.priority > t.root.priority:
                    t.root = a
                #node = node.right
            elif node.left.priority > node.right.priority:
                a = t._rotate_right(node)
                if a.priority > t.root.priority:
                    t.root = a
                #node = node.right
            else:
                a = t._rotate_left(node)
                if a.priority > t.root.priority:
                    t.root = a
                #node = node.left

        t.deleteLeaf(key)
        return t
    
    def reRoot(self, newRoot):
        node = self.root
        while (node.left):
            node = node.left
        _, t = self.split2(node.key+0.5)
        self.root = t.root
        l, r = self.split2(newRoot-0.5)
        newT = self.join(r,l)
        node2 = newT.root
        self.size = self.size - 1
        while(node2.left):
            node2 = node2.left
        newT.anchor = self.size - node2.key + 1
        self.root = newT.root
        self.anchor = newT.anchor
        self.insert(node.key,random.randint(0,1000),node2.value) 

    def eulerSplit(self,key1,key2):
        t = Treap()
        t.root = self.root
        t.size = self.size
        t.anchor = self.anchor
        left, right = t.split2(key1)
        left2,right2 = right.split2(key2)

        #node = left.root
        #while(node.right):
        #    node = node.right
        #left3, _ = left.split2(node.key-0.5)
        
        #return self.join(left,right2), left2
        return right2, left2 #bandaid fix works because only removing one element from left2, need to make proper deletete lol

    #links a and b from t1 and t2, t2 is rooted at b, and the key represents the first occurence of a in t1
    def eulerLink(self,t1,t2,key): # this should work ?, still needs to add the new node inbetween
        l, r = t1.split2(key)
        newT = self.join(l,t2)

        node = r.root
        while (node.left):
            node = node.left
        #r.insert(node.key,random.randint(0,1000),r.root.value) #should probally be more like this...
        treeToReturn = self.join(newT,r)
        treeToReturn.insert(0,random.randint(0,1000),1) 

        return treeToReturn

    def validate(self,node): #validate the tree is a valid Treap
        valid = True
        if (node):
            if (node.left):
                if (node.left.priority > node.priority or 
                    ((node.left.key + self.anchor) % self.size) > ((node.key + self.anchor) % self.size)):
                    print("parent",node.key,"child",node.left.key)
                    print("left",node.left.priority, node.priority, node.left.key, self.anchor, self.size, node.key,(node.left.key + self.anchor) % self.size,(node.key + self.anchor) % self.size)
                    return False
                valid = self.validate(node.left)

            if (node.right):
                if (node.right.priority > node.priority or 
                    ((node.right.key + self.anchor) % self.size) < ((node.key + self.anchor) % self.size)):
                    print("parent",node.key,"child",node.right.key)
                    print("right",node.right.priority, node.priority, node.right.key, self.anchor, self.size, node.key,(node.right.key + self.anchor) % self.size,(node.key + self.anchor) % self.size)
                    return False
                valid = self.validate(node.right)
        return valid