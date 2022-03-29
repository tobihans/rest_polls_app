from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import Choice, Poll
from .serializers import (
    ChoiceSerializer,
    PollSerializer,
    UserSerializer,
    VoteSerializer,
)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request: Request):
        username = request.data.get('username')  # type: ignore
        password = request.data.get('password')  # type: ignore
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.CreateAPIView):
    authentication_classes= ()
    permission_classes = ()
    serializer_class = UserSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()  # type: ignore
    serializer_class = PollSerializer

    def destroy(self, request: Request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])  # type: ignore
        if not request.user == poll.created_by:
            raise PermissionDenied('You are not allowed to delete this poll')
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.filter(poll_id=self.kwargs['pk'])  # type: ignore

    def post(self, request: Request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])  # type: ignore
        if not request.user == poll.created_by:
            raise PermissionDenied('Yu are not allowed to delete this poll')
        return super().post(request, *args, **kwargs)

class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request: Request, pk: int, choice_pk: int):
        voted_by = request.data.get('voted_by')  # type: ignore
        data = {
            'choice': choice_pk,
            'poll': pk,
            'voted_by':voted_by,
        }
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

