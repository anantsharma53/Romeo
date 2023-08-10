from .models import *
from .serializers import *
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class SignUpView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.error,status.HTTP_400_BAD_REQUEST,safe=False)
    
class SignInView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data
            refresh=RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.error,status.HTTP_400_BAD_REQUEST,safe=False)
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        product=Products.objects.all().values()
        print(product)
        return JsonResponse(list(product),safe=False)

















class ProductViewPriceRange(View):
    def get(self,request):
        min_price=request.GET.get('min',None)
        max_price=request.GET.get('max',None)
        if min_price and max_price:
            product=Products.objects.filter(Q(price__gte=int(min_price))| Q(price__lte=int(max_price)))
            serializer=ProductSerializer(product,many=True).data
            return JsonResponse(serializer,safe=False)
        return JsonResponse({"Massage": "Invalid Paramaters"}) 

class ProductMultifillter(View):
    def get(self,request):
        category=request.GET.get('category', None)
        brand=request.GET.get('brand', None)
        active=request.GET.get('active',None)
        product=Products.objects.all()
        if brand:
            product=product.filter(brand__iexact=brand)
        if category:
            product=product.filter(category__iexact=category)
        if active:
            product=product.filter(active__in=[bool(int(active))])
        serializer=ProductSerializer(product,many=True).data
        return JsonResponse(serializer,safe=False)


class ProductSearchNameDesc(View):
    def get(self,request):
        query=request.GET.get("query",None)
        products=Products.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        serializer=ProductSerializer(products,many=True).data
        return JsonResponse(serializer,safe=False)



















class SearchProductView(View):
    def get(self, request):
        query=request.GET.get('query', "")
        product=Products.objects.filter(name__icontains=query)
        # for serching the products in name or description sections
        # product=Products.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        serializer=ProductSerializer(product,many=True).data
        return JsonResponse(serializer,safe=False)
    
class ProductFilterView(View):
    def get(self, request):
        query=request.GET.get('query', "")
        min_price=request.GET.get('min')
        max_price=request.GET.get('max')
        brand=request.GET.get('brand', None)
        features=request.GET.get('features', None)
        category=request.GET.get('category', None)
        product=Products.objects.all()
        if query:
            product=product.filter(name__icontains=query)
        if min_price:
            product=product.filter(price__gte=min_price)
        if max_price:
            product=product.filter(price__lte=max_price)
        if brand:
            product=product.filter(brand=brand)
        if features:
            product=product.filter(features=features)
        if category:
            product=product.filter(category=category)
        serializer=ProductSerializer(product,many=True).data
        return JsonResponse(serializer,safe=False)

class ProductPaginatorView(View):
    def get(self, request):
        page_number = request.GET.get("page", 1)
        products = Products.objects.all().order_by("id")
        paginator = Paginator(products, 5)
        page = paginator.get_page(page_number)
        products_on_page = page.object_list
        serializer = ProductSerializer(products_on_page, many=True).data
        return JsonResponse({"data": serializer, 
        "total_pages": paginator.num_pages, 
        "total_product": products.count()})

class ProductSearchPaginatorView(View):
    def get(self, request):
        query=request.GET.get('query', "")
        min_price=request.GET.get('min')
        max_price=request.GET.get('max')
        brand=request.GET.get('brand', None)
        features=request.GET.get('features', None)
        category=request.GET.get('category', None)
        page_number = request.GET.get("page", 1)
        product=Products.objects.all().order_by("id")
        if query:
            product=product.filter(name__icontains=query)
        if min_price:
            product=product.filter(price__gte=min_price)
        if max_price:
            product=product.filter(price__lte=max_price)
        if brand:
            product=product.filter(brand=brand)
        if features:
            product=product.filter(features=features)
        if category:
            product=product.filter(category=category)
        paginator = Paginator(product, 5)
        page = paginator.get_page(page_number)
        products_on_page = page.object_list
        serializer = ProductSerializer(products_on_page, many=True).data
        return JsonResponse(serializer,safe=False)


         





























class ProductReview(View): 
    def get(self,request,product_id):
        product = Products.objects.filter(id=product_id).first()
        if product:
            review=Review.objects.filter(product=product.id).values()
            serializer=ReviewSerializer(product).data
            serializer["review"]=list(review)
            return JsonResponse(serializer,safe=False)
        return JsonResponse({"massage":"Product Not Found"})
class AllOrderItems(View): 
    def get(self,request,order_id):
        order = Order.objects.filter(id=order_id).first()
        print(order)
        if order:
            orderItems=OrderItems.objects.filter(order=order.id).values()
            serializer=OrderSerializer(order).data
            serializer["OrderItems"]=list(OrderItems)
            return JsonResponse(serializer,safe=False)
        return JsonResponse({"massage":"Order Not Found"})
# using for loop
class AllOrderItemsFor(View): 
    def get(self,request,order_id):
        order = Order.objects.filter(id=order_id).first()
        if order:
            items=[]
            orderItems=OrderItems.objects.filter(order=order.id).values()
            for val in orderItems:
                items.append(
                    {
                        "order":val.order,
                        "product":val.product,
                        "quantity":val.quantity,
                        "price":val.price,
                    }
                )
                orderResponse={
                    "id":order.id,
                    "user":order.user,
                    "order_number":order.order_number,
                    "order_date":order.order_date,
                    "order_itmes":items,
                }

            return JsonResponse(orderResponse)
        return JsonResponse({"massage":"Order Not Found"})