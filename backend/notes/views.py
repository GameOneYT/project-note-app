from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import NoteSerializer, UserSerializer
from .models import Note, User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class NoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Get the authenticated user
        notes = Note.objects.filter(owner=user)  # Filter notes by the authenticated user
        serializer = NoteSerializer(notes, many=True)  # Serialize the notes
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateNoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user  # Get the authenticated user
        note_text = request.data.get('note_text')
        # owner_id = request.data.get('owner')  # Assuming owner is an ID
        print(note_text, user)
        try:
            owner = user
            Note.objects.create(
                note_text=note_text,
                pub_date=timezone.now(),
                owner=owner
            )
            return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_418_IM_A_TEAPOT)
    
class CreateUserView(APIView):

    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class HandleUserConnction(APIView):
    queryset = User.objects.all()

    def post(self, request):
        username = request.data.get('login')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide username and password'}, status=status.HTTP_418_IM_A_TEAPOT)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Generate or get an existing token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            


