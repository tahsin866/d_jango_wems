from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'board_name']
        read_only_fields = ['id']


class BoardOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for board options to be used in dropdowns
    Returns both id and board_name for frontend compatibility
    """
    value = serializers.CharField(source='board_name', read_only=True)
    name = serializers.CharField(source='board_name', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'value', 'name']
        read_only_fields = ['id']