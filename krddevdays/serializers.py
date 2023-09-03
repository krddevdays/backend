from rest_framework import serializers


class EnumField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj].name
