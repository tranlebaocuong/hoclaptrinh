people = input('người lớn, người cao tuổi, trẻ em hay hssv ')
day = input('coi phim vào thứ mấy ')
time = int (input('suất chiếu vào lúc mấy giờ '))

note = 'Giá vé của bạn là: 60.000 VNĐ'
note_1 = 'Giá vé của bạn là: 65.000 VNĐ'
note_2 = 'Giá vé của bạn là: 45.000'
note_3 = 'Giá vé của bạn là 75.000'
note_4 = 'Giá vé của bạn là 85.000'

if people == 'lớn':
  if day == 'thứ 2' and day == 'thứ 4' and day == 'thứ 5' and time < 10 or time > 22:
    print(note)
  elif day == 'thứ 6' and day == 'thứ 7' and day == 'chủ nhật' and time < 10 or time > 22:
    print(note_1)

if people == 'lớn':
  if day == 'thứ 2' and day == 'thứ 4' and day == 'thứ 5' and time <= 22:
    print(note_3)
  elif day == ' thứ 7' and day == 'chủ nhật' and time <= 22:
    print(note_4)

if people == 'trẻ em':
  if day == 'thứ 2' and day == 'thứ 4' and day == 'thứ 5' and time <= 24:
    print(note)
  elif day == 'thứ 7' and day == 'chủ nhật' and time <= 24:
    print(note_1)

if day == 'thứ 3':
  if people == 'lớn' and time <= 24:
    print(note_2)
  elif people == 'trẻ em' and time <= 24:
    print(note_2)