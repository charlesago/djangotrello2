from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trello.api.serializers import *
from trello.models import Workspace, Board, List, Card

from trello.api.serializers import CardSerializer


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User registered  successfully',
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
    return Response("something went wrong", status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    workspaces = Workspace.objects.all()
    serialized_workspaces = WorkspaceSerializer(workspaces, many=True)

    return Response(serialized_workspaces.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_workspace(request):
    workspace = WorkspaceCreateSerializer(data=request.data)
    if workspace.is_valid():
        workspace.save(owner=request.user, members=[request.user])
        return Response(workspace.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_workspace(request, id):
    workspace = get_object_or_404(Workspace, id=id)
    if workspace.owner != request.user:
        return Response("Vous n'êtes pas le propriétaire de cette workspace", status=status.HTTP_403_FORBIDDEN)
    workspace_serialized = WorkspaceSerializer(data=request.data, instance=workspace)
    if workspace_serialized.is_valid():
        workspace_serialized.save()
        return Response(workspace_serialized.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_workspace(request, id):
    workspace = get_object_or_404(Workspace, id=id)
    if workspace.owner != request.user:
        return Response("Vous n'êtes pas le propriétaire de cette workspace", status=status.HTTP_403_FORBIDDEN)
    workspace.delete()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_board(request, id):
    board = get_object_or_404(Board, id=id)
    serialized_board = BoardSerializer(board)
    return Response(serialized_board.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_board(request, id):
    if request.method == 'POST':
        workspace = get_object_or_404(Workspace, id=id)
        board = BoardCreateSerializer(data=request.data)
        if board.is_valid():
            board.save(members=[request.user], workspace=workspace)
            return Response(board.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_board(request, id):
    board = get_object_or_404(Board, id=id)
    if not board.members.filter(id=request.user.id).exists():
        return Response("Vous n'êtes pas membre de ce tableau", status=status.HTTP_403_FORBIDDEN)
    board_serialized = BoardCreateSerializer(data=request.data, instance=board)
    if board_serialized.is_valid():
        board_serialized.save()
        return Response(board_serialized.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_board(request, id):
    board = get_object_or_404(Board, id=id)
    if board is not None:
        if not board.members.filter(id=request.user.id).exists():
            return Response("Vous n'êtes pas membre de ce tableau", status=status.HTTP_403_FORBIDDEN)
    board.delete()
    return Response("Supprimé avec success", status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_list(request, id):
    list_showed = get_object_or_404(List, id=id)
    serialized_list = ListSerializer(list_showed)
    return Response(serialized_list.data, status=status.HTTP_200_OK)


# Ask for a board id
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_list(request, id):
    board_list = ListSerializer(data=request.data)
    if board_list.is_valid():
        board_list.save(board=get_object_or_404(Board, id=id))
        return Response(board_list.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_list(request, id):
    edited_list = get_object_or_404(List, id=id)
    list_serialized = ListSerializer(edited_list, data=request.data)
    if list_serialized.is_valid():
        list_serialized.save()
    return Response(list_serialized.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_list(request, id):
    removed_list = get_object_or_404(List, id=id)
    removed_list.delete()
    return Response("votre liste a bien été supprimée et placée dans la liste archivée",status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_card(request, id):
    card = get_object_or_404(Card, id=id)
    serialized_card = CardSerializer(card)
    return Response(serialized_card.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_card(request, id):
    card = CardSerializer(data=request.data)
    if card.is_valid():
        card.save(list=get_object_or_404(List, id=id))
        return Response(card.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_card(request, id):
    card = get_object_or_404(Card, id=id)
    card_serialized = CardSerializer(card, data=request.data)
    if card_serialized.is_valid():
        card_serialized.save()
    return Response(card_serialized.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_card(request, id):
    card = get_object_or_404(Card, id=id)
    card.delete()
    return Response("votre carte a bien été supprimée", status=status.HTTP_200_OK)


# pouvoir envoyer des requetes pour rejoindre des workspaces et des tableaux
# voir la liste archivée/ajouter items dans la liste archivée