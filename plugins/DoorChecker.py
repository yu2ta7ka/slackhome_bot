#!/usr/bin/python
# coding: UTF-8

###########################################################################
# TWE_Lite-2525Aから加速度データをMONOSTICKへ送信されるので、
# MONOSTICKが受信したデータを本プログラムで処理する。
# z軸の値を取得し、ドアの施錠状態を検知する。
#  z:51以上→open
#  z:50以下→close
# 第一引数：シリアルポート名（ubuntu例:/dev/ttyUSB0）
###########################################################################

#パッケージのimport
import time
import concurrent.futures
from serial import *
from sys import stdout, stdin, stderr, exit
from time import sleep

#0:null 1:close 2:open
Door_State = 0

#ドアの施錠状態を監視する
def WatchDoorState():
    global Door_State
    print("WatchDoorState")
    # シリアルポートを開く ボーレート：115200
    try:
        ser = Serial("/dev/ttyUSB0", 115200)
        print("open serial port: /dev/ttyUSB0")
    except:
        print("cannot open serial port: /dev/ttyUSB0")
        exit(1)

    Counter = 0

    # データを１行ずつ解釈し続ける
    while True:
        coordinate = []
        line_array = []
        line = ser.readline().rstrip() # １ライン単位で読み出し、末尾の改行コードを削除（ブロッキング読み出し）
        line_str = line.decode() #バイナリなので文字列へエンコード
        try: 
            line_array = line_str.split(":")
        except TypeError:
            print("TypeError: %s" % line)

        #加速度データを受信した場合処理する
        if len(line_array) > 3:
            #x,y,zの値を取得する
            for index in range(10,13):
                coordinate.append(line_array[index].split("=")[1])
            
        if len(coordinate) == 3:
            #z値：lockが100くらい、openが0付近
            print(int(coordinate[2]))
            if int(coordinate[2]) > 50:
                print("The door is close ")
                Door_State = 1
            else:
                print("The door is open")
                Door_State = 2
            Counter = 0

#施錠状態検知関数のスレッドを起動する
def StartDoorChecker():
    print("Start_DoorChecker")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    executor.submit(WatchDoorState)

#施錠状態を返す
def GetDoorState():
    print("DoorState: %d " % Door_State)
    return Door_State


