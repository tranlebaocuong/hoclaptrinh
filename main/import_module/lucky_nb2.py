import random

def doan_so(min_so, max_so, so_luot_toi_da):
    so_doan = random.randint(min_so, max_so)
    thang = False

    for i in range(1,so_luot_toi_da + 1):

    # print(player)
        player = int(input('hay nhap lai: '))

        if player == so_doan:
            print('chính xác! bạn đã thắng')
            break
            thang = True

        elif player > so_doan:
            print('thấp hơn!')

        else:
            print('cao hơn!')
    if not thang:
        print('bạn đã hết lượt chơi')
# doan_so(1,50, 5)
doan_so(1,100,7)