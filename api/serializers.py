from rest_framework import serializers
from .models import *
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class StudentClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = "__all__"

    def validate(self, data):
        try:
            if StudentClass.objects.filter(cls_name=data.get('cls_name')).exists():
                raise serializers.ValidationError('Student Class Name Should be Unique.')
            return data
        except Exception as err:
            raise serializers.ValidationError({'error': err.args[0]})

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            return instance
        except Exception as err:
            raise serializers.ValidationError({'error': str(err)})


class UserSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    # cls = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'mobile', 'first_name', 'last_name', 'password', 'confirm_password', 'cls', 'image', 'dob',
            'is_inactive',)

    def validate(self, data):
        try:
            if User.objects.filter(mobile=data.get('mobile')).exists():
                raise serializers.ValidationError('User Mobile Number Already Exists.')

            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError('Password Does not matched.')
            return data
        except Exception as err:
            raise serializers.ValidationError({'error': err.args[0]})

    def validate_cls(self, data):
        try:
            std_cls = StudentClass.objects.get(id=data.id)
        except ObjectDoesNotExist:
            raise Http404
        return std_cls

    def get_cls(self, obj):
        try:
            return getattr(obj.cls, 'cls_name', None)
        except AttributeError:
            return None

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        is_inactive = validated_data['is_inactive']
        instance.is_inactive = is_inactive
        instance.save()
        return instance


class UserLoginSerializers(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=15, validators=[validate_mobile_number])
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "mobile",
            'password',
        )

    def validate(self, data):
        mobile_number = data.get('mobile')
        password = data.get('password')
        if not User.objects.get(mobile=mobile_number).is_inactive:
            raise serializers.ValidationError('User Still Deactivated.You should wait for the activation.')

        user = authenticate(self.context.get('request'), mobile=mobile_number, password=password)

        if not user:
            raise AuthenticationFailed('Invalid mobile number or password')

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class StudentUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'email',
            'cls',
            'dob',
        )

    def validate(self, data):
        for field_name in ['image', 'first_name', 'last_name', 'email', 'cls', 'dob']:
            if field_name not in data:
                raise serializers.ValidationError(f"This fields `{field_name}` is required.")
        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
