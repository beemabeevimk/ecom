import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
client = Client("AC6a49ad30101cd267442a2b302c2aee1e", "b9a0bf927aae29580d545e2cfacac90f")
verify = client.verify.services("VA16e034b29f72d52c4e5d2e193ec109ab")


def send(phone):
    print(verify)
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'



