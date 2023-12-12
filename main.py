import numpy as np

import HornerM
from Graphics import FirstGraphic, SecondGraphic, ThirdGraphic
from classes import Pressure, Time, Debit, Meters, Hydro, Compressibility

# Все данные из Excel файла
data = HornerM.GetInfoFromExcel()
# Все время исследования
alltime = data.to_numpy(float)[:, 0]
alltime = Time(alltime).fMin_toSec
# Забойное давление
pressure = data.to_numpy(float)[:, 1]
pressure = Pressure(pressure).fATM_toPa
# Значение времени во время закачки
time = data.to_numpy(float)[:, 2]
time = Time(time).fMin_toSec
# Изменение объема закачки во времени
debit = data.to_numpy(float)[:, 3]
debit = Debit(debit).fM3min_toM3sec
# Время остановки закачки
DownloadTime = HornerM.TimeZAK(data, time)
# Время Хорнера
HornerTime = HornerM.HornerTime(alltime, DownloadTime)
# Qdt
Qdt = HornerM.Qdt(debit, time)
# Объем закачанной жидкости
SumOfDebit = HornerM.FullDebit(Qdt)
# Средний дебит за время закачки
AvgDebit = HornerM.AvgDebit(SumOfDebit, DownloadTime)
# График t - Pзаб
FirstGraphic(pressure, alltime, debit)
# Давление после остановки закачки
pressureAfterTest = HornerM.GetPressureAfterTest(pressure,
                                                 alltime,
                                                 DownloadTime)
# Время Хорнера после остановки закачки
hornerAfterTest = HornerM.GetHornerAfterTest(HornerTime,
                                             alltime,
                                             DownloadTime)
alltimeAfterTest = HornerM.GetAlltimeAfterTest(alltime, DownloadTime)
# График Время Хорнера - Pзаб
SecondGraphic(hornerAfterTest, pressureAfterTest)
# Обработка параметров вводимых пользователем
UserInput = HornerM.UserHorner(hornerAfterTest, pressureAfterTest)
# Расчет пластового давления
PlastPressure = HornerM.ReservoirPressure(UserInput[0],
                                          UserInput[1],
                                          UserInput[2],
                                          UserInput[3])
# Угол наклона прямой (tga)
tga = HornerM.tgAlpha(UserInput)
# Гидропроводность
HydConductivity = HornerM.HydraulicСonductivity(AvgDebit, tga)
print('Введите толщину пласта, м')
PlastThickness = float(input())
# PlastThickness = 8.0

print('Введите величину коэффициента B, безразмерное')
coefB = float(input())
# coefB = 1.2
print('Введите значение пористости, д.ед ')
Porosity = float(input())
# Porosity = 0.28
print('Введите значение сжимаемости нефти')
compressibility = float(input())
# compressibility = 0.01
print('Введите значение радиуса скважины, м')
WellRadius = float(input())
# WellRadius = 0.146
# Безразмерное время
DimensTime = HornerM.DimensionlessTime(pressureAfterTest,
                                       alltimeAfterTest,
                                       Meters(PlastThickness).fM_toFoot,
                                       Hydro(HydConductivity).fDarsi_toFoot,
                                       Porosity,
                                       Compressibility(compressibility).fSI_toAmer,
                                       Meters(WellRadius).fM_toFoot,
                                       Debit(AvgDebit).fM3sec_toSTBd,
                                       coefB)[0]
# Безразмерное давление
DimensPressure = HornerM.DimensionlessTime(pressureAfterTest,
                                           alltimeAfterTest,
                                           Meters(PlastThickness).fM_toFoot,
                                           Hydro(HydConductivity).fDarsi_toFoot,
                                           Porosity,
                                           Compressibility(compressibility).fSI_toAmer,
                                           Meters(WellRadius).fM_toFoot,
                                           Debit(AvgDebit).fM3sec_toSTBd,
                                           coefB)[1]
# Производная безразмерного давления
dPWDtodTD = HornerM.pwDtotD(DimensTime, DimensPressure)
# Введите значение альфа для сглаживания прямой
print('Введите значение альфа для сглаживания прямой, от нуля до единицы')
AlphaInput = float(input())
# Массив производной после экспоненциального сглаживания
exponental = HornerM.exponential_smoothing(dPWDtodTD, AlphaInput)  # Вопрос сколько делать экспоненциальное сгл.
# График стращный
ThirdGraphic(DimensTime, DimensPressure, dPWDtodTD, exponental)
# m EST
mest = HornerM.Mest(DimensPressure, DimensTime)[0]
# Максимальное значение производной безразмерного давления после экспоненциального сглаживания
dPWmax = HornerM.getMax(exponental, DimensTime)[0]
# Соответствующее этой производной значение безразмерного времени
dtDmax = HornerM.getMax(exponental, DimensTime)[1]
# Ccoef
Ccoef = HornerM.Ccoef(AvgDebit, dPWmax, coefB, dtDmax)
# CDcoef
CDcoef = HornerM.CDcoef(Ccoef, Porosity, compressibility, WellRadius)
# Скин-фактор
Skin = HornerM.Skin(AvgDebit, coefB, Ccoef, Hydro(HydConductivity).fDarsi_toM2, DownloadTime, mest, CDcoef)
