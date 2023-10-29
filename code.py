import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# Чтение данных с исходного файла
dannye = pd.read_excel('in.xlsx')
new_dannye = dannye[np.isfinite(dannye)]


# Присваивание переменных исходным данным
alltime = dannye.to_numpy(float)[:, 0]  # Все время исследования
pressure = dannye.to_numpy(float)[:, 1]  # Забойное давление
time = dannye.to_numpy(float)[:, 2]  # Время закачки
debit = dannye.to_numpy(float)[:, 3]  # Закачка

# Перевод в СИ исходных данных
pressurePA = pressure * 101325  # Перевод в  атм - ПА
debitPS = debit / 60  # Перевод в -м3/мин - м3/с
timeSEC = time * 60  # Перевод мин - сек
alltimeSEC = alltime * 60  # Перевод мин-сек

# Операции с данными
# Поиск времени закачки
zakach = dannye.to_numpy(float)[:, -2:]
for x in zakach:
    if x[1] == 0:
        timeZak = t
        timeZakSEC = t * 60
        # print(timeZakSEC)
        break
    t = x[0]

# Время Хорнера
HornerTime = []
for x in alltimeSEC:
    addHorner = math.log(((x + timeZakSEC) / x), 10)
    HornerTime.append(addHorner)

# Qdt и сортировка от NaN
Qdt = []
y = 0
for x in range(0, len(debitPS)):
    if y == 0:
        b = debitPS[x] * timeSEC[x]
        Qdt.append(b)
        y = y + 1
    else:
        b = debitPS[x] * (timeSEC[x] - timeSEC[x - 1])
        Qdt.append(b)
Qdt = list(filter(lambda i: str(i) != 'nan', Qdt))


# Объем закачки
FullDebit = sum(Qdt)

# Средняя закачка
AvgDebit = FullDebit / (timeZak * 60)

# График t-Pзаб
fig, ax = plt.subplots()
ax.plot(alltimeSEC, pressurePA, color='green')
ax.set_xlabel('Время, сек', fontsize=7)
ax.set_ylabel('Забойное давление, Па', fontsize=7)
ax2 = ax.twinx()
ax2.plot(alltimeSEC, debitPS, color='orange')
ax2.set_ylabel('Закачка, м3/сек', fontsize=7)
plt.ylim(0, 0.1)
plt.show()

# Поиск данных после нагнетательного теста, Pзаб - Время хорнера
linearFind = [HornerTime, pressurePA, alltime]
tranlinearFind = np.transpose(linearFind)
LFpressure = []
LFHorner = []
for x in tranlinearFind:
    # print (x[0],' - ',x[1],' - ', x[2])
    if x[2] > timeZak:
        LFHorner.append(x[0])
        LFpressure.append(x[1])
    else:
        continue

# График lg(t/t+T) - Pзаб
fig, ax = plt.subplots()
ax.plot(LFHorner, LFpressure, color='red')
ax.set_xlabel('Время Хорнера', fontsize=7)
ax.set_ylabel('Забойное давление, Па')
plt.xlim(0, 0.4)
plt.ylim(0, 70000000)
plt.show()

LFHorLFpres1 = LFHorner, LFpressure
LFHorLFpres2 = np.transpose(LFHorLFpres1)

# Построение касательной

# Ввод значений для пользователя
print('Введите значение времени Хорнера 1, для построения касательной: ')
userHorner1 = float(input())
print('Введите значение времени Хорнера 2, для построения касательной: ')
userHorner2 = float(input())

# Смена значений, если пользователь введет сначала большее значение, а затем меньшее
if userHorner1 > userHorner2:
    c = userHorner1
    userHorner1 = userHorner2
    userHorner2 = c

# Поиск значений среди предоставленных данных, максимально приближенных к введенным пользователем
for x in LFHorLFpres2:
    if userHorner1 > x[0]:
        userHorner1 = x[0]
        userPressure1 = x[1]
        print('Время Хорнера для точки Х1,наиболее приближенное к введеному :', userHorner1)
        print('Давление для точки Х1, наиболее приближенное к введеному:', userPressure1, 'Па')
        break

for x in LFHorLFpres2:
    if userHorner2 > x[0]:
        userHorner2 = x[0]
        userPressure2 = x[1]
        print('Время Хорнера для точки Х2,наиболее приближенное к введеному :', userHorner2)
        print('Давление для точки Х2, наиболее приближенное к введеному:', userPressure2, 'Па')
        break

# Расчет пластового давления, основываясь на данных пользователя
PlastPressure = (userPressure1 - userPressure2) * ((-1) * ((userHorner2) / (userHorner1 - userHorner2))) + userPressure2
print('Пластовое давление равно:', PlastPressure)
tga = (userPressure2 - userPressure1) / (userHorner2 - userHorner1)
print('Уклон касательной равен :', tga)
hydro = AvgDebit / 4 / math.pi / tga
print('Гидропроводность равна:', hydro, 'м*Д/Па*с')

dannye.to_excel('./out.xlsx', sheet_name='Расчеты', index=False)
