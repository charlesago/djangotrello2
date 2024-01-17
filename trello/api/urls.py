from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from trello import views

urlpatterns = [
    # user paths
    path('register', views.create_user, name='createUser'),

    # workspaces paths
    path('index', views.index, name='index'),
    path('workspace/create', views.create_workspace, name='createWorkspace'),
    path('workspace/edit/<str:id>', views.edit_workspace, name='editWorkspace'),
    path('workspace/delete/<str:id>', views.delete_workspace, name='deleteWorkspace'),

    # board paths
    path('board/show/<str:id>', views.show_board, name='showBoard'),
    path('board/create/<str:id>', views.create_board, name='createBoard'),
    path('board/edit/<str:id>', views.edit_board, name='editBoard'),
    path('board/delete/<str:id>', views.delete_board, name='deleteBoard'),

    # list paths
    path('list/show/<str:id>', views.show_list, name='showList'),
    path('list/create/<str:id>', views.create_list, name='createList'),
    path('list/edit/<str:id>', views.edit_list, name='editList'),
    path('list/delete/<str:id>', views.delete_list, name='deleteList'),

    # card paths
    path('card/show/<str:id>', views.show_card, name='showCard'),
    path('card/create/<str:id>', views.create_card, name='createCard'),
    path('card/edit/<str:id>', views.edit_card, name='editCard'),
    path('card/delete/<str:id>', views.delete_card, name='deleteCard'),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]