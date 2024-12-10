class Node:
    def __init__(self, key, count=1):
        self.left = None
        self.right = None
        self.key = key
        self.count = count


def search(root, key):
    while(root != None and root.key != key):
        if key < root.key:
            root = root.left
        else:
            root = root.right

    return root

def insert(node, key):
    if node is None:
        return Node(key)
    
    if key == node.key:
        node.count += 1
    
    if key < node.key:
        node.left = insert(node.left, key)

    elif key > node.key:
        node.right = insert(node.right, key)

    return node

def minValueNode(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete(root, key):
    if root is None:
        return root

    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.count > 1:
            root.count -= 1
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            root.key = minValueNode(root.right).key
            root.right = delete(root.right, root.key)

    return root

def print_tree(root):
    print("Drukowanie drzewa w rosnącej kolejności kluczy:")
    inorder_print(root, 0)
    print()

def inorder_print(root, level):
    if root:
        inorder_print(root.left, level + 1)

        for i in range(level):
            print("--", end="")
        
        print(f"{root.key}({root.count}) ")

        inorder_print(root.right, level + 1)

def main():
    root = Node(100)
    insert(root, 30)
    insert(root, 20)
    insert(root, 40)
    insert(root, 70)
    insert(root, 60)
    insert(root, 80)
    insert(root, 40)
    insert(root, 70)

    print_tree(root)
    key = 80
    if search(root, key) is None:
        print(key, "nie znaleziono")
    else:
        print(key, "znaleziono")

    root = delete(root, 100)

    if search(root, key) is None:
        print(key, "nie znaleziono")
    else:
        print(key, "znaleziono")

    root = delete(root, 70)
    print_tree(root)
if __name__ == "__main__":
    main()