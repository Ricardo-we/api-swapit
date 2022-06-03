from api.models import ProductTags, User
from api.serializers import ProductTagsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from api.utils.PagePagination import PagePagination
from api.utils.check_token_and_user import check_user_and_token
from api.utils.regexp import match_pattern


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def add_tag(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_superuser or not user.is_staff:
            raise PermissionError(
                'Hey hey baddie boy what are you trying to do?')
        if not request.data.get('name'):
            raise ValueError('Name required for tag creation')
        check_user_and_token(user_id, request.headers['Authorization'])
        match_pattern(r"[\w\s]{2,150}", request.data.get('name'))

        tag = ProductTags.objects.create(name=request.data['name'])
        serializer = ProductTagsSerializer(tag)
        return Response(serializer.data)
    except Exception as error:
        return Response({'error': str(error)})


@api_view(['GET'])
@csrf_exempt
def get_tags(request):
    try:
        tags = ProductTags.objects.all()
        serializer = ProductTagsSerializer(tags, many=True)
        return Response(serializer.data)
    except Exception as error:
        return Response({'error': str(error)})


@api_view(['PUT', 'DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def tags_detail(request, user_id, tag_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.is_superuser or not user.is_staff:
            raise PermissionError(
                'Hey hey baddie boy what are you trying to do?')
        check_user_and_token(user_id, request.headers['Authorization'])
        tag = ProductTags.objects.get(id=tag_id)

        if request.method == 'PUT':
            match_pattern(r"[\w\s]{2,150}", request.data.get('name'))
            tag.name = request.data.get('name') or tag.name
            tag.save()
            serializer = ProductTagsSerializer(tag)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            tag.delete()
            return Response({'message': 'Product tag deleted successfully'})
    except Exception as error:
        return Response({'error': str(error)})
