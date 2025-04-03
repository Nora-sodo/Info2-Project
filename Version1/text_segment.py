from segment import *

n1 = Node ('Nora', 1, 1)
n2 = Node ('Laia', 3, 4)
n3 = Node ('Maroua', 7, 3)

s1 = Segment ('1',n1, n2)
s2 = Segment ('2',n2, n3)

print(s1.cost)
print(s2.cost)