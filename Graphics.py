import matplotlib.pyplot as plt
from classes import Debit, Pressure, Time
import pandas as pd


def GetInfoFromExcel():
    dannye = pd.read_excel('in.xlsx')
    return dannye


alltime = GetInfoFromExcel().to_numpy(float)[:, 0]  # Все время исследования
pressure = GetInfoFromExcel().to_numpy(float)[:, 1]  # Забойное давление
time = GetInfoFromExcel().to_numpy(float)[:, 2]  # Время закачки
debit = GetInfoFromExcel().to_numpy(float)[:, 3]  # Закачка


async def ChoosePressure(pressurePA):
    print('Введите желаемую величину для отображения графика')
    print('1-Па, 2- МПа, 3-атм')
    choose2 = int(input())
    if choose2 == 1:
        pressure = Pressure(pressurePA).fPa_toPa
    elif choose2 == 2:
        pressure = Pressure(pressurePA).fPa_toMPa
    elif choose2 == 3:
        pressure = Pressure(pressurePA).fPa_toATM
    return pressure, choose2


async def FirstGraphic(pressure, alltime, debit):
    ChosenPressure = await ChoosePressure(pressure)
    a = ChosenPressure[0]
    b = ChosenPressure[1]
    print(a)
    print(b)
    plt.plot(alltime, a, color='green', label='Давление')
    plt.xlabel('Время, сек')
    if b == 1:
        plt.ylabel('Забойное давление,  Па', )
    elif b == 2:
        plt.ylabel('Забойное давление,  МПа', )
    elif b == 3:
        plt.ylabel('Забойное давление,  атм', )
    ax2 = plt.twinx()
    ax2.plot(alltime, debit, color='orange', label='Закачка')
    ax2.set_ylabel('Закачка, м3/сек', )
    plt.ylim(0, 0.1)
    plt.show()


async def SecondGraphic(hornerTime, pressure):
    ChosenPressure = await ChoosePressure(pressure)
    plt.plot(hornerTime, ChosenPressure[0], color='red')
    plt.xlabel('Время Хорнера', )
    if ChosenPressure[1] == 1:
        plt.ylabel('Забойное давление,  Па', )
    elif ChosenPressure[1] == 2:
        plt.ylabel('Забойное давление,  МПа', )
    elif ChosenPressure[1] == 3:
        plt.ylabel('Забойное давление,  атм', )
    plt.title('После закачки')
    maxX = max(hornerTime)
    maxY = max(ChosenPressure[0])
    plt.xlim(0, maxX * 1.5)
    plt.ylim(0, maxY * 1.2)
    plt.tight_layout()
    plt.show()
