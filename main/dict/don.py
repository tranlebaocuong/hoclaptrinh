
don = {
    "name": "Tra sua",
    "base_price": 25000,
    "size": "M",
    "sugar": 100,
    "ice": 100
}

# Viết code của bạn tại đây
def hien_thi_don_hang(mon):
    print()
    print('='*5, 'ĐƠN HÀNG HIỆN TẠI', '='*5)
    print(f"Món: {mon['name']}")
    goi_them = f"| topping: {mon['topping']}" if 'topping' in mon else ""
    print(f"size: {mon['size']} | đường: {mon['sugar']} | đá: {mon['ice']} {goi_them}")
    print(f" TỔNG: {tinh_gia_cuoi(mon):,} VNĐ")
    print('='*30)

def tinh_gia_cuoi(mon):
    tong = mon['base_price']

    if mon['size'] == 'S': tong -= 5000
    if mon['size'] == 'L': tong += 10000

    if 'topping' in mon: tong += 5000
    return tong

def danh_sach_tuy_chinh():
    print()
    lua_chon = ['chỉnh Đường/Đá', 'thêm bỏ topping', 'đổi size', 'xác nhận đặt hàng']
    for i, mon in enumerate(lua_chon, 1):
        print(f"{i}. {mon}")

def tuy_chinh_duong_da(mon):
    loai = input('bạn muốn chỉnh gì(đường/đá): ').strip().lower()
    if loai in ['duong', 'da']:
        muc = input(f"mức {loai} mới (0,25,50,75,100): ")
        if muc.isdigit():
            mon['sugar' if loai == 'duong' else 'ice'] = int(muc)
    else:
        print('lựa chọn không hợp lệ')

def tuy_chinh_topping(mon):
    if 'topping' in mon:
        del mon['topping']
        print(' đã bỏ topping')
    else:
        mon['topping'] = 'trân châu'
        print('đã thêm trân châu')

def tuy_chinh_size(mon):
    moi = input('size S/M/L').strip().upper()
    if moi in ['S', 'M', 'L']:
        mon['size'] = moi
    else:
        print('size không có')


def main():
    while True:
        hien_thi_don_hang(don)
        danh_sach_tuy_chinh()

        user = input('nhập số thứ tự bạn muốn chọn: ').strip()

        if user == '4':
            print('cảm ơn bạn đã ủng hộ <3')
            hien_thi_don_hang(don)
            break
        elif user == '1':
            tuy_chinh_duong_da(don)
        elif user == '2':
            tuy_chinh_topping(don)
        elif user == '3':
            tuy_chinh_size(don)
        else:
            print('vui lòng chọn đúng STT')

if __name__ == '__main__':
    main()
