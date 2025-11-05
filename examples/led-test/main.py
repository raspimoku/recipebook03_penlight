import time
import neopixel
from machine import Pin

NUM_LEDS = 1
PIN_NUM = 6          # DI ピンに接続した GPIO ピン番号

np = neopixel.NeoPixel(Pin(PIN_NUM), NUM_LEDS)

np[0] = (255, 0, 0)  # 赤
np.write()
time.sleep(1)

np[0] = (0, 255, 0)  # 緑
np.write()
time.sleep(1)

np[0] = (0, 0, 255)  # 青
np.write()
time.sleep(1)

np[0] = (0, 0, 0)    # 消灯
np.write()
