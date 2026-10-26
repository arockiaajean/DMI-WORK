from pynput import mouse
import time
import json

# LOAD FILE
with open("mouse_actions.json", "r") as f:
    actions = json.load(f)

controller = mouse.Controller()

print("Replaying in 3 seconds...")
time.sleep(3)

for i, action in enumerate(actions):
    if i > 0:
        delay = action[-1] - actions[i-1][-1]
        time.sleep(delay)

    if action[0] == "move":
        _, x, y, _ = action
        controller.position = (x, y)

    elif action[0] == "click":
        _, x, y, button, pressed, _ = action
        controller.position = (x, y)

        # Convert string back to button
        if "left" in button:
            btn = mouse.Button.left
        elif "right" in button:
            btn = mouse.Button.right
        else:
            btn = mouse.Button.middle

        if pressed:
            controller.press(btn)
        else:
            controller.release(btn)

    elif action[0] == "scroll":
        _, x, y, dx, dy, _ = action
        controller.scroll(dx, dy)

print("Replay finished.")
