import time

with open("wzorzecA.txt") as pattern_in:
	patternA = pattern_in.read().strip()

with open("tekstA.txt") as text_in:
	textA = text_in.read().strip()

with open("wzorzecB.txt") as pattern_in:
	patternB = pattern_in.read().strip()

with open("tekstB.txt") as text_in:
	textB = text_in.read().strip()

print()
def naive(P, T):
	m = len(P)
	n = len(T)

	for s in range(n - m + 1):
		match = True
		for i in range(m):
			if T[s + i] != P[i]:
				match = False
				break
		if match:
			print(f"Wzorzec znaleziony na pozycji {s}")
		


def rabin_karp(P, T, d, q):
	m = len(P)
	n = len(T)
	
	h = 1

	p = 0
	t = 0

	for i in range(m-1):
		h = (h * d) % q
	
	for i in range(m):
		p = (d * p + ord(P[i])) % q
		t = (d * t + ord(T[i])) % q
	
	for s in range (n - m + 1):
		if p == t:
			match = True
			for i in range(m):
				if T[s + i] != P[i]:
					match = False
					break
			if match:
				print(f"Wzorzec znaleziony na pozycji {s}")
		
		if s < n - m:
			t = (d * (t - ord(T[s]) * h) + ord(T[s + m])) % q

			if t < 0:
				t = t + q

def prefix(P):
	m = len(P)
	pi = [0] * m
	k = 0
	for q in range(1, m):
		while k > 0 and P[k] != P[q]:
			k = pi[k - 1]
		if P[k] == P[q]:
			k += 1
		pi[q] = k
	
	return pi

def kmp(P, T):
	n = len(T)
	m = len(P)
	pi = prefix(P)
	q = 0
	for i in range(n):
		while q > 0 and P[q] != T[i]:
			q = pi[q - 1]
		if P[q] == T[i]:
			q += 1
		if q == m:
			print(f"Wzorzec znaleziony na pozycji {i - m + 1}")
			q = pi[q - 1]


def main():
	d = 128
	q = 27077

	test_text = "ABABDABACDABABCABAB"
	test_pattern = "ABABCABAB"

	print("Wyniki dla malych danych: ")
	naive(test_pattern, test_text)
	rabin_karp(test_pattern, test_text, d, q)
	kmp(test_pattern, test_text)
	print()

	print("Wyniki dla algorytmu naiwnego: ")
	start_time = time.time()
	naive(patternA, textA)
	end_time = time.time()
	print("Czas wykonania: ", end_time - start_time, "sekundy")
	print()

	print("Wyniki dla algorytmu Rabina-Karpa: ")
	start_time = time.time()
	rabin_karp(patternA, textA, d, q)
	end_time = time.time()
	print("Czas wykonania: ", end_time - start_time, "sekundy")
	print()

	print("Wyniki dla algorytmu Knutha-Morrisa-Pratta: ")
	start_time = time.time()
	kmp(patternA, textA)
	end_time = time.time()
	print("Czas wykonania: ", end_time - start_time, "sekundy")

if __name__ == "__main__":
	main()