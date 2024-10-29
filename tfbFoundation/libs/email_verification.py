#----------NECESSARY MODULE,FILE,CODE IMPORT----------
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import random

#----------EMAIL VERIFICATION LINK GENERATE START----------
# def email_verification_link(user):
#     token = default_token_generator.make_token(user)
#     user_id = urlsafe_base64_encode(force_bytes(user.pk))
#     verification_link = f'{backend_live_link}/account/active/{user_id}/{token}'
#     return verification_link
#----------EMAIL VERIFICATION CODE GENERATE END----------
def email_verification_code(user):
    user_id = str(user.id)
    random_num = str(random.randint(1000,9999)) + user_id
    verification_code = random_num[-5:]
    #update user code_verification field
    profile = user.profile
    profile.verification_code = verification_code
    profile.save()
    return verification_code
#----------EMAIL VERIFICATION CODE GENERATE START----------

#----------EMAIL SENDING START----------
def send_verification_code(user):
    verification_code = email_verification_code(user)
    mail_subject = 'Verification Code'
    mail_body = render_to_string('email_verification.html', {'verification_code':verification_code})
    send_mail = EmailMultiAlternatives(mail_subject, '', to=[user.email])
    send_mail.attach_alternative(mail_body, 'text/html')
    send_mail.send()
    return verification_code
#----------EMAIL SENDING END----------