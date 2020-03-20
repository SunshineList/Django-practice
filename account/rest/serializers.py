from rest_framework import serializers

from account.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "last_login", "username", "first_name", "email", "is_staff", "is_active",
                  "date_joined", "type", "mobile", "gender", "birthday", "note",)
