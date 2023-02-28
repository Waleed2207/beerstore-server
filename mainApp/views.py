from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserProfileSerializer, ProductsSerializer, SuppliersSerializer, OrdersSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .models import UserProfile, Products, Suppliers, Orders
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login


@csrf_exempt
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid login credentials'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def getuser(self, request, pk=None):
        user = User.object.get(id=pk)
    @action (detail=True ,methods = ['GET'])
    def getUserID(self, request , pk =None):
        print("im here inside getUserID")
        user =request.user

        u = User.objects.fillter()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)
   # authentication_classes = (TokenAuthentication, )

   
    @action(detail=True, methods=['POST'])
   

    def createUserProfile(self, request, pk=None):
        print("inside create user profile")
        # get the given username
        username1 = request.data.get('user')
        givenUsername1 = request.data.get('username','')
        # get the values of first name, last name, email and user type
        givenFirstName = request.data.get('firstName', '')
        givenLastName = request.data.get('lastName', '')
        givenUserEmail = request.data.get('email', '')
        givenUserType = request.data.get('userType', '')
        
        # create the new user profile
        newUser = UserProfile.objects.create(
            user=username1, username=givenUsername1, firstName=givenFirstName,
            lastName=givenLastName, email=givenUserEmail, userType=givenUserType)
        print("user is: ", newUser)
        
        response = {'message': 'created', 'results': {'id': newUser.id}}
        return Response(response, status=status.HTTP_200_OK)

    # @action(detail = True, methods=['POST'])
    # def getUserTypeByUserID(self ,request,pk=None):
    #     userID = request.data['userID']
    #     username =request.data['username']
    #     arr = [userID,username]
    #     u = UserProfile.objects.get(username = arr[2])
    #     serializers = UserProfileSerializer(u, many=False)
    #     response = {'message': 'Get', 'results': serializers.data}
    #     print("response:", response)
    #     return Response(response, status=status.HTTP_200_OK)
    #

    @action(detail=True, methods=['POST'])
    def getUserByUsername(self, request, pk=None):
        username = request.data['username']
        arr = []
        u = UserProfile.objects.get(username=username)

        serializers = UserProfileSerializer(u, many=False)

        response = {'message': 'Get', 'results': serializers.data}
        print("response:", response)
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def getUserDetails(self, request, pk=None):
        print("im here")
        user = request.user
        print("user from query is: ", user)
        arr = []
        u = UserProfile.objects.get(user=user)
        # print("user mail is: ", u.email)
        print("user name is: ", u.firstName)
        print("user surname is: ", u.lastName)
        # userDetails= User.objects.filter(user=user.id, course=pk)
        # for userCourse in userCourses:
        u.username = user
        serializers = UserProfileSerializer(u, many=False)
        #     arr.append(serializers.data)

        response = {'message': 'Get', 'results': serializers.data}
        return Response(response, status=status.HTTP_200_OK)
    # samir:
    # def UpdateUserDetails(self, request, pk=None):
    #         print("im here")
    #         user = request.user
    #         print("user from query is: ",user)
    #         arr=[]
    #         u = UserProfile.objects.get(user=user)
    #         # print("user mail is: ", u.email)
    #         print("user name is: ", u.firstName)
    #         print("user surname is: ", u.lastName)
    #         u.username=user
    #         serializers = UserProfileSerializer(u, many=False)
    #         response = {'message': 'Get', 'results': serializers.data}
    #         return Response (response, status=status.HTTP_200_OK)

