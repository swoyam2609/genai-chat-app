from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
from dependencies import mongo
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import key

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email: str):
    with open("dependencies/html/sifra-signup.html", "r") as file:
        html_content = file.read()
    otp = generate_otp()
    html_content = html_content.replace("123456", f"{otp}")
    expiration_time = datetime.utcnow() + timedelta(minutes=5)
    mongo.db.pendingusers.update_one({"email": email},{"$set": {"otp": otp, "expiration_time": expiration_time}},upsert=True)
    subject = 'OTP for Account Verification'
    body = f'Your OTP for password reset is: {otp}'
    email_user = key.EMAIL_LOGIN
    email_password = key.EMAIL_PASS
    msg = MIMEMultipart()
    msg['From'] = key.EMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content,'html'))
    try:
        with smtplib.SMTP(key.EMAIL_SERVER, 587) as server:
            server.starttls()
            server.login(email_user, email_password)

            # Sending the email
            server.sendmail(key.EMAIL_USER, [email], msg.as_string())

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        print(f"Error sending OTP to {email}: {e}")

def send_otp_reset(email: str):
    with open("dependencies/html/sifra-reset.html", "r") as file:
        html_content = file.read()
    otp = generate_otp()
    html_content = html_content.replace("123456", f"{otp}")
    expiration_time = datetime.utcnow() + timedelta(minutes=5)
    mongo.db.pendingusers.update_one({"email": email},{"$set": {"otp": otp, "expiration_time": expiration_time}},upsert=True)
    subject = 'OTP for Account Verification'
    body = f'Your OTP for password reset is: {otp}'
    email_user = key.EMAIL_LOGIN
    email_password = key.EMAIL_PASS
    msg = MIMEMultipart()
    msg['From'] = key.EMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content,'html'))
    try:
        with smtplib.SMTP(key.EMAIL_SERVER, 587) as server:
            server.starttls()
            server.login(email_user, email_password)

            # Sending the email
            server.sendmail(key.EMAIL_USER, [email], msg.as_string())

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        print(f"Error sending OTP to {email}: {e}")

def verify_otp(email: str, otp: str):
    pending_user = mongo.db.pendingusers.find_one({"email": email})
    if pending_user:
        if pending_user["otp"] == otp:
            if pending_user["expiration_time"] > datetime.utcnow():
                mongo.db.pendingusers.delete_one({"email": email})
                return True
            else:
                return JSONResponse(content={"message": "OTP expired"}, status_code=400)
        else:
            return JSONResponse(content={"message": "OTP is incorrect"}, status_code=400)
    else:
        return JSONResponse(content={"message": "Email not found"}, status_code=400)
    