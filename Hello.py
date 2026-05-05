don = {
    "name": "Tra sua",
    "base_price": 25000,
    "size": "M",
    "sugar": 100,
    "ice": 100
}

# Viết code của bạn tại đây
lua_chon_menu = ["chỉnh đường/ đá", "thêm/bỏ topping", "đổi size", "xác nhận đặt hàng"]
gia_tong = don['base_price']
while True:
    print('=== ĐƠN HÀNG HIỆN TẠI ===')
    print('Món:', don['name'])
    print('size:',don['size'],'/', 'đường:',don['sugar'],'/','đá:', don['ice'])
    if 'topping' in don:
        print('topping:',don['topping'])
    print('gia:',gia_tong)
    print()

    for i, chon in enumerate(lua_chon_menu, 1):

        print(str(i) + '.' ,chon)
    print()
    user = input('bạn muốn thay đổi gì không(nhập số): ')
    print()
    if user == '4':
        print('đặt hàng thành công, vui lòng kiểm tra lại thông tin')
        print('=== ĐƠN HÀNG HIỆN TẠI ===')
        print('Món:', don['name'])
        print('size:',don['size'],'/', 'đường:',don['sugar'],'/','đá:', don['ice'])
        if 'topping' in don:
            print('topping:',don['topping'])
        print('tổng của bạn là:', gia_tong)
        break

    if user == '1':

        thay_doi = input('bạn muốn thay đổi gì? (đường/đá): ').lower()

        if thay_doi not in ['đường', 'đá']:
            print('vui lòng nhập (đường hoặc đá)! ')
            continue

        muc_moi = int(input(f'tỉ lệ {thay_doi} mới? (0/25/50/75/100): ' ))
        print()

        if thay_doi == 'đường':
            don["sugar"] = muc_moi
        else:
            don["ice"] = muc_moi

    if user == '2':
        topping = input('bạn muốn thêm Trân châu không? (co/khong): ').lower()

        print()
        if topping == 'co':
            print('đã thêm trân châu!')
            print()
            don['topping'] = "trân châu"

            gia_tong += 5000

        elif topping == 'ko':
            print('đã bỏ trân châu')
            if 'topping' in don:
                don.pop('topping',None)
                gia_tong -= 5000

    if user == '3':
        doi_size = input('bạn muốn dùng size nào (S/M/L): ')

        print()
        don['size'] = doi_size
        if don['size'] == 'S':
            gia_tong -= 5000
        elif don['size'] == 'L':
            gia_tong += 10000
        else:
            gia_tong