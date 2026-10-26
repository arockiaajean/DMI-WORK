import json
import time
from pynput import mouse, keyboard

events = []
start_time = time.time()
stop_recording = False

# Track pressed keys for combination detection
pressed_keys = set()

def get_time():
    return round(time.time() - start_time, 4)

# ---------------- MOUSE ----------------
def on_move(x, y):
    if stop_recording:
        return False
    events.append({
        "type": "mouse_move",
        "time": get_time(),
        "x": x,
        "y": y
    })

def on_click(x, y, button, pressed):
    if stop_recording:
        return False
    events.append({
        "type": "mouse_click",
        "time": get_time(),
        "x": x,
        "y": y,
        "button": str(button),
        "pressed": pressed
    })

def on_scroll(x, y, dx, dy):
    if stop_recording:
        return False
    events.append({
        "type": "mouse_scroll",
        "time": get_time(),
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy
    })

# ---------------- KEYBOARD ----------------
def on_press(key):
    global stop_recording

    pressed_keys.add(key)

    # Detect SHIFT + 2
    if (keyboard.Key.shift in pressed_keys or keyboard.Key.shift_l in pressed_keys or keyboard.Key.shift_r in pressed_keys):
        try:
            if key.char == '2':
                print("Stopping recording...")
                stop_recording = True
                return False
        except AttributeError:
            pass

    events.append({
        "type": "key_press",
        "time": get_time(),
        "key": str(key)
    })

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

    events.append({
        "type": "key_release",
        "time": get_time(),
        "key": str(key)
    })

# ---------------- START LISTENERS ----------------
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
)

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
)

print("Recording started... Press SHIFT + 2 to stop.")

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()  # Wait until stop key is pressed
mouse_listener.stop()

# ---------------- SAVE TO JSON ----------------
with open("recorded_events.json", "w") as f:
    json.dump(events, f, indent=4)

print("Recording saved to recorded_events.json")
