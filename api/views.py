from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import CartItemSerializer, ProfileSerializer, RUserSerializer, UserSerializer, LoginSerializer, ProductSerializer
from users.models import Cart, CartItems, Profile
from products.models import Product, SizeVariant


class RegisterAPIview(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data = data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message' : 'Registered successfully', 
                    'user' : {
                            'first_name' : user.first_name,
                            'last_name' : user.last_name,
                            'email' : user.email
                        },
                    'note' : 'Mail is sent to your mail please verify'
                    
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIview(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)

            response =  Response(
                {
                    'message': 'login successfully',
                    'data' : {
                        'refresh_token' : str(refresh_token),
                        'access_token': access_token
                    }
                }, status=status.HTTP_200_OK)
            
            response.set_cookie(
                'refresh_token', 
                refresh_token,
                max_age=timedelta(days=7),  # Expiry time for refresh token
                httponly=True,              # HttpOnly flag for security
                secure=True,                # Set this to True in production (requires HTTPS)
                samesite='None'             # Allows cross-site cookies (if required)
            )

            response.set_cookie(
                'access_token',
                access_token,
                max_age=timedelta(minutes=15),  # Expiry time for access token (shorter lifespan)
                httponly=True,                  # HttpOnly flag for security
                secure=True,                    # Set this to True in production (requires HTTPS)
                samesite='None'                 # Allows cross-site cookies (if required)
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateProfile(APIView):
    def post(self, request):
        email_token = request.data.get('email_token')
        if not email_token:
            return Response({'error' : 'email_token field is required'})
        try:
            profile = Profile.objects.get(email_token = email_token)
            profile.is_email_varified = True
            profile.save()
        except:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message' : 'Verified successfully'})


class ProfileAPIview(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = request.user.profile  
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class GetProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GetProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return generics.get_object_or_404(Product, slug=slug)


class ShowCartAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user, is_paid = False)
        except:
            cart = Cart.objects.create(user = user, is_paid = False)
        
        cart_items = CartItems.objects.filter(cart = cart)

        data = []

        for item in cart_items:
            serializer = CartItemSerializer(item)
            data.append(serializer.data)
        
        total_price ,discounted_price, subtotal_price  = cart.get_cart_total()
        
        return Response({'data' : data, 'subtotal_price' : subtotal_price, 'discounted_price' : discounted_price, 'total_price': total_price})
        


class AddItemToCartAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        uid = request.data.get('uid')
        size = request.data.get('size')

        if not uid:
            return Response({'uid':['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        
        cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
        product = Product.objects.filter(uid = uid)

        if not product.exists():
            return Response({'error' : ['product does not exists']}, status=status.HTTP_404_NOT_FOUND)
       

        if size:
            try:
                size_variant = SizeVariant.objects.get(size_name = size)
            except:
                return Response({'error' : ['size is not valid! enter valid size']}, status=status.HTTP_404_NOT_FOUND)

            cart_item = CartItems.objects.filter(cart = cart, product = product.first(), size_variant = size_variant)
            if cart_item.exists():
                cart_item = cart_item.first()
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
                return Response({'message' : f'Successfully {product.first().product_name} added to cart'}, status=status.HTTP_200_OK)
            else:
                cart_item = CartItems.objects.create(cart = cart, product = product.first(), size_variant = size_variant)
                return Response({'message' : f'Successfully {product.first().product_name} added to cart'}, status=status.HTTP_200_OK)
                

        cart_item = CartItems.objects.create(cart = cart, product = product.first())

        return Response({'message' : f'Successfully {product.first().product_name} added to cart'}, status=status.HTTP_200_OK)


class RemoveItemToCartAPIview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        uid = request.data.get('uid')
        size = request.data.get('size')
        if not uid:
            return Response({'uid':['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        if not size:
            return Response({'size':['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.filter(uid = uid)
        except:
            return Response({'error':['The product does not found']}, status=status.HTTP_404_NOT_FOUND)
        
        cart = Cart.objects.filter(user = user, is_paid = False)
        if not cart.exists():
            return Response({'error':['Cart does not exists.']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            size = SizeVariant.objects.get(size_name = size)
        except:
            return Response({'error':['size is not valid! enter valid size.']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cartItem = CartItems.objects.get(cart = cart.first(), product = product.first(), size_variant = size)
            cartItem.delete()

        except:
            return Response({'error' : ['Does not have that product in cart.']}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message' : f'Successfully {product.first().product_name} removed from'})
        


    
   



# AAPTxy8BH1VEsoebNVZXo8HurL4Rh7wIaTccHIcpldnDTqVK9vNWo2ajs1bEmSdfxo5nN-yhoO2NZtsXT5GoNy84GKmKPryiW-bBApkNTJjtzFQIOPhMV34W5JRZV3AMANWc1VyuL3hSHWB2v6UCCm6FkPYeCOYAsEdDE4ByBb9vkXJWxDno5RbBI3lzPQ5yTwUKrHsZHeVUYnk-Dy5vrsFJhEY2v4SchKElEUk2qchAln4.AT1_tpxgcRMN
   


     






