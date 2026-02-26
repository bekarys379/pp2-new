N=5
print("First task:")
def square(N):
    for N in range(N):
        yield pow(N, 2)

g=square(N)
print(next(g))
print(next(g))
print(next(g))
print(next(g))

print()
print("second task:")
n=10
def even(n):
    for i in range(0, n):
        if i%2==0:
            yield i


it=even(n)
res=",".join(map(str, even(n)))
print(res)


print()
print("Third task:")

x=40
def cnbd(x):
    for i in range(0, x+1):
        if i%3==0 and i%4==0:
            yield i

ares=map(str, cnbd(x))
print(*ares)

print()
print("Fourth task:")
a=10
b=23
def squares(a, b):
    for i in range(a, b+1):
        yield i*i


for value in squares(a, b):
    print(value)

print()
print("5th task")
a=12
def ret(a):
    for i in range(0, a):
        yield i

for gen in ret(a):

    print(gen)
