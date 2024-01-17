from rest_framework.serializers import ModelSerializer
from trello.models import *


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'name', 'description', ]


class ListSerializer(ModelSerializer):
    cards = CardSerializer(many=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'cards']


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()

        return user

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class WorkspaceCreateSerializer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'type']


class VisibilitySerializer(ModelSerializer):
    class Meta:
        model = Visibility
        fields = ['name']


class BoardSerializer(ModelSerializer):
    visibility = VisibilitySerializer(read_only=True)
    lists = ListSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'visibility', 'lists']


class BoardCreateSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', "visibility"]


class WorkspaceSerializer(ModelSerializer):
    owner = UserSerializer()
    members = UserSerializer(many=True)
    boards = BoardSerializer(many=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'type', 'owner', 'members', 'boards']