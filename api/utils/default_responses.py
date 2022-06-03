from rest_framework.response import Response


def error_response(error, status=400):
    return Response({'error': str(error)}, status=status)


def success_response(success_message="success", status=200):
    return Response({'message': success_message}, status=status)
