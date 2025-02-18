from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone 


from products.models import Product, Category, SizeVariant
from users.models import Profile,CartItems


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, data):
        email = data.get('email')
        user = User.objects.filter(username = email).exists()
        if user:
            raise serializers.ValidationError({'error': ['The user is already exists with this email']})
        return data

 
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['email'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', '')
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username = email, password=password)
        if user is None:
            raise serializers.ValidationError({'error' : 'Invalid credentials'})
        if not user.profile.is_email_varified:
            raise serializers.ValidationError({'error' : 'Please verify email!'})
        user.last_login = timezone.now()
        user.save()
        return user
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'slug']


class SizeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = ['size_name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    size_variant = SizeVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['uid','product_name', 'slug', 'category', 'price', 'product_description', 'color_variant', 'size_variant']
        depth = 2


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'profile_image']


    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('user', {})
        print(user_data)

        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

       
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()

        return instance

    
class CartItemSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source = 'product.uid')
    product_name = serializers.CharField(source = "product.product_name")
    size_variant = serializers.CharField(source='size_variant.size_name')
    total_price = serializers.SerializerMethodField() 
    unit_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['uid' ,'product_name', 'quantity', 'size_variant', 'total_price', 'unit_price']

    def get_total_price(self, obj):
        return obj.get_product_price() 
    
    def get_unit_price(self, obj):
        return obj.product.get_product_price_by_size(obj.size_variant.size_name)


class RUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']