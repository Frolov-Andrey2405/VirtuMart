import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    """
    The send_email_verification function sends an email to the user with a link that will verify their email address.
    The function takes in a user_id and uses it to find the corresponding User object. It then creates an EmailVerification
    object, which is used for tracking whether or not the user has verified their email address. The EmailVerification object
    is created with a unique code, expiration date 48 hours from now, and associated User object.
    """
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(
        code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
