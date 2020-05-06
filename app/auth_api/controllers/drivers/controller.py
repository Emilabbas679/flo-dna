import uuid
from random import randint

from app.data.models import Registration


def verify_phone_number(data):
    country_code = data['country_code']
    number = data['number']
    phone_number = f'{country_code}{number}'
    code = randint(100000, 999999)

    r = Registration.create(phone_number=phone_number, code=code)
    response = {
        'verification_id': r.id,
        'code': str(code)
    }
    return response


def verify_code(data):
    verification_id = data['verification_id']
    code = data['sms_code']
    driver = Registration.get(id=verification_id)
    if code == driver.code:
        response = {
            'verification_id': driver.id,
            'code': str(code)
        }
    else:
        response = {
            "error": "Code doesn't match"
        }
    return response


def setup_account(data):
    verification_id = data['verification_id']
    account_data = data['account_data']
    # TODO: create Driver in DB
    return


operations = {
    'phone_number': verify_phone_number,
    'code': verify_code,
    'account': setup_account,
}


def post(body):
    step = body['step']
    operation = operations[step]
    return operation(body)
