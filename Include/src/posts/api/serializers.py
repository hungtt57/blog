from rest_framework.serializers import ModelSerializer

from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			# 'id',
			'title',
			# 'slug',
			'content',
			'publish'
		]



class PostDetailSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'title',
			'slug',
			'content',
			'publish'
		]


class PostListSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'id',
			'user',
			'title',
			'slug',
			'content',
			'publish'
		]

