import random
from collections import Counter
import heapq

# file = open("numbers.txt", "a")

#numbers = [1, 2, 3, 4, 5, 6, 7]

# probabilities = [0.35, 0.1, 0.15, 0.1, 0.05, 0.15 , 0.1]

# random_numbers = random.choices(numbers, weights=probabilities, k=10000)

# for i in random_numbers:
# 	file.write(str(i))

numbers = [1, 2, 3, 4, 5, 6, 7]

class Node:
	def __init__(self, freq, number, left=None, right=None):
		self.freq = freq
		self.number = number
		self.left = left
		self.right = right
		self.huff = ''

	# fancy less than method
	def __lt__(self, nxt):
		return self.freq < nxt.freq
	

def print_nodes(node,lengths, val='', ):
	newVal = val + node.huff
	if node.left:
		print_nodes(node.left, lengths, newVal)
	if node.right:
		print_nodes(node.right, lengths, newVal)

	if not node.left and not node.right:
		#print(f"{node.number} dlugosc kodu: {len(newVal)}")
		lengths[node.number] = len(newVal)
	return dict(sorted(lengths.items()))

def huffman_encode_single(nodes, freq):
	for x in range(len(numbers)):
		heapq.heappush(nodes, Node(freq[x], numbers[x]))

	while len(nodes) > 1:
		left = heapq.heappop(nodes)
		right = heapq.heappop(nodes)

		left.huff = '0'
		right.huff = '1'

		newNode = Node(left.freq + right.freq, left.number + right.number, left, right)
		heapq.heappush(nodes, newNode)

def huffman_encode_pairs(nodes):
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        left.huff = '0'
        right.huff = '1'
        new_number = left.number + right.number
        new_node = Node(left.freq + right.freq, new_number, left, right)
        heapq.heappush(nodes, new_node)

def len_of_file_pairs(freq, lengths):
    total_len = 0
    for chars, f in freq.items():
        total_len += f * lengths[chars]
    return total_len

def len_of_file(freq, lengths):
	total_len = 0
	for i in range(len(freq)):
		total_len += freq[i]*lengths[i+1]
	return total_len

def main():
	file = open("numbers.txt", "r")
	text = file.read().strip()
	file.close()

	#single characters
#########################################
	print("wyniki dla pojedynczych cyfr")
	nums = [int(digit) for digit in text]
	c = Counter(nums)
	freq = [c[num] for num in numbers]
	nodes = []
	
	huffman_encode_single(nodes, freq)
	lengths = print_nodes(nodes[0], lengths = {})
	print(lengths)
	print("Dlugosc zakodowanego pliku: ",len_of_file(freq, lengths))
	print()
	
#########################################
	#pairs of characters
#########################################
	print("wyniki dla par cyfr")
	pairs = [int(text[i:i+2]) for i in range(0, len(text), 2)]
	c1 = Counter(pairs)
	freq1 = {pair: count for pair, count in c1.items()}
	nodes1 = []
	for pair, count in freq1.items():
		heapq.heappush(nodes1, Node(count, pair))

	huffman_encode_pairs(nodes1)
	lengths1 = print_nodes(nodes1[0], lengths = {})
	print(lengths1)
	print("Dlugosc zakodowanego pliku: ",len_of_file_pairs(freq1, lengths1))
	
if __name__ == "__main__":
	main()
