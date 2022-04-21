from rest_framework import serializers
from rest_framework.utils import representation

from applications.product.models import Image, Product, ProductReview, Likes, ProductFavourites


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')    # это поле только для чтение(не обьязателньо заполнять)    || source='owner.email' = отображай email ownera
    images = ProductImageSerializers(many=True, read_only=True)      # чтобы обрабатывать несколько картин

    class Meta:
        model = Product
        fields = ('id', 'owner', 'name', 'description', 'price', 'category', 'images') # images = related name в модельках

    def create(self, validated_data): # переопределяем create он работает последним
        request = self.context.get('request') # получили файлы которые передали в запросе
        images_data = request.FILES # занесли в переменное
        product = Product.objects.create(**validated_data) # validated_data хранятся те данные которые указали помимо images
        for image in images_data.getlist('images'): # вытащи поля images
            Image.objects.create(product=product, image=image) # models
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.review.all())
        # print('dawwwwwwwwwwwwwwwwwwwwwwwwwwwww')

        # rev = ReviewSerializer(ProductReview.objects.filter(product=instance))
        # rev = instance.review.all()
        # rev = ReviewSerializer(product=rev)
        # print(rev)
        # print(instance) ################### question
        # print(representation['description'])

        representation['review'] = ProductReview.objects.filter(product=instance).count()
        print(representation['review'])

        return representation

        # data = super(ProductSerializer, self).to_representation(instance)
        # data.update(ReviewSerializer)
        # return data



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = "__all__"

    def to_representation(self, instance):
        ##like_representation
        total_likes = 0
        for i in instance.likes.all():
            total_likes += 1
            print(i)
        representation['likes'] = total_likes
        return representation


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFavourites
        fields = "__all__"
