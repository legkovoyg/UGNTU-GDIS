import HornerM
from Graphics import FirstGraphic, SecondGraphic
from classes import Pressure, Time, Debit

# Все данные из Excel файла
data = HornerM.GetInfoFromExcel()
# Все время исследования
alltime = data.to_numpy(float)[:, 0]
alltime = Time(alltime).sec
# Забойное давление
pressure = data.to_numpy(float)[:, 1]
pressure = Pressure(pressure).fATM_toPa
# Значение времени во время закачки
time = data.to_numpy(float)[:, 2]
time = Time(time).sec
# Изменение объема закачки во времени
debit = data.to_numpy(float)[:, 3]
debit = Debit(debit).m3sec
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
