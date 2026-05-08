from math import acos, sqrt

a = int(input('chiều dài cạnh a là: '))
b = int(input('chiêu dài cạnh b là: '))
c = int(input('chiều dài cạnh c là: '))
P = (a + b + c)
p = (a + b + c) / 2
S = sqrt(p * (p - a) * (p - b) * (p - c))
h_a = (2 * S) / a
h_b = (2 * S) / b
h_c = (2 * S) / c
m_a = 0.5 * sqrt(2*b**2 + 2*c**2 - a**2)
m_b = 0.5 * sqrt(2*a**2 + 2*c**2 - b**2)
m_c = 0.5 * sqrt(2*a**2 + 2*b**2 - c**2)
A = acos((b**2 + c**2 - a**2) / (2 * b * c))
B = acos((a**2 + c**2 - b**2) / (2 * a * c))
C = acos((a**2 + b**2 - c**2) / (2 * a * b))
print('chu vi ' + str(P))
print('nữa chu vi ' + str(p))
print('diện tích công thức heron ' + str(S))
print('đường cao a ' + str(h_a))
print('đường cao b ' + str(h_b))
print('đường cao c ' + str(h_c))
print('trung tuyến m_a ' + str(m_a))
print('trung tuyến m_b ' + str(m_b))
print('trung tuyến m_c ' + str(m_c))
print('góc A ' + str(A))
print('góc B ' + str(B))
print('góc C ' + str(C))