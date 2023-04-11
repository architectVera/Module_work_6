# b = lambda e, i : {e: i}
# print(b(1,2)[1])

# c = lambda a, b: a+b
# print(c(1,2,3))

d = {"p", "i", "p"}
a=0

for i in d:
    if i[0] == "p":
        a+=1
print(a)