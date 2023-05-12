from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Ресурс categories."""
    lookup_field = 'slug'

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Ресурс genres."""
    lookup_field = 'slug'

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleViewSerializer(serializers.ModelSerializer):
    """Ресурс titles. Отображение."""
    category = CategorySerializer(required=True)
    genre = GenreSerializer(required=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class TitleEditSerializer(serializers.ModelSerializer):
    """Ресурс titles. Модификация."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        required=True, many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Ресурс reviews."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        review = Review.objects.filter(
            title=title_id, author=user).exists()
        if self.context['request'].method == 'POST' and review:
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data

    class Meta:
        fields = ('id', 'text', 'score', 'pub_date', 'author')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Ресурс comments."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author')
        model = Comment
