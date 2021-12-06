import random

from django.core.cache import cache


def verification_code_generator():
    return random.randint(11111, 99999)


def email_generator(email):
    subject = 'Verification email'
    verification_code = verification_code_generator()
    cache.set(email, verification_code, timeout=600)
    email_body = 'Please enter the code below to verify\n {}'.format(verification_code)

    email_data = {
        'subject': subject,
        'message': email_body,
        'recipient_list': [email],
    }
    return email_data
