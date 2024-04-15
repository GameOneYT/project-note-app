from django.utils import timezone
from django.shortcuts import render
from django.db import connection
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .serializers import NoteSerializer, UserSerializer
from .models import Note, User
from rest_framework.authtoken.views import obtain_auth_token

from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



class NoteView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateNoteView(APIView):
    def post(self, request):
        note_text = request.data.get('note_text')
        owner_id = request.data.get('owner')  # Assuming owner is an ID
        print(note_text, owner_id)
        try:
            owner = User.objects.get(id=owner_id)
            Note.objects.create(
                note_text=note_text,
                pub_date=timezone.now(),
                owner=owner
            )
            return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'})
    
class CreateUserView(APIView):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class HandleUserConnction(APIView):
    queryset = User.objects.all()
    # def post(self, request):
        
    #     login = str(request.data.get('login'))
    #     password = str(request.data.get('password'))  # Assuming owner is an ID
    #     print(login+password)
        
        
    #     cursor = connection.cursor()
    #     cursor.execute('SELECT count(*) FROM notes_user WHERE username LIKE "'+login+'" AND password LIKE "'+password+'"')
    #     row = str(cursor.fetchone()[0])
    #     print (row)
    #     try:
    #         if (row == "1"):
    #             return Response({'message': 'User found'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'User not found'}, status=status.HTTP_418_IM_A_TEAPOT)
    #     except:
    #         return Response({'error': 'System error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # def post(self, request):
    #     username = request.data.get('login')
    #     password = request.data.get('password')
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         # Generate or get an existing token for the user
    #         token = obtain_auth_token(request._request)  # Use Token.objects.get_or_create to get or create the token
    #         print("token: "+str(token))
    #         return Response({'token': token.key}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': 'User not found'}, status=status.HTTP_418_IM_A_TEAPOT)
    def post(self, request):
        username = request.data.get('login')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Generate or get an existing token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            


