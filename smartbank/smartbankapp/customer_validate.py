import json
import string
import random
import datetime


def validate_customer(body_data):
    name = body_data.get('name')
    address = body_data.get('address')
    city = body_data.get('city')
    state = body_data.get('state')

    validate_none = ['',None]
    if city in validate_none or not isinstance(city,str):
        return False,"City"
    elif state in validate_none or not isinstance(state,str):
        return False,"State"
    elif name in validate_none or not isinstance(name,str):
        return False,'Name'
    elif address in validate_none or not isinstance(address,str):
        return False,'Address'
    else:
        return True,''


def check_user(request):
    user = request.user
    if user.is_authenticated:
        return user
    else:
        return False


def generate_account_number():
    date = datetime.date.today()

    prefix = "CUS"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}{suffix}{date.year}{date.day}"
