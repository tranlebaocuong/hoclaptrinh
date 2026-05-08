so_du = 1000000   #đơn vị tính VNĐ
so_tien_rut = int(input('nhập số tiền bạn muốn rút, số tiền rút phải lớn hơn 50000: '))   #hỏi về câu lệnh số tiền rút > 50.000, và gán dữ liệu float bị lỗi.
so_du_con_lai = so_du - so_tien_rut

A = 'giao dịch thành công, vui lòng đợi... '
B = 'Số dư không đủ vui lòng kiểm tra và thực hiện lại giao dịch! '

if so_tien_rut <= so_du:
  print(A + 'tài khoản của bạn hiện còn ' + str(so_du_con_lai))
else:
  print(B)