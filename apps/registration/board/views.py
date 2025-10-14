from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Board
from .serializers import BoardSerializer, BoardOptionSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def board_list(request):
    """
    Get all boards for dropdown selection
    """
    try:
        boards = Board.objects.all().order_by('board_name')
        serializer = BoardOptionSerializer(boards, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'Boards retrieved successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error retrieving boards: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def board_detail(request, pk):
    """
    Get board details by ID
    """
    try:
        board = get_object_or_404(Board, pk=pk)
        serializer = BoardSerializer(board)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'Board details retrieved successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error retrieving board details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def board_options(request):
    """
    Get board options formatted for frontend dropdown
    Returns array of objects with {id, name, value} structure
    """
    try:
        boards = Board.objects.all().order_by('board_name')
        serializer = BoardOptionSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error retrieving board options: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)