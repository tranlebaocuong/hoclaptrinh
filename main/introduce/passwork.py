from getpass import getpass
passkey = 'Python123'
login = str(getpass('vui lòng nhập mật khẩu?: '))
A = ' Đăng nhập thành công, đang chuyển đến trang chủ... '
B = ' Mật khẩu không chính xác, vui lòng kiểm tra lại '
if login == passkey:
  print(A)
else:
  print(B)