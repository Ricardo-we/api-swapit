from rest_framework import serializers
from api.models import Product, User, ProductImage, ProductTags, UserContactInformation
from rest_framework.authtoken.models import Token
from dotenv import load_dotenv
import os
load_dotenv()

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        fields = ['id', 'username', 'email', 'phone_number', 'location', 'user_currency', 'is_superuser']
        model = User 

class ProductTagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductTags

class UserContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserContactInformation

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_product_images')
    tags = serializers.SerializerMethodField('get_product_tags')
    user_contact_info = serializers.SerializerMethodField('get_user_contact_information')
    currency = serializers.SerializerMethodField('get_user_currency')

    class Meta: 
        fields = '__all__'
        model = Product

    def get_product_images(self, obj):
        product_images = ProductImage.objects.filter(product=obj).all()
        return ProductImageSerializer(product_images, many=True).data
    
    def get_product_tags(self, obj):
        product_tags = obj.tags.all()
        return ProductTagsSerializer(product_tags, many=True).data
        # return product_tags

    def get_user_currency(self, obj):
        return obj.user.user_currency

    def get_user_contact_information(self, obj):
        user_contact_info = UserContactInformation.objects.filter(user=obj.user).all()
        return UserContactInfoSerializer(user_contact_info, many=True).data
        # return user_contact_info

class InRevisionProductsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")
    class Meta:
        fields = '__all__'
        model = ProductImage

    def get_image_url(self, obj):
        return f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_NAME')}/{obj.image}"    
    