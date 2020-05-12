# Given integer positive number n. 
# Write a function that returns all integer powers of two, not exceeding n, in ascending order.

def powers_of_two(n):
    i = 0
    a = []
    while 2**i <= n:
        a.append(2**i)
        i = i + 1
    return a

print(powers_of_two(50))
#[1, 2, 4, 8, 16, 32]
