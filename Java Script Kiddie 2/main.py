# PNG header bytes: 137 80 78 71 13 10 26 10
# picoCTF{90d440ad6523968d5000e122a085b68c}
from pwn import *
import itertools
LEN = 16

numbers = '196 230 44 71 23 175 179 79 159 0 184 27 165 104 179 0 126 171 236 114 68 242 188 127 61 0 111 58 0 159 211 82 246 163 58 2 13 121 114 216 21 0 163 0 73 154 241 108 27 252 69 95 0 82 66 198 247 120 198 13 0 188 0 227 0 110 78 74 112 228 26 96 79 200 112 0 155 0 0 82 137 60 1 238 141 165 1 10 130 54 0 237 155 0 68 24 0 127 0 140 14 136 68 114 0 111 0 228 253 72 95 39 164 73 70 75 8 174 94 65 1 222 0 11 81 192 138 120 48 80 62 239 233 10 96 202 84 64 156 65 141 77 57 245 223 0 56 85 26 0 139 45 55 0 81 227 215 13 105 29 210 0 239 128 85 73 183 16 13 254 53 144 50 196 213 139 89 16 197 169 31 13 76 112 75 87 241 43 148 86 222 231 227 192 48 126 45 48 117 229 48 194 120 62 199 55 19 175 24 205 85 223 64 74 87 6 7 245 134 241 140 134 22 95 105 148 77 191 6 215 197 235 25 115 112 122 127 132 117 188 224 255 209 88 218 45 76 196 49 167 96 255 96 12 237 67 9 127 10 81 196 85 77 23 62 131 143 63 126 240 45 117 215 84 213 5 62 249 167 228 5 233 185 74 191 127 206 79 151 231 227 25 2 206 34 190 199 52 24 152 201 124 129 55 155 255 182 37 183 163 171 34 137 248 226 254 230 111 32 78 104 203 91 88 169 252 227 199 210 151 250 99 175 207 12 196 139 115 26 124 159 85 174 218 248 207 248 100 170 251 205 231 234 126 63 110 124 79 117 52 251 116 55 131 163 136 124 19 253 1 91 63 235 159 82 41 68 231 170 90 30 116 210 63 213 128 114 64 12 232 227 103 200 87 18 215 52 37 187 18 134 143 91 51 2 2 131 31 178 123 49 57 244 174 24 154 82 198 113 49 232 185 95 8 222 235 90 115 116 252 100 174 8 226 16 21 245 242 53 85 147 238 170 33 65 116 184 150 130 108 172 244 96 107 130 174 202 242 250 123 82 43 255 255 126 58 199 26 94 229 127 136 138 42 144 105 221 24 210 249 164 45 219 215 128 230 111 16 94 250 144 135 127 169 67 239 164 87 38 33 31 184 213 157 159 175 171 7 50 53 60 234 133 186 37 102 207 20 212 87 124 58 107 127 119 153 183 82 150 69 180 189 186 24 153 246 181 213 101 230 223 100 46 223 235 73 197 3 117 251 237 252 223 51 249 22 248 99 253 48 232 145 104 253 170 163 113 74 110 118 141 179 245 118 149 247 12 57 190 248 0 107 98 79 243 122 106 19 151 85 249 28 63 214 222 248 73 239 47 77 38 102 149 76 17 42 201 12 239 52 33 170 47 144 184 180 85 46 142 38 199 86 127 223 239 241 203 127 99 26 139 242 164 224 135 82 98 24 206 9 235 107 223 254 249 79 83 228 126 71 43 69 185 197 153 99 111 79 199 255 235 244 127 95 34 221 17 93 43 217 169 198 63 243 231 78 70 50 53 43 254 115 127 169 111 208 165 0'
numbers = map(int, numbers.split(' '))
l = len(numbers)

def shift(index, times,old):
  new_arr = old[:]
  for i in range(l//LEN):
    new_arr[(i)*LEN+index] = old[((i+times)*LEN+index)%l]
  return new_arr

header = '89504e470d0a1a0a0000000d49484452'
header = map(ord,header.decode('hex'))
print header

d = {}
for i in range(LEN):
  temp = numbers[:]
  for j in range(l//LEN):
    temp = shift(i, 1, temp)
    if temp[i] == header[i]:
      if i in d:
        d[i].append(j+1)
      else:
        d[i] = [j+1]
  if i not in d:
    print 'error'
print d

arr = []
for i in range(LEN):
  arr.append(d[i])
print arr

counter = 0
for i in itertools.product(*arr):
  print i
  key = i
  temp = numbers[:]
  for i, each in enumerate(key):
    temp = shift(i, each, temp)
  temp = ''.join(map(chr, temp))
  with open('{}.png'.format(counter), 'wb') as f:
    f.write(temp)
  print '.',
  counter+=1
# counter = 0

# for i12 in [1,3]:
#   for i10 in [1,2,3,4]:
#     for i9 in [2,3,4,5]:
#       for i8 in [1,44]:

#         key = [(12, i12), (10, i10), (9, i9), (8, i8), (0, 7), (1, 4), (2, 1), (3, 4), (4, 9), (5, 7), (6, 4), (7, 9), (11, 7), (13, 5), (14, 4), (15, 4)]
#         temp = numbers[:]
#         for i, each in key:
#           temp = shift(i, each, temp)
#         temp = ''.join(map(chr, temp))
#         with open('{}.png'.format(counter), 'wb') as f:
#           f.write(temp)
#         print '.',
#         counter+=1
# for i, each in enumerate([137, 80, 78, 71, 13, 10, 26, 10]):
#   assert numbers[i] == each

# assert numbers[0] == 137
# assert numbers[1] == 80
# assert numbers[2] == 78

# for i in range(45):
#   numbers = shift(8, 1)
#   if numbers[8] == 0:
#     print i+1

# 12: [1,3]
# 10: [1,2,3,4]
# 9: [2,3,4,5]
# 8: [1,44]
