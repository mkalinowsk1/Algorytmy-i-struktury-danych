class Node:
	def __init__(self, data, color="red"):
		self.data = data
		self.color = color
		self.left = None
		self.right = None
		self.parent = None
		

class RBTree:
	def __init__(self):
		self.NULL_NODE = Node(None, color="black")
		self.NULL_NODE.left = None
		self.NULL_NODE.right = None
		self.root = self.NULL_NODE
		
	def insert(self, data):
		new_node = Node(data)
		new_node.left = self.NULL_NODE
		new_node.right = self.NULL_NODE
		new_node.parent = None
		new_node.color = "red"

		if self.root == self.NULL_NODE:  
			self.root = new_node
			self.root.color = "black"
			return

		parent = None
		current = self.root
		while current != self.NULL_NODE:
			parent = current
			if new_node.data < current.data:
				current = current.left
			else:
				current = current.right

		new_node.parent = parent
		if parent is None:
			self.root = new_node
		elif new_node.data < parent.data:
			parent.left = new_node
		else:
			parent.right = new_node
		self.fix_insert(new_node)

	def fix_insert(self, node):
		while node.parent is not None and node.parent.color == "red":
			#print("Fixing insert with node:", node.data)
			if node.parent == node.parent.parent.right:
				uncle = node.parent.parent.left
				#print("Uncle:", uncle.data)
				if uncle.color == "red":
					#print("Case 1: Uncle is red")
					node.parent.color = "black"
					uncle.color = "black"
					node.parent.parent.color = "red"
					node = node.parent.parent
				else:
					if node == node.parent.left:
						#print("Case 2: Node is left child")
						node = node.parent
						self.right_rotate(node)
					#print("Case 3: Node is right child")
					node.parent.color = "black"
					node.parent.parent.color = "red"
					self.left_rotate(node.parent.parent)
			else:
				uncle = node.parent.parent.right
				#print("Uncle:", uncle.data)
				if uncle.color == "red":
					#print("Case 1: Uncle is red")
					node.parent.color = "black"
					uncle.color = "black"
					node.parent.parent.color = "red"
					node = node.parent.parent
				else:
					if node == node.parent.right:
						#print("Case 2: Node is right child")
						node = node.parent
						self.left_rotate(node)
					#print("Case 3: Node is left child")
					node.parent.color = "black"
					node.parent.parent.color = "red"
					self.right_rotate(node.parent.parent)
			
			if node.parent is None:
				break
		self.root.color = "black"
			
		
		

	def left_rotate(self, node):
		right_child = node.right
		node.right = right_child.left
		if right_child.left != self.NULL_NODE:
			right_child.left.parent = node
		right_child.parent = node.parent
		if node.parent is None:
			self.root = right_child
		elif node == node.parent.left:
			node.parent.left = right_child
		else:
			node.parent.right = right_child
		right_child.left = node
		node.parent = right_child

	def right_rotate(self, node):
		left_child = node.left
		node.left = left_child.right
		if left_child.right != self.NULL_NODE:
			left_child.right.parent = node
		left_child.parent = node.parent
		if node.parent is None:
			self.root = left_child
		elif node == node.parent.right:
			node.parent.right = left_child
		else:
			node.parent.left = left_child
		left_child.right = node
		node.parent = left_child

def inorder_print(root, level):
	if root:
		inorder_print(root.right, level + 1)

		for _ in range(level):
			print("--", end="")
		
		print(f"{root.data}({root.color})")

		inorder_print(root.left, level + 1)

def print_tree(root):
	print("Drukowanie drzewa: ")
	inorder_print(root, 0)
	print()

	

if __name__ == "__main__":
	rb_tree = RBTree()
	rb_tree.insert(10)
	rb_tree.insert(20)
	rb_tree.insert(30)
	rb_tree.insert(15)
	rb_tree.insert(25)
	print_tree(rb_tree.root)
	