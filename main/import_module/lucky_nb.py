
# player = int(input('hay nhap so ban muon: '))
import random

so_doan = random.randint(1, 50)
thang = False     #bắt đầu chưa chơi nên sẽ mặc định số lần thắng là false

for i in range(1,6):

    # print(player)
    player = int(input('hay nhap lai: '))

    if player == so_doan:
        print('chính xác! bạn đã thắng')
        thang = True             #khi đã thắng biến sẽ nhận là true
        break
    elif player > so_doan:
        print('thấp hơn!')

    else:
        print('cao hơn!')           #tạo biến để theo dõi thắng thua
if not thang:
    print('bạn đã hết lượt chơi')