from api.models import Product, ProductImage, ProductTags, User
from api.serializers import ProductSerializer, InRevisionProductsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from api.utils.PagePagination import PagePagination
from api.utils.check_token_and_user import check_user_and_token
from api.utils.default_responses import error_response, success_response

# GETTING AND FILTERING PRODUCTS,
@api_view(['GET'])
def get_products(request):
    try:
        if request.GET.get('product_id'):
            product = Product.objects.filter(
                id=request.GET['product_id']).first()
            serializer = ProductSerializer(
                product, many=False, context={'request': request})
            return Response(serializer.data)
        if request.GET.get('in_revision'):
            products = Product.objects.filter(in_revision=True).order_by(
                'last_update', 'aproximate_price').all()
            serializer = InRevisionProductsSerializer(products, many=True)
            return Response(serializer.data)

        if request.GET.get('user_id'):
            products = Product.objects.filter(
                user_id=request.GET.get('user_id')).all()
        elif request.GET.get('tags'):
            products = Product.objects.filter(tags=request.GET.get(
                'tags').split('-')).exclude(in_revision=True).all()
        elif request.GET.get('name'):
            products = Product.objects.filter(name__icontains=request.GET.get('name')).exclude(
                in_revision=True).order_by('last_update', 'aproximate_price').all()
        elif request.GET.get('location'):
            products = Product.objects.filter(user__location=request.GET['location']).exclude(
                in_revision=True).order_by('last_update').all()
            if len(products) <= 0:
                products = Product.objects.all()
        else:
            products = Product.objects.all()

        paginator = PagePagination()
        paginated_data = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            paginated_data, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response({'error': error})


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def add_product(request, user_id):
    try:
        if not user_id:
            raise ValueError('User id required')
        check_user_and_token(user_id, request.headers['Authorization'])
        product = Product.objects.create(
            user_id=user_id,
            name=request.data['name'],
            description=request.data.get('description'),
            aproximate_price=request.data['aproximate_price'],
            possible_interchanges=request.data.get('possible_interchanges')
        )
        print(request.FILES.getlist('product_images'))
        for image in request.FILES.getlist('product_images'):
            ProductImage.objects.create(product=product, image=image)
        for tag in request.data.getlist("tags"):
            product.tags.add(tag)

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Exception as error:
        return Response({'error': str(error)})


@api_view(['DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def add_tags_to_product(request, user_id, product_id, tag_id):
    if product.user.id != user_id: raise Exception(f'This product isnt property of id: {user_id}')
    product = Product.objects.get(pk=product_id)
    product.tags.remove(tag_id)
    return Response({})


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
@csrf_exempt
def product_details(request, user_id, pk):
    try:
        product = Product.objects.get(pk=pk)
        if product.user.id != user_id:
            raise Exception(f'This product isnt property of id: {user_id}')
        check_user_and_token(user_id, request.headers['Authorization'])
        if request.method == 'PUT':
            product.name = request.data.get('name') or product.name
            product.description = request.data.get('description') or product.description
            product.aproximate_price = request.data.get('aproximate_price') or product.aproximate_price
            product.possible_interchanges = request.data.get('possible_interchanges') or product.possible_interchanges
            for image in request.FILES.getlist('product_images'):
                ProductImage.objects.create(product=product, image=image)
            for tag in request.data.getlist("tags"):
                product.tags.add(tag)

            product.save()
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            for image in ProductImage.objects.filter(product=product).all():
                print(image.image)
                ProductImage.delete_image(image)
            product.delete()
            return Response({'message': f'Product with id {product.id} deleted'})
    except Exception as error:
        return Response({'error': str(error)})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_product_as_superuser(request, user_id, product_id):
    try:
        check_user_and_token(user_id, request.headers['Authorization'])
        if not User.objects.get(id=user_id).is_superuser:
            raise Exception('Hey hey baddie boy what are you trying to do?')
        Product.objects.get(id=product_id).delete()
        return success_response("Product deleted successfully")
    except Exception as error:
        return error_response(error)
