from rest_framework import serializers
from .models import Post, Comment, Group, Follow, User
from rest_framework.exceptions import ValidationError

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment

        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.CharField(source='following.username')

    class Meta:
        fields = ('id', 'user', 'following', )
        model = Follow

    def validate(self, data):
        user = self.context['request'].user
        author = data['following']
        follow_user = User.objects.get(username=author['username'])
        get_following = Follow.objects.filter(user=user, following=follow_user)
        data['following'] = follow_user
        if get_following:
            raise ValidationError() 
        return data