name1 = input('Tên đầy đủ là gì mậy? ')
guessed_number1 = str(input('kéo, búa, hay bao? '))
name2 = input('Tên đầy đủ là gì mậy? ')
guessed_number2 = str(input('kéo, búa hay bao? '))
if (guessed_number2 == 'kéo' and guessed_number1 == 'kéo') or (guessed_number2 == 'bao' and guessed_number1 == 'bao') or (guessed_number2 == 'búa' and guessed_number1 == 'búa'):
  print('Hòa rồi đó, làm lại đi tụi bây')
elif (guessed_number2 == 'búa' and guessed_number1 == 'kéo') or (guessed_number2 == 'kéo' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'búa'):
  print(name2 + ' thắng rồi đó con gà này')
elif (guessed_number2 == 'kéo' and guessed_number1 == 'búa') or (guessed_number2 == 'búa' and guessed_number1 == 'bao') or (guessed_number2 == 'bao' and guessed_number1 == 'kéo'):
  print(name1 + ' thắng rồi đó con gà này')
