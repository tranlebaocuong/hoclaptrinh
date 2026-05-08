def tinh_hoa_don(gia, so_luong, giam_gia=0, thue=0.1):       #giảm=0, thuế=10%, 2 giá trị không thay đổi

    chua_tinh_tien = gia * so_luong     #công thức tính tiền trước thanh toán

    sau_giam_gia = chua_tinh_tien - giam_gia    #công thức tính sau giảm giá

    tien_thue = sau_giam_gia * thue    #công thức quy đổi thuế sau giảm giá

    tong_thanh_toan = sau_giam_gia + tien_thue  #công thức tính tổng tiền sau thanh toán

    print('tong so tien can thanh toan la: ' + str(tong_thanh_toan))
tinh_hoa_don(10000, 2)
tinh_hoa_don(250000, 10)