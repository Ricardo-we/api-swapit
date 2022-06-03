from api.models import Product, ProductImage, ProductReport
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from api.utils.check_token_and_user import check_user_and_token
from api.utils.regexp import match_pattern

@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def report_product(request, user_id, product_id):
    try:
        check_user_and_token(user_id, request.headers['Authorization'])
        if ProductReport.objects.filter(product_id=product_id, report_from_id=user_id).exists():
            return Response({'message': 'Product already reported'})

        match_pattern(r"[\w\d\s]{5,}", request.data.get('report_reason'))
        ProductReport.objects.create(
            report_from_id=user_id, 
            report_reason=request.data.get('report_reason') or 'I don\'t like this publication',
            product_id=product_id
        )
        if ProductReport.objects.filter(product_id=product_id).count() > 10:
            product = Product.objects.get(product_id=product_id)
            product.in_revision = True
            product.save()

        return Response({'message': 'Thanks for reporting this item'})
    except Exception as error:
        return Response({'error': str(error)})
