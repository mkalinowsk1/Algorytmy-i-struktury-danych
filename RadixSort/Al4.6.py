with open("C:/Users/mical/Desktop/code/randomS.txt") as fin:
    lines = fin.read().strip().split()

output = open("output.txt","w")

Tablica = []

for line in lines:
    Tablica.append(line.lower())


def counting_sort(A, B, k, p):
# A - tablica do posortowania
# B - wynik sortowania
# k - zakres znaków
# p - pozycja według której sortuje napisy

    C = [0] * (k + 1)
    # C - pomocnicza tablica liczników
    for j in range(1, len(A) + 1):
        char = A[j - 1][p] if p < len(A[j - 1]) else 'a'
        C[ord(char) - ord('a')] += 1

    for i in range(1, k + 1):
        C[i] += C[i - 1]

    for j in range(len(A), 0, -1):
        char = A[j - 1][p] if p < len(A[j - 1]) else 'a'
        B[C[ord(char) - ord('a')] - 1] = A[j - 1]
        C[ord(char) - ord('a')] -= 1

def radix_sort(A, d, k):
    B = [0] * len(A)

    for j in range(d, 0, -1):
        counting_sort(A, B, k, j - 1)
        A = B.copy()

    return A

d = 25  # maksymalna długość napisu
k = 26  # liczba różnych znaków

s = ["synowa", "mama", "brat", "corka", "dziadek", "babcia", "syn", "bratowa", "ciocia", "dziecko"]
d1 = len(max(s))
result = radix_sort(Tablica, d, k)
for s in result:
    output.write(s + "\n")

output.close()