from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django_otp.oath import TOTP
from django_otp.util import random_hex, hex_validator
from django_otp.models import Device
from binascii import unhexlify
from .models import User
import time


class OTPVerifier():
    key = random_hex(20)
    time = time.time()
    digits = 6
    verified = models.BooleanField(default=False)
    lasttotpt = -1
    TokenValidityTime = 40

    def setuser(self, username):
        self.user = User.object.get(username=username)

    # def __bin_key__(self):
    #     return unhexlify(self.key.encode())

    def GenerateToken(self):
        totp_obj = TOTP(key=self.key, step=self.TokenValidityTime,
                        digits=self.digits)
        totp_obj.time = time.time()
        token = str(totp_obj.token())
        print(token)
        mail = 'Hello, ' + self.user.name + '. Your OTP is: ' + token
        send_mail('OTP', mail, 'otpverifier80@gmail.com', [self.user.email], fail_silently=False)
        return token

    def VerifyToken(self, token, tolerance=0):
        totp_object = TOTP(key=self.key, step=self.TokenValidityTime,
                        digits=self.digits)
        totp_object.time = time.time()
        if (totp_object.t() <= self.lasttotpt):
            self.verified = False
        elif (totp_object.verify(token, tolerance=tolerance)):
            self.lasttotpt = totp_object.t()
            self.verified = True
        return self.verified
