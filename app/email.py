# third party service mailer , fake call printing code.
async def send_email(email : str, verification_code : str):
    print("Start send email")
    sender = "Dailymotion Team"
    receiver = email

    message = f"""\
    Subject: Verification code Dailymotion 
    To: {receiver}
    From: {sender}

    Your code is : {verification_code} """

    print(message)