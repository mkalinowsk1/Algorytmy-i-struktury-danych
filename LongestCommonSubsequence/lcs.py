import random
import string

x = "aabca"
y = "cabba"

def print_lcs(x, b, i, j):
    if i==0 or j==0:
        return
    if b[i][j] == "\\":
        print_lcs(x, b, i-1, j-1)
        print(x[i-1], end='')
    elif b[i][j] == "|":
        print_lcs(x,b,i-1,j)
    else:
        print_lcs(x,b,i,j-1)

def lcs(x, y):
    m = len(x)
    n = len(y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[''] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = "\\"
            else:
                if c[i - 1][j] >= c[i][j - 1]:
                    c[i][j] = c[i - 1][j]
                    b[i][j] = "|"
                else:
                    c[i][j] = c[i][j - 1]
                    b[i][j] = "-"

    print_lcs(x,b,m,n)
    return b, c

def lcs_length(x, y):
    m = len(x)
    n = len(y)
    
    c = [[0] * (n + 1) for _ in range(2)]

    for i in range(1, m + 1):
        row_index = i % 2
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[row_index][j] = c[1 - row_index][j - 1] + 1
            else:
                c[row_index][j] = max(c[1 - row_index][j], c[row_index][j - 1])

    return c[m % 2][n]

def generate_sequence(n, k):
    return ''.join(random.choices(string.ascii_lowercase[:k], k=n))

def Chvatal_Sankoff(n, k):
    seq1 = generate_sequence(n, k)
    seq2 = generate_sequence(n, k)
    length = lcs_length(seq1, seq2)
    print(f"wyliczona długość {length} oraz iloraz: {length/n} dla ciągów długości {n} zbudowanych z {k} liter.")

def main():
    lcs(x, y)
    print("\nDługość najdłuższego wspólnego podciągu (NWP):", lcs_length(x, y)) 
    
    Chvatal_Sankoff(100, 2)
    Chvatal_Sankoff(500, 2)
    Chvatal_Sankoff(1000, 2)
    Chvatal_Sankoff(100, 4)
    Chvatal_Sankoff(500, 4)
    Chvatal_Sankoff(1000, 4)
    Chvatal_Sankoff(100, 8)
    Chvatal_Sankoff(500, 8)
    Chvatal_Sankoff(1000, 8)
    Chvatal_Sankoff(100, 16)
    Chvatal_Sankoff(500, 16)
    Chvatal_Sankoff(1000, 16)

if __name__ == "__main__":
    main()
