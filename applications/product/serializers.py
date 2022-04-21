from rest_framework import serializers
from rest_framework.utils import representation

from applications.product.models import Image, Product, ProductReview, Likes, ProductFavourites# Rating
# from parser import main


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ProductImageSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'owner', 'name', 'description', 'price', 'category', 'images',)

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        product = Product.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(product=product, image=image)
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.review.all())
        # representation['rating'] = Rating.objects.filter(product=instance).count()
        # rev = ReviewSerializer(ProductReview.objects.filter(product=instance))
        # rev = instance.review.all()
        # rev = ReviewSerializer(product=rev)
        # print(rev)
        # print(instance) ################### question
        # print(representation['description'])
        representation['likes'] = Likes.objects.filter(product=instance).count()
        representation['review'] = ProductReview.objects.filter(product=instance).count()
        # print(representation['review'])

        return representation


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
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = ProductFavourites
        fields = "__all__"


# class RatingSerializers(serializers.ModelSerializer):
#     # owner = serializers.EmailField(required=False) # не обьязателньо к заполнению
#
#     class Meta:
#         model = Rating
#         fields = ('rating', ) # 'owner'



# class ParserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PhonesParser
#         fields = '__all__'


    # def create(self, request):
        # print('+++++++++++++++++++++++++++++++++++++++')
        # vacations = main()
        # print('---------------------------------------')
        # print(vacations)
        # title = vacations.get('title')
        # price = vacations.get('price')
        # image = vacations.get('image')
        # PhonesParser.objects.create(title=title, price=price, image=image)


    # def create(self, validated_data):
    #     requests = self.context.get('request')
    #     vacation = validated_data.get('title')
    #     if PhonesParser.objects.filter(title=vacation):
    #         return PhonesParser.objects.get(title=vacation)
    #
    #     else:
    #         return PhonesParser.objects.create(title=vacation)





