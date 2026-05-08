import json
import sys
from pathlib import Path

def doc_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def luu_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def lay_duong_dan_du_lieu():
    root_dir = Path(__file__).resolve().parents[2]
    menu_path = root_dir / "data" / "orders" / "menu.json"
    orders_path = root_dir / "data" / "orders" / "orders.json"
    return menu_path, orders_path

def tinh_gia_cuoi(mon):
    gia = mon['base_price']
    if mon['size']  == 'S': gia -= 5000
    elif mon['size'] == 'L': gia += 10000

    if mon.get('topping'): gia += 5000
    return gia


def chinh_size(mon):
    s = input("chọn size (S/M/L): ").upper()
    if s in ['S', 'M', 'L']:
        mon['size'] = s
    else:
        print("size không có")
    return mon

def chinh_topping(mon):
    mon['topping'] = input("nhập tên topping: ")
    return mon

def chinh_duong_da(mon, loai):
    mon[loai] = input(f"nhập mức {loai}: ")
    return mon

def tuy_chinh_mon(mon):
    if 'size' not in mon:
        mon.update({'size': 'M', 'sugar': '100', 'ice': '100', 'topping': '', 'final_price': mon['base_price']})

    while True:
        top_info = f"   | topping: {mon['topping']}" if mon['topping'] else ""
        print(f" --->  hiện tại: size: {mon['size']} | đường: {mon['sugar']} | đá: {mon['ice']} {top_info}")
        print(f" --> giá tạm tính: {mon['final_price']:,}")

        chinh = input("bạn muốn điều chỉnh gì? (size/duong/da/topping/xong): ").lower()

        if chinh == 'xong': break
        elif chinh == 'size': mon = chinh_size(mon)
        elif chinh == 'duong': mon = chinh_duong_da(mon, 'sugar')
        elif chinh == 'da': mon = chinh_duong_da(mon, 'ice')
        elif chinh =='topping': mon = chinh_topping(mon)

        mon['final_price'] = tinh_gia_cuoi(mon)

    return mon

def hien_thi_giao_dien(menu, don_hang):
    print('='*40)
    print("=== MENU QUÁN ===")
    for i, m in enumerate(menu, 1):
        print(f"{i}. {m['name']} | {m['base_price']:,}")

    print("=== ĐƠN HÀNG HIỆN TẠI ===")
    tong_bill = 0

    if not don_hang:
        print('trống')
        return 0
    else:
        for i, item in enumerate(don_hang, 1):
            topping = item.get('topping', '')
            top_str = f"(+{topping})" if topping else ""
            final_price = item.get('final_price', item.get('base_price', 0))
            size = item.get('size', 'M')
            print(f"{i}. {item['name']} (size {size}{top_str}) - {final_price:,}")
            tong_bill += final_price
    print('_'*40)
    print(f" TỔNG ĐƠN: {tong_bill:,}")
    return tong_bill

def hanh_dong_them(menu, don_hang):
    chon = input("chọn món (nhập STT): ")
    if chon.isdigit() and 0 < int(chon) <= len(menu):
        mon_moi = menu[int(chon)-1].copy()
        mon_sau_chinh = tuy_chinh_mon(mon_moi)
        don_hang.append(mon_sau_chinh)
        print(f"đã thêm: {mon_sau_chinh['name']}")
    else:
        print("STT không hợp lệ")

def hanh_dong_bo(don_hang):
    if not don_hang:
        print("đơn hàng trống")
        return
    stt = input("nhập STT món cần xóa: ")

    if stt.isdigit() and 0 < int(stt) <= len(don_hang):
        removed = don_hang.pop(int(stt)-1)
        print(f"đã xóa: {removed['name']}")

    else:
        print('STT không hợp lệ')

def hanh_dong_chinh(don_hang):
    if not don_hang:
        print("đơn hàng đang trống")
        return
    stt = input("nhập STT món cần chỉnh: ")

    if stt.isdigit() and 0 < int(stt) <= len(don_hang):
        tuy_chinh_mon(don_hang[int(stt)-1])
        print("đã cập nhật món")
    else:
        print("STT không hợp lệ")

def xac_nhan_va_luu(don_hang, lich_su_don, tong_bill):
    if not don_hang:
        print("hẹn gặp lại quý khách")
        return
    new_id = f"ODR{len(lich_su_don) + 1:03}"
    lich_su_don.append({
        "id": new_id,
        "items": don_hang,
        "total": tong_bill
    })
    _, orders_path = lay_duong_dan_du_lieu()
    luu_json(orders_path, lich_su_don)
    print(f"đã đặt đơn {new_id} thành công ")

def ung_dung_goi_mon():
    # Tránh lỗi UnicodeEncodeError trên terminal Windows khi in tiếng Việt.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    menu_path, orders_path = lay_duong_dan_du_lieu()
    menu = doc_json(menu_path)
    lich_su = doc_json(orders_path)
    don_hang_hien_tai = []

    while True:
        tong_cong = hien_thi_giao_dien(menu, don_hang_hien_tai)

        print("bạn muốn làm gì? (1). thêm | (2). bỏ | (3). chỉnh | (q). xong")
        lenh = input("--->: ").lower().strip()

        if lenh == 'q':
            xac_nhan_va_luu(don_hang_hien_tai, lich_su, tong_cong)
            break

        if lenh == "1":
            hanh_dong_them(menu, don_hang_hien_tai)
        elif lenh == "2":
            hanh_dong_bo(don_hang_hien_tai)
        elif lenh == "3":
            hanh_dong_chinh(don_hang_hien_tai)
        else:
            print("không hợp lệ")

if __name__ == "__main__":
    ung_dung_goi_mon()
