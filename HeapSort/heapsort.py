input = open("C:/Users/mical/Desktop/code/input.txt", "r")
A = []
for line in input:
	A.append(int(line))
#A - tablica
#n - rozmiar kopca

input.close()

def heapifyIter(Arr,n, i):
	while True:
		l = 2 * i + 1
		r = 2 * i + 2
		if l < n and Arr[l] > Arr[i]:
			largest = l
		else:
			largest = i
		if r < n and Arr[r] > Arr[largest]:
			largest = r
		if largest != i:
			Arr[i], Arr[largest] = Arr[largest], Arr[i]
			i = largest
		else:
			break

def heapifyRec(Arr, n, i):
	l = 2 * i + 1
	r = 2 * i + 2
	if l < n and Arr[l] > Arr[i]:
		largest = l
	else:
		largest = i
	if r < n and Arr[r] > Arr[largest]:
		largest = r
	if largest != i:
		Arr[i], Arr[largest] = Arr[largest], Arr[i]
		heapifyRec(Arr, n, largest)
 


def buildHeap(Arr):
	n = len(Arr)
	for i in range(n // 2 -1, -1, -1):
		heapifyIter(Arr, n, i)
		#heapifyRec(Arr, n, i)

def heapSort(Arr):
	buildHeap(Arr)

	for i in range(len(Arr) - 1, 0, -1):
		Arr[i], Arr[0] = Arr[0], Arr[i]
		heapifyIter(Arr, i, 0)
		#heapifyRec(Arr, i, 0)

heapSort(A)
output = open("output.txt", "a")
for i in range(len(A)):
	output.write(str(A[i])+"\n")
	
		
output.close()