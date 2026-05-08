
playlist = ["Shape of You", "Blinding Lights", "Dynamite"]

# Viết code của bạn tại đây

while True:
    # print(playlist)

    for bai_hat in enumerate(playlist, 1):

        print(bai_hat)

        print()

    print( '1: thêm bài / 2: đổi thứ tự / 3: xóa bài / q: thoát')

    print()



    lua_chon = input('bạn muốn làm gì? ').lower()
    print()
    if lua_chon.lower() == 'q':
        print('đã thoát...')
        break

    elif lua_chon == '1':
        them_bai = input('nhập bài hát bạn muốn thêm: ')
        playlist.append(them_bai)
        print('đã thêm bài: ', them_bai)

    elif lua_chon == '2':
        cu = input('nhập số thứ tự bài bạn muốn di chuyển ')
        print()

        moi = input('nhập vị trí bạn muốn di chuyển tới ')
        print()

        if  cu.isdigit() and moi.isdigit():     #ktra người dùng nhập bằng số

            so_cu = int(cu) - 1          #thứ tự bắt đầu = 0
            so_moi = int(moi) - 1


        if 0 <= so_cu < len(playlist) and 0 <= so_moi < len(playlist):
            di_chuyen =  playlist.pop(so_cu)

            playlist.insert(so_moi, di_chuyen)

            print('đã chuyển bài: ', di_chuyen, 'sang vị trí số: ', moi)

            print()

        else:
            print('vị trí không hợp lệ...')
            print()


    elif lua_chon == '3':
        xoa = input('nhập số thứ tự bài muốn xóa ')

        if  xoa.isdigit():     #ktra người dùng nhập bằng số

            so_xoa = int(xoa) - 1          #thứ tự bắt đầu = 0

        if 0 <= so_xoa < len(playlist):
            bai_da_xoa =  playlist.pop(so_xoa)

            print('playlist sau khi xóa: ', bai_da_xoa)
            print()

        else:
            print('bài hát không tồn tại...')

    else:
        print('vui lòng nhập số thứ tự')
    # print('playlist hiện tại là:', playlist)