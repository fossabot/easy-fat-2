from farm.models import UserFarmRelations
from django.contrib.auth.models import User
from django.db import models


class UserProfileManager(models.Manager):
    def get_profile_for_user(self, user):
        result = super().filter(user=user)
        if result.count() == 0:
            return super().create(user=user)
        elif result.count() == 1:
            return result[0]
        else:
            raise ValueError('User seems to have multiple profiles.')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField(default='Farmer', max_length=15)
    objects = UserProfileManager()

    @property
    def name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def role(self):
        return self.user_role

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
