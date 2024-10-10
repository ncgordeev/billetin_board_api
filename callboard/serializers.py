from rest_framework import serializers

from callboard.models import Ad, Review


class ReviewSerializers(serializers.ModelSerializer):
    """Сериализатор отзывов"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewChangeSerializers(serializers.ModelSerializer):
    """Сериализатор создания, изменения отзыва"""

    class Meta:
        model = Review
        fields = ('text', 'ad')


class AdRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра товара"""
    review_list = ReviewSerializers(source='review_set', many=True, read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра списка товаров"""

    class Meta:
        model = Ad
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор добавления, изменения товара"""

    class Meta:
        model = Ad
        fields = ('title', 'price', 'description')
