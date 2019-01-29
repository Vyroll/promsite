from django.contrib.auth.models import User, Group
from rest_framework import serializers
from blogdemo.models import Post, Comment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='post-detail',
        read_only=True)
    comments = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='comment-detail',
        read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups','posts','comments')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class PostSerializer(serializers.HyperlinkedModelSerializer):
    pub_date = serializers.DateTimeField(read_only=True,)
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
    )
    comment_set = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='comment-detail',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('url', 'title', 'text', 'pub_date', 'creator','comment_set')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    pub_date = serializers.DateTimeField(read_only=True,)
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
    )
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='post-detail',
    )
    
    class Meta:
        model = Comment
        fields = ('url', 'text', 'pub_date', 'creator', 'post')
