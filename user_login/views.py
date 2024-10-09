from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
import requests,json
from rest_framework import status
from rest_framework.permissions import AllowAny
from inventory_management import ins_logger



# Create your views here.
class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            str_username = request.data['username']
            str_password = request.data['password']
            user = authenticate(
                request, username=str_username, password=str_password)
            if user:
                login(request, user)
                token_json = requests.post(request.scheme+'://'+request.get_host()+'/api/token/',{'username':str_username,'password':str_password})
                token = json.loads(token_json._content.decode("utf-8"))['access']
                str_name = user.username
                email = user.email or ''
                userdetails = {'Name': str_name, 'email': email}
                return Response({'status': 1, 'token': token, 'userdetails': userdetails, "str_session_key": request.session.session_key},status = status.HTTP_200_OK)
            raise Exception('User does not exist')
        except Exception as e:
            ins_logger.logger.error(e, extra={'user': 'user_id:' + str(request.user.id),'details':'line no: ' + str(e.__traceback__.tb_lineno)})
            return Response({'status':0,'reason':str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)