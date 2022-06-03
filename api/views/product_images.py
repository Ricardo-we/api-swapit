from api.models import ProductImage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from api.utils.check_token_and_user import check_user_and_token

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
@csrf_exempt
def add_product_image(request, user_id, product_id):
    try:
        check_user_and_token(user_id, request.headers['Authorization'])
        ProductImage.objects.create(product_id=product_id, image=request.FILES.get('product_image'))
    except Exception as error:
        return Response({'error': str(error)})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
@csrf_exempt
def delete_product_image(request, user_id, image_id):
    try:
        check_user_and_token(user_id, request.headers['Authorization'])
        product_image = ProductImage.objects.get(id=image_id)
        ProductImage.delete_image(product_image)
        return Response({'message': 'Image deleted'})
    except Exception as error:
        return Response({'error': str(error)})
