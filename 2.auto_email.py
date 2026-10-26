#for official email id 
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Credentials
EMAIL = "cm_kitwe@dmiseu.edu.zm"
PASSWORD = "byow iijd spgp azmv"  # 16-digit app password

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Load Excel File
df = pd.read_excel("email.xlsx")

# Send Email Function
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"SUCCESS: Email sent to {to_email}")
    except Exception as e:
        print(f"FAILED: {to_email} ❌ Error: {e}")

# Loop Through Excel Rows
for index, row in df.iterrows():
    send_email(row["email"], row["subject"], row["body"])

