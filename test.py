"""
                       _oo0oo_
                      o8888888o
                      88" . "88
                      (| -_- |)
                      0\  =  /0
                    ___/`---'\___
                  .' \\|     |// '.
                 / \\|||  :  |||// \
                / _||||| -:- |||||- \
               |   | \\\  -  /// |   |
               | \_|  ''\---/''  |_/ |
               \  .-\__  '-'  ___/-. /
             ___'. .'  /--.--\  `. .'___
          ."" '<  `.___\_<|>_/___.' >' "".
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
         \  \ `_.   \_ __\ /__ _/   .-` /  /
     =====`-.____`.___ \_____/___.-`___.-'=====
                       `=---=' 
"""
import json


test_str = """
{"UNO_R3":1,"Servo_Engine":1,"Potentiometer":1,"Keypad":1,"Button":2,"Number_LED":1,"Wire":1,"Thermistor":1,"Rheostat":2,"LED":1,"Breadboard":2,"USB_Cable":1,"LCD":1,"Remote":1}
"""

ys = json.loads(test_str)
for y in ys.values():
    print(y)
