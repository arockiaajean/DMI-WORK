from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

WELCOME_MSG = """Welcome to Safari Bus Booking.
Please enter the region code:

1 – Kasama
2 – Mpika
3 – Nakonde
4 – Chipata
5 – Livingstone
6 – Solwezi
7 – Kabwe
8 – Lusaka
9 – Mongu
"""

BUS_LIST = """Code | Bus         | Price (ZMW)
1    | Likili      | 450
2    | Scorpion    | 400
3    | Juldan      | 390
4    | Mbew        | 700
5    | Powertools  | 390

Send the money through Airtel:
0774678089
Name: Bobby

Once the transaction is completed,
you will receive a confirmation message automatically.
"""

# FIX → Use Service()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://web.whatsapp.com")

print("Scan the WhatsApp QR code...")
time.sleep(20)

last_msg = ""

def send_message(msg_box, text):
    for line in text.split("\n"):
        msg_box.send_keys(line)
        msg_box.send_keys(Keys.SHIFT + Keys.ENTER)
    msg_box.send_keys(Keys.ENTER)


while True:
    try:
        # open latest chat
        chats = driver.find_elements(By.XPATH, '//div[@data-tab="3"]')
        if chats:
            chats[0].click()
            time.sleep(1)

        msgs = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")]//span[@dir="ltr"]')
        if not msgs:
            continue

        user_msg = msgs[-1].text.strip()

        if user_msg == last_msg:
            continue

        last_msg = user_msg
        print("User:", user_msg)

        msg_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')

        if user_msg.lower() in ["hi", "hello", "start", "menu"]:
            send_message(msg_box, WELCOME_MSG)

        elif user_msg in ["1","2","3","4","5","6","7","8","9"]:
            send_message(msg_box, BUS_LIST)

        else:
            send_message(msg_box, WELCOME_MSG)

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        time.sleep(3)

