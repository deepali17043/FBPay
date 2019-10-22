from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django_otp.oath import TOTP
from django_otp.util import random_hex, hex_validator
from django_otp.models import Device
from binascii import unhexlify
from .models import User
import time


class OTPVerifier(Device):
    key = models.CharField(
        max_length=20,
        default=random_hex(20).decode(),
        validators=[hex_validator],
        help_text="Hex-encoded secret key to generate totp tokens.",
        unique=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    lasttotpt = -1

    def __bin_key__(self):
        return unhexlify(self.key.encode())

    def generate_token(self):
        totp_obj = TOTP(key=self.__bin_key__, step=settings.TOTP_TOKEN_VALIDITIY,
                        digits=settings.TOTP_DIGITS, time=time.time())
        token = str(totp_obj.token()).zfill(settings.TOTP_DIGITS)
        mail = 'Hello, ' + self.user.username + '. Your OTP is: ' + token
        send_mail('OTP', mail, 'otpverifier80@gmail.com', [self.user.email], fail_silently=False)
        return token

    def verify_is_allowed(self, token, tolerance=0):
        totp_object = TOTP(key=self.__bin_key__, step=settings.TOTP_TOKEN_VALIDITIY,
                        digits=settings.TOTP_DIGITS, time=time.time())
        if (totp_object.t() <= self.lasttotpt):
            self.verified = False
        elif (totp_object.verify(token, tolerance=tolerance)):
            self.lasttotpt = totp_object.t()
            self.verified = True
            self.save()
        return self.verified


