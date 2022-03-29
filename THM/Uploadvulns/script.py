from itertools import product
###wordlist given in challenge hints, the script is just faster than logging in and downlloading

ls = [chr(i) for i in range(65,91)]
f= open("wl.txt", "w")
for p in product(ls, repeat=3):
    f.write("".join(p) + '\n')
f.close()
