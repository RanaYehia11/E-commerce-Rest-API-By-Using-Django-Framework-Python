
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Review
from .serializer import Product_serializer
from .filter import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.db.models import Avg
from django.utils.crypto import get_random_string
# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    restPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = restPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = Product_serializer(queryset, many=True)

    return Response({'products': serializer.data})

@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = Product_serializer(product, many=False)
    return Response({'products': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    data = request.data
    serializer = Product_serializer(data=data)
    if serializer.is_valid():
        product=Product.objects.create(**data,user=request.user)
        res=Product_serializer(product,many=False)
   
        return Response({'products': res.data})
    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"product": "Sorry you can't update this product"}, status=status.HTTP_403_FORBIDDEN)
    product.name=request.data['name']
    product.description=request.data['description']
    product.price=request.data['price']
    product.brand=request.data['brand']
    product.category=request.data['category']
    product.rating=request.data['rating']
    product.stock=request.data['stock']
    product.save()
    serializer=Product_serializer(product ,many=False)
    return Response({"Product":serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"product": "Sorry you can't delete this product"}, status=status.HTTP_403_FORBIDDEN)
   
    product.delete()
    return Response({"details":"Product is deleted"},status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request,pk):
    user=request.user
    product=get_object_or_404(Product,id=pk)
    data = request.data
    review=product.reviews.filter(user=user)
 
    if data['rating']<=0 or data['rating'] >5:
        return Response({'error':" please choose from 1 to 5 only "},status=status.HTTP_400_BAD_REQUEST)
    
    elif review.exists():
        new_review={'rating': data['rating'],'comment':data['comment']}
        review.update(**new_review)
    
        rating=product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.save()
        return Response({'details':' product review updated'})
    else:
        Review.objects.create (
            user=user ,
            product=product ,
            rating=data['rating'] ,
            comment=data['comment']
        )
        rating=  rating=product.reviews.aggregate(avg_ratings=Avg('rating'))
        product_rating=rating['avg_ratings']
        product.save()
        return Response({'details': 'Product review created'})
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    product = get_object_or_404(Product, id=pk)
    user=request.user
    review=product.reviews.filter(user=user)

    if review.exists():
        review.delete()
        rating=product.reviews.aggregate(avg_ratings=Avg('rating'))
        if rating['avg_ratings'] is None:
           rating['avg_ratings']=0
           product_rating=rating['avg_ratings']
           product.save()
           return Response({'details': 'Product review deleted'})
    else:
            return Response({"error":"Product isn't found"},status=status.HTTP_404_NOT_FOUND)

