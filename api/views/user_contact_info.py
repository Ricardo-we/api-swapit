from api.models import User, ConfirmationCode, UserContactInformation
from api.serializers import UserContactInfoSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from api.utils.check_token_and_user import check_user_and_token

@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def add_user_contact_info(request, user_id):
    try:
        check_user_and_token(user_id, request.headers['Authorization'])
        if request.method == 'POST':
            if not request.data.get('contact_type'): raise ValueError('Not contact type')
            if not request.data.get('contact'): raise ValueError('Not contact')
            created_contact = UserContactInformation.objects.create(
                user_id=user_id, 
                contact_type=request.data['contact_type'], 
                contact=request.data['contact']
            )
            serializer = UserContactInfoSerializer(created_contact, many=False)
            return Response(serializer.data)
        elif request.method == 'GET':
            contact_info = UserContactInformation.objects.filter(user_id=user_id).all()
            serializer = UserContactInfoSerializer(contact_info, many=True)
            return Response(serializer.data)
    except Exception as error:
        return Response({'error': str(error)})
    
@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def contact_info_details(request, user_id, contact_id):
    try:
        check_user_and_token(user_id, request.headers['Authorization'])
        contact_info = UserContactInformation.objects.get(id=contact_id)
        if request.method == 'PUT':
            print(request.data.get('contact_type'))
            contact_info.contact_type = request.data.get('contact_type') or contact_info.contact_type
            contact_info.contact = request.data.get('contact') or contact_info.contact
            contact_info.save()
            serializer = UserContactInfoSerializer(contact_info, many=False)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            contact_info.delete()
            return Response({'message': 'Contact deleted'})
    except Exception as error:
        return Response({'error': str(error)})