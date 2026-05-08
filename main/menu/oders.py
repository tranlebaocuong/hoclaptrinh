import json

def doc_du_lieu(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    return []

def xu_ly_size(mon):
    while True:

        size = input("chọn size  (S/M/L): ").upper()
        mon['size'] = size

        if size not in ["S", "M", "L"]:
            print('không hợp lệ (vui lòng chọn S/M/L)')
            continue

        elif size == 'L':
            mon['final_price'] = mon['base_price'] + 5000
        elif size == 'S':
            mon['final_price'] = mon['base_price'] - 5000
        else:
            mon['final_price'] = mon['base_price']
        return mon

def xu_ly_topping(mon):
    topping = input('nhập tên topping: ')
    mon['topping'] = topping

    mon['final_price'] += 5000
    print(f"đã thêm {topping} (+5000)")
    return mon

def xu_ly_duong(mon):
    print("mức đường: 1. 0% | 2. 25% | 3. 50 | 4. 75% (mặc định là 100%)")
    chon = input("chọn mức đường bạn muốn (1/2/3/4): ")
    if chon == '1': mon['sugar'] = 0
    elif chon == '2': mon['sugar'] = 25
    elif chon == '3': mon['sugar'] = 50
    elif chon == '4': mon['sugar'] = 75
    else: mon['sugar'] = 100
    return mon

def xu_ly_da(mon):
    print("mức đá: 1. 0% | 2. 25% | 3. 50 | 4. 75% (mặc định là 100%)")
    chon = input("chọn mức đá bạn muốn (1/2/3/4): ")
    if chon == '1': mon['ice'] = 0
    elif chon == '2': mon['ice'] = 25
    elif chon == '3': mon['ice'] = 50
    elif chon == '4': mon['ice'] = 75
    else: mon['ice'] = 100
    return mon

def tuy_chinh_mon(mon):
    mon.update({'size': 'M', 'sugar': 100, 'ice': 100, 'final_price': mon['base_price']})

    while True:
        chinh = input("bạn muốn chỉnh gì? (size/duong/da/topping/xong): ")

        if chinh == 'xong': break
        elif chinh == 'size': mon = xu_ly_size(mon)
        elif chinh == 'duong': mon = xu_ly_duong(mon)
        elif chinh == 'da': mon = xu_ly_da(mon)
        elif chinh == 'topping': mon = xu_ly_topping(mon)
    return mon

def in_hoa_don(don_hang):
    print('='*30)
    print('=== ĐƠN HÀNG CỦA BẠN ===')

    tong_tien = 0
    for i, item in enumerate(don_hang, 1):
        note = f"{item['size']}, {item['sugar']} đường, {item['ice']} đá"
        if 'topping' in item: note += f", +{item['topping']}"

        print(f"{i}. {item['name']} ({note})")
        print(f"    {item['final_price']:,}")
        tong_tien += item['final_price']

    print('-'*30)
    print(f"TỔNG CỘNG: {tong_tien:,}")
    return tong_tien

def tao_don_hang():
    menu = doc_du_lieu("practicing/orders/menu.json")
    don_hang = []


    while True:
        print()
        print('===  MENU QUÁN ===')
        for i, m in enumerate(menu,1):
            print(f"{i}. {m['name']} - {m['base_price']:,}")

        chon = input("chọn món(nhập STT, hoặc q để hoàn tất): ")
        if chon.lower() == 'q': break

        if not chon.isdigit():
            print("vui lòng nhập STT hoặc q")
            continue
        idx = int(chon) - 1
        if idx < 0 or idx >= len(menu):
            print(f"không có món số {chon}. vui lòng chọn món khác!")
            continue

        mon_goc = menu[idx].copy()
        mon_sau_chinh = tuy_chinh_mon(mon_goc)
        don_hang.append(mon_sau_chinh)

        print(f"đã thêm {mon_sau_chinh['name']}")
        in_hoa_don(don_hang)
    if don_hang:
        path_orders = "practicing/orders/orders.json"
        all_orders = doc_du_lieu(path_orders)

        new_id = f"ODR{len(all_orders) + 1:03}"
        new_orders = {
            "id": new_id,
            "items": don_hang,
            "total_price": in_hoa_don(don_hang)
        }
        all_orders.append(new_orders)

        with open(path_orders, "w", encoding="utf-8") as f:
            json.dump(all_orders, f, ensure_ascii=False, indent=4)
        print(f"đã lưu đơn hàng {new_id} thành công")
    else:
        print('cảm ơn bạn đã ủng hộ <3')

tao_don_hang()

