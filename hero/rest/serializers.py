from rest_framework import serializers

from hero.models import HeroModel


class HeroSerializer(serializers.ModelSerializer):
    gender = serializers.ReadOnlyField(source='get_gender_display')

    class Meta:
        model = HeroModel
        fields = ("id", "hero", 'gender', 'address', 'weizhi', 'taici')
