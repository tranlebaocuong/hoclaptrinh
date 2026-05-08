
MENU = [
    {"name": "Trà sữa", "base_price": 25000},
    {"name": "Trà sữa trân châu", "base_price": 29000},
    {"name": "Cà phê sữa", "base_price": 30000},
    {"name": "Matcha latte", "base_price": 35000},
    {"name": "Hồng trà", "base_price": 22000},
    {"name": "Trà đào", "base_price": 28000}
]

don = []

#Viết code của bạn tại đây:
def hoi_tuy_chinh_gi():
    chinh = input('muốn chỉnh gì? (duong/da/size/topping/xong): ').strip().lower()
    if chinh in ('duong', 'da', 'size', 'topping', 'xong'):
        return chinh
    return None


def hoi_muc_duong_da(loai):
    muc = input(f"nhập mức {loai} mới (0/25/50/100): ").strip()
    if muc in ('0', '25', '50', '100'): return int(muc)
    return None

def hoi_muc_moi_size():
    size_moi = input('chọn size mới (S/M/L): ').strip().upper()
    if size_moi in ('S', 'M', 'L'): return size_moi
    return None

def hoi_muc_moi(chinh):
    if chinh in ('duong', 'da'): return hoi_muc_duong_da(chinh)
    if chinh == 'size': return hoi_muc_moi_size()
    return None

def dieu_huong():
    print('-'*30)
    return input('(1). Thêm | (2). Bỏ | (3). Chỉnh | (4). Xác Nhận/Thanh Toán: ').strip()

def thong_tin_stt(chon, gioi_han):
    stt = int(input(chon))
    if 1 <= stt <= gioi_han:
        return stt
    return None

def tinh_gia_cuoi(mon):
    gia = mon['base_price']

    #tính size:
    size = mon.get('size', 'M')
    if size == 'S': gia -= 5000
    if size == 'L': gia += 10000

    #tính topping:
    if 'topping' in mon: gia += 5000
    return gia

def tuy_chinh_mon(mon):
    tuy_chinh = {'duong': 'sugar', 'da': 'ice', 'size': 'size'}
    while True:

        chinh = hoi_tuy_chinh_gi()
        if not chinh or chinh == 'xong':
            break

        if chinh == 'topping':
            if 'topping' in mon:
                del mon['topping']
                print('-> đã bỏ topping')
            else:
                mon['topping'] = 'trân châu'
                print('-> đã thêm topping')
        else:
            muc_moi = hoi_muc_moi(chinh)
            if muc_moi is not None:
                mon[tuy_chinh[chinh]] = muc_moi
                print(f"dã chỉnh {chinh} thành {muc_moi}")
            else:
                print('mức không hợp lệ')

def in_don_hang():
    if not don:
        return 0

    print('='*5, 'ĐƠN HÀNG', '='*5)

    tong = 0

    for i, mon in enumerate(don, 1):
        gia = tinh_gia_cuoi(mon)
        goi_them = f"| topping: {mon['topping']}" if 'topping' in mon else ""
        print(f"{i}.{mon['name']} ({mon['size']}: {gia})")
        print(f"    size: {mon['size']} | đường: {mon['sugar']} | đá: {mon['ice']} {goi_them}")
        tong += gia
    print(f"TỔNG CỘNG: {tong:}")
    return tong



def main():

    while True:
        print()
        print('='*5, 'MENU', '='*5)

        for i, m in enumerate(MENU, 1):
            print(f"{i}. {m['name']:} | {m['base_price']:} ")
        print()
        tong_hien_tai = in_don_hang()
        print()
        chon = dieu_huong()

        if chon == '4':
            print()
            print('tổng đơn hàng của bạn là: ', tong_hien_tai)
            print('cảm ơn bạn đã ủng hộ <3')
            break

        elif chon == '1':
            stt = thong_tin_stt('nhập STT để chọn món: ', len(MENU))
            if not stt:
                print('sai')
                continue

            mon_moi = {**MENU[stt-1], 'size': 'M', 'sugar': 100, 'ice': 100}
            tuy_chinh_mon(mon_moi)
            don.append(mon_moi)

        elif chon == '2':
            if not don:
                print('đơn hàng trống')
                continue
            stt = thong_tin_stt('nhập stt món muốn bỏ: ', len(don))
            if stt:
                da_xoa = don.pop(stt-1)
                print(f"đã bỏ {da_xoa['name']}")
        elif chon == '3':
            if not don:
                print('đơn hàng trống.')
                continue
            stt = thong_tin_stt('nhập stt món muốn chỉnh: ', len(don))

            if stt:
                tuy_chinh_mon(don[stt-1])



if __name__ == '__main__':
    main()