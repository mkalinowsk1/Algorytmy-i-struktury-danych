import random
import string

file = open("randomS.txt", "w+")
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


for i in range(100):
    file.write(get_random_string(random.randint(1, 25))+"\n")


file.close()