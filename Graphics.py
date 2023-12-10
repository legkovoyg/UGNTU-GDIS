import matplotlib.pyplot as plt
import matplotlib
from classes import Debit, Pressure, Time
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots


def GetInfoFromExcel():
    dannye = pd.read_excel('in.xlsx')
    return dannye


alltime = GetInfoFromExcel().to_numpy(float)[:, 0]  # Все время исследования
pressure = GetInfoFromExcel().to_numpy(float)[:, 1]  # Забойное давление
time = GetInfoFromExcel().to_numpy(float)[:, 2]  # Время закачки
debit = GetInfoFromExcel().to_numpy(float)[:, 3]  # Закачка


def ChoosePressure(pressurePA):
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


def FirstGraphic(pressure, alltime, debit):
    ChosenPressure = ChoosePressure(pressure)
    a = ChosenPressure[0]
    b = ChosenPressure[1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=alltime, y=a, name='Давление-от времени'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=alltime, y=debit, name='Закачка-от времени'),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="График закачки-давления от времени"
    )
    if b == 1:
        fig.update_xaxes(title_text="Время, сек")
        fig.update_yaxes(title_text="<b>Давление,</b> Па", secondary_y=False)
        fig.update_yaxes(title_text="<b>Закачка</b> м3/c", secondary_y=True, range=[0, max(debit) * 9])
    elif b == 2:
        fig.update_xaxes(title_text="Время, сек")
        fig.update_yaxes(title_text="<b>Давление,</b> МПа", secondary_y=False)
        fig.update_yaxes(title_text="<b>Закачка</b> м3/c", secondary_y=True, range=[0, max(debit) * 9])
    elif b == 3:
        fig.update_xaxes(title_text="Время, сек")
        fig.update_yaxes(title_text="<b>Давление,</b> атм", secondary_y=False)
        fig.update_yaxes(title_text="<b>Закачка</b> м3/c", secondary_y=True, range=[0, max(debit) * 9])
    fig.show()


def SecondGraphic(hornerTime, pressure):
    ChosenPressure = ChoosePressure(pressure)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hornerTime, y=ChosenPressure[0], name='Давление-от времени'))
    fig.update_layout(
        title_text="График Давление-Время Хорнера")
    if ChosenPressure[1] == 1:
        fig.update_yaxes(title_text="<b>Давление,</b> Па", range=[0, max(ChosenPressure[0]) * 1.2])
    elif ChosenPressure[1] == 2:
        fig.update_yaxes(title_text="<b>Давление,</b> МПа", range=[0, max(ChosenPressure[0]) * 1.2])
    elif ChosenPressure[1] == 3:
        fig.update_yaxes(title_text="<b>Давление,</b> атм", range=[0, max(ChosenPressure[0]) * 1.2])
    fig.update_xaxes(title_text="<b>Время Хорнера</b>, безразмерное", range=[0, max(hornerTime) * 1.5])
    fig.show()


def ThirdGraphic(DimensTime, DimensPressure, dPWDtodTD, exponental):
    DimensTime.pop(0)
    DimensPressure.pop(0)
    plt.plot(DimensTime, DimensPressure, DimensTime, dPWDtodTD, DimensTime, exponental)
    plt.semilogx()
    plt.semilogy()
    plt.grid(True)
    plt.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=DimensTime, y=DimensPressure, name='<b>Безразмерное давление - безразмерное время</b>'))
    fig.add_trace(go.Scatter(x=DimensTime, y=dPWDtodTD, name='<b>dPWD/dTd - безразмерное время</b>'))
    fig.add_trace(go.Scatter(x=DimensTime, y=exponental, name='<b>dPWD/dTd(эксп.сгл.) - безразмерное время</b>'))
    fig.update_layout(title_text='Итоговые графики')
    fig.update_yaxes(type='log')
    fig.update_xaxes(type='log')
    fig.show()
