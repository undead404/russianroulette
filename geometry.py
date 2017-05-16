import math

A = (-3, 2, 4)
Y1 = (0, -10, 0)
Y2 = (0, 14, 0)


def get_distance(A, B):
    return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 + (A[2] - B[2]) ** 2)


print(get_distance(A, Y1))
print(get_distance(A, Y2))
