from twilio.rest import Client
import random

account_sid = 'AC1cbeb4ea2483fe64e7683ecf717ae930'
auth_token = 'ab61a9169aae2db81c8f85e270ef87cd'
messaging_service_sid = ''


def generate_code():
    return str(random.randrange(100000, 999999))


def send_sms(to_number, body):
    client = Client(account_sid, auth_token)
    message = client.api.messages.create(to_number, messaging_service_sid=messaging_service_sid, body=body)

    return message


def send_whatsapp(to_number, body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your delhero code is {body}',
        from_='whatsapp:+14155238886',
        to='whatsapp:{}'.format(to_number)
    )

    return message
