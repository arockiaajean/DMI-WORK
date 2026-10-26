from pynput import mouse
import time
import json

actions = []
recording = True

def on_move(x, y):
    if recording:
        actions.append(("move", x, y, time.time()))

def on_click(x, y, button, pressed):
    if recording:
        actions.append(("click", x, y, str(button), pressed, time.time()))
    if button == mouse.Button.right and not pressed:
        return False

def on_scroll(x, y, dx, dy):
    if recording:
        actions.append(("scroll", x, y, dx, dy, time.time()))

print("Recording... Right-click to stop.")
start_time = time.time()

with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()

# Normalize time
normalized_actions = []
for action in actions:
    new_action = list(action)
    new_action[-1] -= start_time
    normalized_actions.append(new_action)

# SAVE TO FILE
with open("mouse_actions.json", "w") as f:
    json.dump(normalized_actions, f, indent=4)

print("Saved to mouse_actions.json")
