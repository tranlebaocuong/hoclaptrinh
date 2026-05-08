from getpass import getpass
name1 = input('Tên đầy đủ là gì mậy? ')
guessed_number1 = str(input('keo, bua, hay bao? '))
score_1 = 0
name2 = input('Tên đầy đủ là gì mậy? ')
guessed_number2 = str(input('keo, bua hay bao? '))
score_2 = 0
if (guessed_number2 == 'keo' and guessed_number1 == 'keo') or (guessed_number2 == 'bao' and guessed_number1 == 'bao') or (guessed_number2 == 'bua' and guessed_number1 == 'bua'):
  print('Hòa rồi đó, làm lại đi tụi bây')
elif (guessed_number2 == 'bua' and guessed_number1 == 'keo') or (guessed_number2 == 'keo' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'bua'):
  print(name2 + ' thắng rồi đó con gà này')
  score_2 = score_2 + 1
elif (guessed_number2 == 'keo' and guessed_number1 == 'bua') or (guessed_number2 == 'bua' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'keo'):
  print(name1 + ' thắng rồi đó con gà này')
  score_1 = score_1 + 1
guessed_number1 = str(input('keo, bua, hay bao? '))
guessed_number2 = str(input('keo, bua hay bao? '))
if (guessed_number2 == 'keo' and guessed_number1 == 'keo') or (guessed_number2 == 'bao' and guessed_number1 == 'bao') or (guessed_number2 == 'bua' and guessed_number1 == 'bua'):
  print('Hòa rồi đó, làm lại đi tụi bây')
elif (guessed_number2 == 'bua' and guessed_number1 == 'keo') or (guessed_number2 == 'keo' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'bua'):
  print(name2 + ' thắng rồi đó con gà này')
  score_2 = score_2 + 1
elif (guessed_number2 == 'keo' and guessed_number1 == 'bua') or (guessed_number2 == 'bua' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'keo'):
  print(name1 + ' thắng rồi đó con gà này')
  score_1 = score_1 + 1
guessed_number1 = str(input('keo, bua, hay bao? '))
guessed_number2 = str(input('keo, bua hay bao? '))
if (guessed_number2 == 'keo' and guessed_number1 == 'keo') or (guessed_number2 == 'bao' and guessed_number1 == 'bao') or (guessed_number2 == 'bua' and guessed_number1 == 'bua'):
  print('Hòa rồi đó, làm lại đi tụi bây')
elif (guessed_number2 == 'bua' and guessed_number1 == 'keo') or (guessed_number2 == 'keo' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'bua'):
  print(name2 + ' thắng rồi đó con gà này')
  score_2 = score_2 + 1
elif (guessed_number2 == 'keo' and guessed_number1 == 'bua') or (guessed_number2 == 'bua' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'keo'):
  print(name1 + ' thắng rồi đó con gà này')
  score_1 = score_1 + 1
if score_1 >= 2:
  print(name1 + ' thang')
elif score_2 >= 2:
  print(name2 + ' thang')