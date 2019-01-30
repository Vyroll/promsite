from rest_framework import viewsets
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer, GroupSerializer, PostSerializer, CommentSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsCreatorOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User, Group
from blogdemo.models import Post, Comment

from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication, JWTAuthentication,)
    permission_classes = (IsAdminUser,)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication, JWTAuthentication,)
    permission_classes = (IsAdminUser,)

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication, JWTAuthentication,)

    permission_classes = (IsCreatorOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            pub_date=timezone.now(),
        )

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication, JWTAuthentication,)
    permission_classes = (IsCreatorOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            pub_date=timezone.now(),
        )

@login_required
def GetTokenView(request):
    token = Token.objects.get(user=request.user)
    return HttpResponse(f"Your token: {token}")