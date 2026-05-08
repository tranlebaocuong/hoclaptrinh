# Lấy thông tin người dùng
print('''
Bạn xem thứ mấy?
    (2) Thứ 2
    (3) Thứ 3
    (4) Thứ 4
    (5) Thứ 5
    (6) Thứ 6
    (7) Thứ 7
    (8) Chủ nhật''')
thu = int(input('> '))

gio = int(input('Bạn xem lúc mấy giờ? '))

print('''
Bạn bao nhiêu tuổi?
    (1) Trẻ em
    (2) Học sinh/sinh viên
    (3) Người lớn
    (4) Người cao tuổi''')
tuoi = int(input('> '))



# Tính giá vé
# trong_tuan = (thu == 2 or thu == 4 or thu == 5)
trong_tuan = (thu in [2, 4, 5])
treem_hssv_caotuoi = (tuoi == 1 or tuoi == 2 or tuoi == 4)
gio_thap_diem = (gio < 10 or gio > 22)

if thu == 3:
    gia_ve = 45000
elif trong_tuan:
    if treem_hssv_caotuoi:
        gia_ve = 60000
    elif tuoi == 3 and gio_thap_diem:
        gia_ve = 60000
    else:
        gia_ve = 75000
else:
    if treem_hssv_caotuoi:
        gia_ve = 65000
    elif tuoi == 3 and gio_thap_diem:
        gia_ve = 65000
    else:
        gia_ve = 85000



# In giá vé
print('Giá vé là: ' + str(gia_ve))