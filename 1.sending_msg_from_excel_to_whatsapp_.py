import pandas as pd
import pywhatkit as kit
import time

# Load Excel file
df = pd.read_excel(r"Book1.xlsx")  # change to your Excel file name

for i, row in df.iterrows():
    phone = str(row['Phone'])
    message = str(row['Message'])
    
    # Ensure phone number format (country code, no +)
    if not phone.startswith("+"):
        phone = "+" + phone
    
    print(f"Sending to {phone} ...")
    try:
        # Send instantly
        kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10, tab_close=True)
        time.sleep(8)  # small delay before next message
    except Exception as e:
        print(f"Failed to send to {phone}: {e}")

print("✅ All messages sent successfully.")

