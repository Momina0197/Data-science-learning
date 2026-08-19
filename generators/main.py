def number(n):
    for i in range(n):
        yield i

for i in number(5):
    print(i)

