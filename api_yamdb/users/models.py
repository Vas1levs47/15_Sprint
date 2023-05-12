from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ROLES = [
    ('admin', 'ADMIN'),
    ('moderator', 'MODERATOR'),
    ('user', 'USER'),
]

USERNAMEVALIDATORSET = RegexValidator(regex=r'^[\w.@+-]+$')


class User(AbstractUser):
    bio = models.TextField(max_length=1000, blank=True)
    role = models.CharField(max_length=16, choices=ROLES, default='user')
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150,
                                validators=[USERNAMEVALIDATORSET, ])
    confirmation_code = models.CharField(max_length=50, null=True,
                                         blank=False, default=None)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
