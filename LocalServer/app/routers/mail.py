# app/routers/mail.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(tags=["mail"])

class MailRequest(BaseModel):
    smtp_server: str
    smtp_port: int = 587
    username: str
    password: str
    to: EmailStr
    subject: str
    body: str

@router.post("/send-mail", summary="Send email via SMTP")
def send_mail(req: MailRequest):
    msg = MIMEMultipart()
    msg["From"] = req.username
    msg["To"] = req.to
    msg["Subject"] = req.subject
    msg.attach(MIMEText(req.body, "plain", "utf-8"))
    try:
        with smtplib.SMTP(req.smtp_server, req.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(req.username, req.password)
            server.sendmail(req.username, [req.to], msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": "success"}
