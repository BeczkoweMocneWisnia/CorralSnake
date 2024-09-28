import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from CorralSnake.utils import uuid_upload_to
from user.managers import CustomUserManager


USER_ROLES = {
    "Teacher": "Teacher",
    "Student": "Student",
    "Other": "Other",
}


class User(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, editable=False)
    pfp = models.ImageField(upload_to=uuid_upload_to('pfps'), default='defaults/pfps/default.png')
    username = models.CharField(null=False,
                                blank=False,
                                max_length=150,
                                unique=True,
                                editable=False,
                                validators=[UnicodeUsernameValidator()])
    role = models.CharField(null=False, blank=False, choices=USER_ROLES, max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def delete(self, using=None, keep_parents=False):
        if self.pfp.name != self.pfp.field.default:
            self.pfp.delete()

        return super().delete(using, keep_parents)