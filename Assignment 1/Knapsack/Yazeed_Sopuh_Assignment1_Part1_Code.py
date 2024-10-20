import re
import timeit


class BST:
    def __init__(self):
        self.root = self.Node([])
        
    class Node:
        def __init__(self, value=[]):
            self.value = value
            self.left = None
            self.right = None


    def get_leaf_nodes(self,node):
        leaf_nodes = []
        if node:
            if node.left is None and node.right is None:
                leaf_nodes.append(node)
            else:
                leaf_nodes.extend(self.get_leaf_nodes(node.left))
                leaf_nodes.extend(self.get_leaf_nodes(node.right))
        return leaf_nodes

    def insert(self, value):
        if self.root.left is None and self.root.right is None:
            self.add(self.root, value)
        else:
            leaf_nodes = self.get_leaf_nodes(bst.root)
            for root in leaf_nodes:
                self.add(root, value)

    def add(self, root, value):
        # Same as parent
        right_arr = root.value[:]
        root.right = self.Node(right_arr)
        
        # adds the new item
        left_arr = root.value[:]
        left_arr.append(value)
        root.left = self.Node(left_arr)
            
    def print_tree(self,node, level=0):
        if node:
            print("  " * level + str(node.value) + ":")
            self.print_tree(node.left, level + 1)
            self.print_tree(node.right, level + 1)

# Extract the items from the text file
file = open('Assignment 1 knapsack.txt', 'r')
items = file.readlines()

# Removing elements that are not part of the items array
del items[0:7]
del items[-2:]

# Inserting items into a binary search tree
bst = BST()

for item in items:
    arr = re.findall(r'\d+', item)
    bst.insert([int(arr[1]), int(arr[2]), int(arr[0])])


def bfs(root):
    if root is None:
        return
    
    bw_solution = [0, 0]
    node_solution = bst.root

    queue = []
    queue.append(root)

    while len(queue) > 0: 
        node = queue.pop(0) 

        # Choosing best item
        benefits = 0
        weights = 0

        for item in node.value:
            benefits += item[0]
            weights += item[1]

        if weights <= 420:
            if benefits >= bw_solution[0] and len(node.value) >= len(node_solution.value):
                bw_solution = [benefits, weights]
                node_solution = node

        # Choosing best item

        if node.right is not None:
            queue.append(node.right)

        if node.left is not None:
            queue.append(node.left)


    return bw_solution, node_solution.value


def dfs(root):
    if root is None:
        return

    stack = []
    node = root

    bw_solution = [0, 0]
    node_solution = bst.root

    while stack or node:
        
        if node:
            stack.append(node)
            node = node.left
            
        else:
            node = stack.pop()


            # Choosing best item
            benefits = 0
            weights = 0

            for item in node.value:
                benefits += item[0]
                weights += item[1]

            if weights <= 420:
                if benefits >= bw_solution[0] and len(node.value) >= len(node_solution.value):
                    bw_solution = [benefits, weights]
                    node_solution = node
            # Choosing best item
            
            node = node.right

    return bw_solution, node_solution.value


# Driver Code
print("BFS: ", bfs(bst.root))
time_taken = timeit.timeit(lambda: bfs(bst.root), number=100)
print("Execution Time: ", time_taken)

print("DFS: ", dfs(bst.root))
time_taken = timeit.timeit(lambda: dfs(bst.root), number=100)
print("Execution Time: ", time_taken)
