from pynput import keyboard
import time

pressed = 0
array = []

def on_press(key):
    global pressed
    try:
        pressed = 1
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global pressed
    pressed = 0
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    for i in range(100):
        array.append(pressed)
        time.sleep(0.1)
    print(array)
    listener.join()


# ...or, in a non-blocking fashion:
# listener = keyboard.Listener(on_press=on_press,on_release=on_release)
# listener.start()
