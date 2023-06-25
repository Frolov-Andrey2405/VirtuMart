from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    '''
    Custom user model extending Django's AbstractUser
    '''
    image_url = models.URLField(blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    '''
    Model for email verification
    '''
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        """
        The __str__ function is a special function in Python classes.
        It's the function that's called when you use print() on an object, or convert it to a string.
        The __str__ method should return a string representation of the object.
        """
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        """
        The send_verification_email function sends an email to the user's email address with a link that they can click on to verify their account.
        The link is generated using Django's reverse function, which takes in the name of the URL pattern and any keyword arguments that are needed for it.
        In this case, we need both the user's email and verification code.
        """
        link = reverse(
            'users:email_verification', kwargs={
                'email': self.user.email,
                'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Account verification for {self.user.username}'
        message = 'To verify the account for {}, click on the link: {}'.format(
            self.user.email,
            verification_link
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        """
        The is_expired function checks to see if the expiration date has passed.
        If it has, then the function returns True. Otherwise, it returns False.

        """
        return True if now() >= self.expiration else False