# update the user's profile details
    @action(detail=True, methods=['POST'])
    def UpdateUserDetails(self, request, pk=None):

        # get the user by the authentication
        user = request.user
        # if getUserProfile get a value (len(getUserProfile) > 0) it means that
        # this object exist in DB and the user is trying to update that object.
        getUserProfile = UserProfile.objects.filter(user=user.id)
        try:
            # success if need to update

            profile = UserProfile.objects.get(id=getUserProfile[0].id)
            print("aaabbb ", getUserProfile[0].id)
            profile.user = user
            # get the new details
            firstName = request.data['firstName']
            lastName = request.data['lastName']
            aboutMe = request.data['aboutMe']
            hobbies = request.data['hobbies']
            myGoal = request.data['myGoal']
            # insert the new details in the new object
            profile.firstName = firstName
            profile.lastName = lastName
            profile.aboutMe = aboutMe
            profile.hobbies = hobbies
            profile.myGoal = myGoal

            profile.save()
            print("new profile is: ", profile)
            serializers = UserProfileSerializer(profile, many=False)
            response = {'message': 'Updated', 'results': serializers.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            # requested profile not found in DB
            response = {'message': 'error'}
            return Response(response, status=status.HTTP_200_OK)


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = (AllowAny,)
    #authentication_classes = (TokenAuthentication, )
    #  Update or create a userLessons
    #permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def AddNewProduct(self, request):
        givenProductName = ' '
        givenSupplierName = ' '
        givenAmount = ' '
        givenPrice = ' '
       # if 'name' in request.data:
        givenProductName = request.POST.get('name')
        # if 'Supplier name' in request.data:
        givenSupplierName = request.POST.get('supplier_name')
        # if 'Amount' in request.data:
        givenAmount = request.POST.get('amount')
       # if 'Price' in request.data:
        givenPrice = request.POST.get('price')

        newProduct = Products.objects.create(
            name=givenProductName, supplier_name=givenSupplierName, amount=givenAmount, price=givenPrice)
        newProduct.save()
        print("Product is: ", newProduct)

        response = {'message': 'created', 'results': newProduct}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def getAllProducts(self, request, pk=None):
        print("im here")
        product = request.product
        print("product from query is: ", product)
        arr = []
        p = Products.objects.get(product=product)
        # print("user mail is: ", u.email)
        print("Product name is: ", p.name)
        print("Supplier name is: ", p.supplier_name)
        print("amount is ", p.amount)
        print("price is ", p.price)

        # userDetails= User.objects.filter(user=user.id, course=pk)
        # for userCourse in userCourses:
        p.name = product
        serializers = ProductsSerializer(p, many=False)
        #     arr.append(serializers.data)

        response = {'message': 'Get', 'results': serializers.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def UpdateProductDetails(self, request, pk=None):
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name', product.name)
        supplier_name = request.data.get(
            'supplier_name', product.supplier_name)
        amount = request.data.get('amount', product.amount)
        price = request.data.get('price', product.price)

        product.name = name
        product.supplier_name = supplier_name
        product.amount = amount
        product.price = price

        product.save()
        serializer = ProductsSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer
    permission_classes = (AllowAny,)
    #authentication_classes = (TokenAuthentication, )
    @action(detail=False, methods=['POST'])
    def AddNewSupplier(self, request):
        givenSupplierName = ' '
        givenSupplierEmail = ' '
        givenProducts = ' '
        givenAddress = ' '
       # if 'name' in request.data:
        givenSupplierName = request.POST.get('name')
        # if 'Supplier name' in request.data:
        givenSupplierEmail = request.POST.get('SupplierEmail')
        # if 'Amount' in request.data:
        givenProducts = request.POST.get('Products')
       # if 'Price' in request.data:
        givenaddress = request.POST.get('address')

        newSupplier = Suppliers.objects.create(
            name=givenSupplierName, SupplierEmail=givenSupplierEmail, Products=givenProducts, address=givenaddress)
        newSupplier.save()
        print("Supplier is: ", newSupplier)

        response = {'message': 'created', 'results': newSupplier}
        return Response(response, status=status.HTTP_200_OK)

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = (AllowAny,)
    #authentication_classes = (TokenAuthentication, )
    @action(detail=True, methods=['POST'])
    def getAllOrders(self, request, pk=None):
        print("im here")
        Order = request.Order
        print("Orders from query is: ", Order)
        arr = []
        ord = Orders.objects.get(Orders=Order)
        # print("user mail is: ", u.email)
        print("order name is: ", ord.delivery_name)
        print("peoducts id  is: ", ord.products)
        print("total price is ", ord.total_price)
        print("order date is ", ord.order_date)
        print("delivery date is ", ord.delivery_date)
        print("adress is ", ord.address)
        print("amount is ", ord.amount)
        print("Status is ", ord.status)


        # userDetails= User.objects.filter(user=user.id, course=pk)
        # for userCourse in userCourses:
        ord.delivery_name = order
        serializers = OrdersSerializer(ord, many=False)
        #     arr.append(serializers.data)

        response = {'message': 'Get', 'results': serializers.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def AddNewOrder(self, request):
        givenDeliveryName = ' '
        givenProducts = ' '
        givenTotalPrice = ' '
        givenOrderDate = ' '
        givenDeliveryDate = ' '
        givenAddress = ' ' 
        givenAmount = ' '
        givenStatus = ' '
       # if 'name' in request.data:
        givenDeliveryName = request.POST.get('delivery_name')
        # if 'Supplier name' in request.data:
        givenProducts = request.POST.get('products')
        # if 'Amount' in request.data:
        givenTotalPrice = request.POST.get('total_price')
       # if 'Price' in request.data:
        givenOrderDate = request.POST.get('order_date')
        givenDeliveryDate = request.POST.get('delivery_date')
        givenAddress = request.POST.get('address')
        givenAmount = request.POST.get('amount')
        givenStatus = request.POST.get('status')

        newOrder = Orders.objects.create(
            delivery_name=givenDeliveryName, products=givenProducts, total_price=givenTotalPrice, order_date=givenOrderDate, 
            delivery_date=givenDeliveryDate , address=givenAddress ,amount=givenAmount, status=givenStatus)
        newOrder.save()
        print("Order is: ", newOrder)

        response = {'message': 'created', 'results': newProduct}
        return Response(response, status=status.HTTP_200_OK)