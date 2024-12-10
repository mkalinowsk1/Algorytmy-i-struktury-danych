class Node:
	def __init__(self, val):
		self.val = val
		self.next = None
		self.prev = None

class DoublyLinkedList:
	def __init__(self):
		self.sentinel = Node(-1)
		self.sentinel.next = self.sentinel
		self.sentinel.prev = self.sentinel
		self.size = 0

	def wstaw(self, val):
		node = Node(val)
		node.next = self.sentinel
		node.prev = self.sentinel.prev
		self.sentinel.prev.next = node
		self.sentinel.prev = node
		self.size += 1

	def usun(self, val):
		#szukanie elementu do usuniecia
		node_to_delete = self.szukaj(val)
		#usuwanie elementu
		if node_to_delete:
			node_to_delete.prev.next = node_to_delete.next
			node_to_delete.next.prev = node_to_delete.prev
			node_to_delete.prev = None
			node_to_delete.next = None
			self.size -= 1
		else:
			print("Nie ma takiego elementu")

	def szukaj(self, val):
		curr = self.sentinel.next
		while curr != self.sentinel:
			if curr.val == val:
				return curr  
			curr = curr.next
		return None
	
	def bezpowtorzeń(self):
		unique_list = DoublyLinkedList()
		seen_words = set()

		current = self.sentinel.next
		while current != self.sentinel:
			if current.val not in seen_words:
				unique_list.wstaw(current.val)
				seen_words.add(current.val)
			current = current.next

		return unique_list
	
	def scal(L1, L2):

		L3 = DoublyLinkedList()

		# dodanie elementów 1 listy do nowej listy
		current = L1.sentinel.next
		while current != L1.sentinel:
			L3.wstaw(current.val)
			current = current.next

		# dodanie elementów 2 listy do nowej listy

		current = L2.sentinel.next
		while current != L2.sentinel:
			L3.wstaw(current.val)
			current = current.next

		# usuwanie list 1 i 2.

		L1.sentinel.next = L1.sentinel
		L1.sentinel.prev = L1.sentinel
		L2.sentinel.next = L2.sentinel
		L2.sentinel.prev = L2.sentinel

		return L3
	
	
	# wyświetlenie elemntów listy
	def drukuj(self):
		curr = self.sentinel.next
		while curr != self.sentinel:
			print(curr.val, end=" ")
			curr = curr.next
		print()


# wstawienie elementów do 1 listy
lista1 = DoublyLinkedList()
lista1.wstaw("slowo1")
lista1.wstaw("slowo2")
lista1.wstaw("slowo1")

# wstawienie elementów do 2 listy
lista2 = DoublyLinkedList()
lista2.wstaw("slowo4")
lista2.wstaw("slowo2")

# szukanie elementu na liście
print("szukanie slowo1 na liście")
if lista1.szukaj("slowo1"):
	print("znaleziono")
else:
	print("nie znaleziono")

# Scalenie list 1 i 2
print("scalona lista: ")
lista3 = lista1.scal(lista2)
lista3.drukuj()
lista4 = lista3.bezpowtorzeń()
lista4.drukuj()
# usuniecie elementu z listy
lista3.usun("slowo4")
print("Lista po usunięciu elementu slowo4")
lista3.drukuj()

