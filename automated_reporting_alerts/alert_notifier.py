import smtplib
from email.message import EmailMessage
from pathlib import Path


# this function sends automated emails with file attachments
def send_email_with_attachment(filename):
    message = EmailMessage()

    # set up email metadata
    message["From"] = "[EMAIL_ADDRESS]"
    message["To"] = "[EMAIL_ADDRESS]"
    message["Subject"] = "Daily USD Rates"

    message.set_content("Here is the daily USD rates report")

    file_path = Path(filename)

    # open and read the file in binary mode for the attachment
    with open(file_path, "rb") as file:
        content = file.read()

    # attach the excel file 
    message.add_attachment(
        content,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=file_path.name,
    )

    try:
        # connect to the gmail server 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("[EMAIL_ADDRESS]", "APP_PASSWORD")
            smtp.send_message(message)

    except smtplib.SMTPException as e:
        print(f"failed to send email: {e}")