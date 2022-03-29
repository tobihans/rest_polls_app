from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Choice, Poll
from .serializers import ChoiceSerializer, PollSerializer, VoteSerializer


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()  # type: ignore
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()  # type: ignore
    serializer_class = PollSerializer


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.filter(poll_id=self.kwargs['pk'])  # type: ignore


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

