import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURATION ===
file_a = r"C:\Users\USER\Documents\A.xlsx"   # File A: contains student_no, email
file_b = r"C:\Users\USER\Documents\B.xlsx"    # File B: contains student_no, result
email_col = "email"        # Column name for email in File A
student_col = "student_no" # Common column between both files
result_col = "result"      # Column name for result in File B

# Your email settings
smtp_server = "smtp.gmail.com"
smtp_port = 587
your_email = "arockiaajeanconstan@gmail.com"
your_password = "txmv vwnq efyu zpyn"  # Use app password, not real Gmail password

# === READ EXCEL FILES ===
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b)

# Merge data on student number
df = pd.merge(df_a, df_b, on=student_col, how="inner")

# === SEND EMAILS ===
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(your_email, your_password)

for index, row in df.iterrows():
    student_no = row[student_col]
    email = row[email_col]
    result = row[result_col]

    subject = f"Your Exam Result - {student_no}"
    body = f"""
    Dear Student {student_no},

    The formate is: MODULE CODE / CA / SE / TOTAL / GRADE
    IF THE GRADE IS "F" THEN ITS FAIL.
    
    Your result is: {result}
    # THIS IS A COMPUTER GENERATED MAIL. PLEASE DON'T REPLY.
    """

    # Create email
    msg = MIMEMultipart()
    msg["From"] = your_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server.sendmail(your_email, email, msg.as_string())
        print(f"✅ Sent result to {student_no} ({email})")
    except Exception as e:
        print(f"❌ Failed to send to {student_no} ({email}): {e}")

server.quit()
