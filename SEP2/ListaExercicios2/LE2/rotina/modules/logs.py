# 25/07/24 - Lucas Xavier de Morais 
# Programa de logs
# SEP II - Engenharia Elétrica (UFSJ)
import os
from datetime import datetime

def getLogNumber():
    files = [f for f in os.listdir('logs/') if f.split('.')[-1] == 'log']
    maxLog = 0
    for f in files:
        logN = f.split('_')[1]
        logN = logN.split('.')[0]
        logN = int(logN)
        if logN > maxLog: maxLog = logN
    return maxLog

def createNewFile():
    number = str(getLogNumber() + 1)
    if len(number) == 1: number = '0' + number
    file = f'logs/log_{number}.log'
    with open(file, 'w') as f:
        f.write(f'{60*"-"}\n')
        f.write(f'Novo arquivo log {number}\n')
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{now}\n')
        f.write(f'{60*"-"}\n')

def log(message, status):
    number = str(getLogNumber())
    if len(number) == 1: number = '0' + number
    file = f'logs/log_{number}.log'
    with open(file, 'a') as f:
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{now} | {status} | {message}\n')



