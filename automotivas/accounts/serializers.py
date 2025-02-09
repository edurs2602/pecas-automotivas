from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True, help_text="Token JWT gerado para o usuário")

    class Meta:
        model = User
        # Inclui os campos que você deseja expor. Observe que 'password' é write_only.
        fields = ('id', 'username', 'email', 'user_type', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Cria um usuário e define a senha de forma segura.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

