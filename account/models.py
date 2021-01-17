from django.db import models
from django.db.models.constraints import UniqueConstraint

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

username_validator = UnicodeUsernameValidator()

class user(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    username = models.CharField(
        'username',
        max_length=150,
        validators=[username_validator],
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta(AbstractUser.Meta):
        constraints = [
            #UniqueConstraint(fields=['room', 'date'], name='unique_booking'),
        ]
