from gpiozero import Button
from signal import pause
import time

def on_press():
    print("Button pressed")

def on_release():
    print("Button released")

button = Button(17)

button.when_pressed = on_press
button.when_released = on_release

while True:
 time.sleep(1)
#pause()  # Wait indefinitely for events
