# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ

import plugins.DoorChecker as dc

# @respond_to('string')     bot宛のメッセージ
# message.reply('string')   @発言者名: string でメッセージを送信

@respond_to('閉まってる？')
def mention_func(message):
    Door_State = dc.GetDoorState("/dev/ttyUSB0")
    print(Door_State)
    if Door_State == 1:
        message.reply('ドアの鍵は閉まっています') # メンション
    elif Door_State == 2:
        message.reply('ドアの鍵が開いています！') # メンション
    else:
        message.reply('わかりません') # メンション

@respond_to('今日の天気')
def weather(message):
    import urllib
    import json

    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='
    # '270000'とすると大阪の情報を取得してくれる
    # '130010'とすると東京の情報を取得してくれる
    # ここを変えれば任意の地域の天気情報を取得できる
    city_id = '270000'
    html = urllib.request.urlopen(url + city_id)
    jsonfile = json.loads(html.read().decode('utf-8'))
    title = jsonfile['title'] 
    telop = jsonfile['forecasts'][0]['telop']
    #temperature = jsonfile['forecasts'][0]['temperature']
    #仕様　json http://weather.livedoor.com/weather_hacks/webservice
    #telopが晴れだったら晴れのスラックのアイコンとか場合分け
    telop_icon = ''
    if telop.find('雪') > -1:    
        telop_icon = ':showman:'
    elif telop.find('雷') > -1:
        telop_icon = ':thinder_cloud_and_rain:'
    elif telop.find('晴') > -1:
        if telop.find('曇') > -1:
            telop_icon = ':partly_sunny:'
        elif telop.find('雨') > -1:
            telop_icon = ':partly_sunny_rain:'
        else:
            telop_icon = ':sunny:'
    elif telop.find('雨') > -1:
        telop_icon = ':umbrella:'
    elif telop.find('曇') > -1:
        telop_icon = ':cloud:'
    else:
        telop_icon = ':fire:'
    text = title + '\n' + '今日の天気　' + telop + telop_icon
    message.send(text) 