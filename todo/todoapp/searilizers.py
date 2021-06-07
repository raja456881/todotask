from rest_framework import serializers
from.models import *

class todosearilizers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model=todoiteam
        fields=[ 'title', 'completed', "user"]

    def create(self, validated_data):
        todo=todoiteam(
        title=validated_data['title'],
        completed=validated_data['completed'],
        user = self.context['request'].user,
        is_roles='user'
        )
        todo.save()
        return todo






class adminsearilizers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name', 'username', 'email','password' ]

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user = User.objects.create_user(**validated_data,  is_admin=True,
                                        is_superuser=True, is_staff=True, is_roles='admin')
        stu1 = Admin.objects.create(user=user)
        return user
class usersearilizers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user = User.objects.create_user(**validated_data, is_admin=False,
                                        is_superuser=False, is_staff=True)
        return user