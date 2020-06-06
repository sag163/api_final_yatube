
from .models import Post, Comment, Group, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, filters
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

# Create your views here.
class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group',]
  
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        
class CommentViewsSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def list(self, request, posts_pk):
        comment = Comment.objects.filter(post=posts_pk)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)
  
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class GroupViewsSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
    

class FollowViewsSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        user = self.request.user
        following = self.request.data.get('following')
        follow_user = User.objects.get(username=following)
        get_following = Follow.objects.filter(user=user, following=follow_user)
        if get_following:
            raise ValidationError() 
        serializer.save(user=user, following=follow_user)
        