so_dien = int(input('Số điện đã dùng của tháng này là: '))

gia_b1 = 1984   #giá điện bậc 1 theo quy ước của nhà nước (tính theo số điện dưới 50)
gia_b2 = 2050   #giá điện bậc 2 (tính theo số điện từ 51-100)
gia_b3 = 2380   #giá điện bậc 3 (từ 101-200)
gia_b4 = 2998   #giá điện bậc 4 (từ 201-300)
gia_b5 = 3350   #giá điện bậc 5 (từ 301-400)
gia_b6 = 3460   #giá điện bậc 6 (trên 400)

note = 'tiền điện tháng này của bạn là: '
note_1 = ' VNĐ'

if so_dien <= 50:       #50 là số điện cao nhất của bậc 1
  tong_b1 = str(so_dien * gia_b1)    #đơn vị tính VNĐ.
  print(note + tong_b1 + note_1)

elif so_dien <= 100:    #100 là số điện cao nhất của bâc 2
  tong_b2 = str(50 * gia_b1 + (so_dien - 50)*gia_b2)   #Đơn vị tính VNĐ.
  print(note + tong_b2 + note_1)

elif so_dien <= 200:    #200 là số điện cao nhất của bậc 3
  tong_b3 = str(50 * gia_b1 + (so_dien - 50)*gia_b2 + (so_dien - 100)*gia_b3)
  print(note + tong_b3 + note_1)

elif so_dien <= 300:    #300 là số điện cao nhất của bậc 4

  tong_b4 = str(50 * gia_b1 + (so_dien - 50)*gia_b2 + (so_dien - 100)*gia_b3 + (so_dien - 200)*gia_b4)
  print(note + tong_b4 + note_1)

elif so_dien <= 400:    #400 là số điện cao nhất của bậc 5
  tong_b5 = str(50 * gia_b1 + (so_dien - 50)*gia_b2 + (so_dien - 100)*gia_b3 + (so_dien - 200)*gia_b4 + (so_dien - 300)*gia_b5)
  print(note + tong_b5 + note_1)

else:                   #trên 400 là bậc 6
  tong_b6 = str(50 * gia_b1 + (so_dien - 50)*gia_b2 + (so_dien - 100)*gia_b3 + (so_dien - 200)*gia_b4 + (so_dien - 300)*gia_b5 + (so_dien - 400)*gia_b6)
  print(note + tong_b6 + note_1)
