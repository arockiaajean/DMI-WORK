import os

network = "192.168.1."

for i in range(1, 255):
    ip = network + str(i)
    response = os.system(f"ping -n 1 -w 100 {ip} > nul")  # Windows

    if response == 0:
        print(f"{ip} is up")
