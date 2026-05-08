
menu = {

    "tra_sua": {"name": "Trà sữa", "base_price": 25000},
    "ca_phe_sua": {"name": "Cà phê sữa", "base_price": 30000},
    "hong_tra": {"name": "Hồng trà", "base_price": 22000},
    "matcha_latte": {"name": "Matcha latte", "base_price": 35000},
    "tra_dao": {"name": "Trà đào", "base_price": 28000}
}

don = {}

# Viết code của bạn tại đây

#in menu 1 lần:
print('=== MENU ===')
for key, item in menu.items():
    print(f"{key}: {item['name']} | {item['base_price']}")

while True:
    #đơn hàng hiện tại và lệnh tính tiền:
    print()
    print('-'*30)
    print('--- ĐƠN HÀNG ---')
    tong_don = 0
    if not don:
        print('danh sách trống')
    else:
        for mon_moi, thong_tin in don.items():
            gia_cuoi = thong_tin["base_price"]
        #tính giá theo size
            size = thong_tin["size"]
            if size == 'S': gia_cuoi -= 5000
            elif size == 'L': gia_cuoi += 10000
        #tính topping
            goi_them = ""
            if "topping" in thong_tin:
                gia_cuoi += 5000
                goi_them = f"  | topping: {thong_tin['topping']}"
            print(f"{mon_moi} {thong_tin['name']}: {gia_cuoi}")
            print(f"    size: {size} | đường {thong_tin['sugar']} | đá {thong_tin['ice']} | {goi_them}")
            tong_don += gia_cuoi
    print('TỔNG CỘNG: ', tong_don)
    print()

#lệnh điều hướng
    print('-'*30)
    print('nhập để thay đổi')
    print("(1). Thêm món | (2). Bỏ món | (3). Chỉnh món | (q). Xác nhận đơn hàng")
    lenh = input("nhập vào đây: ").strip().lower()
    print()

#mục điều hướng chính:
    if lenh == 'q':
        print('Đặt hàng thành công! Tổng đã oder:', tong_don, '.cảm ơn bạn đã ủng hộ <3!')
        break

#(1). Thêm món
    if lenh == '1':
        chon = input('chọn món tại đây (nhập key menu): ').strip().lower()
        if chon in menu:
            mon_moi = menu[chon].copy()
            mon_moi.update({
            "size": "M",
            "sugar": 100,
            "ice": 100
            })
            print()
            print(f"--- thông số mặc định: {mon_moi['name']}---")
            print(f"    size {mon_moi['size']} | đường {mon_moi['sugar']} | đá {mon_moi['ice']}")
            print()

            while True:
                thay_doi = input('bạn muốn thay đổi gì? (duong/da/size/xong): ').strip().lower()
                if thay_doi == 'xong': break

                if thay_doi == 'duong':
                    mon_moi["sugar"] = int(input('mức đường mới (0/25/50/75/100/xong): '))
                elif thay_doi == 'da':
                    mon_moi["ice"] = int(input('mức đá mới (0/25/50/75/100/xong): '))
                elif thay_doi == 'size':
                    mon_moi["size"] = input('chọn size bạn muốn oder(S/M/L/xong): ').upper()
                elif thay_doi == 'topping':
                    mon_moi['topping'] = 'trân châu'

            # id_don = f"{chon}_{len(don) + 1}"  #phân loại kĩ hơn để dễ tách ra khi khách order nhiều
            id_don = chon
            don[id_don] = mon_moi
            print('đã thêm: ', mon_moi['name'])
            print()
        else:
            print('món không tồn tại trong menu')

#(2). Bỏ món
    elif lenh == '2':
        lua_chon = input('nhập món cần bỏ(nhập key menu): ').strip()
        if lua_chon in don:
            mon_xoa = don[lua_chon]['name']
            del don[lua_chon]
            print('đã bỏ: ', mon_xoa, '!')
            print()
        else:
            print('không tìm thấy món trong đơn hàng của bạn: '
              '. vui lòng thử lại!')

#(3). Chỉnh món
    elif lenh == '3':
        chinh_mon = input('Bạn muốn chỉnh món gì? (nhập xong nếu bấm nhầm) ').strip()
        if chinh_mon in don:
            mon = don[chinh_mon]
            while True:
                chinh = input(f"chỉnh {mon['name']}.(duong/da/topping/size/xong): ").strip().lower()

                if chinh.lower() == 'xong':
                    break

                if chinh == 'duong':
                    mon["sugar"] = int(input('mức đường mới (0/25/50/75/100): '))
                elif chinh == 'da':
                    mon["ice"] = int(input('mức đá mới (0/25/50/75/100): '))
                elif chinh == 'size':
                    mon["size"] = input('chọn size bạn muốn oder(S/M/L): ').upper()
                elif chinh == "topping":
                    if 'topping' in mon:
                        del mon["topping"]
                        print('đã bỏ topping')
                    else:
                        mon["topping"] = "trân châu"
                        print('đã thêm topping')
            print('đã cập nhật món',mon['name'])
        else:
            print('không tìm thấy món trong đơn.!')