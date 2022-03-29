from django.shortcuts import get_object_or_404
from django.http import HttpRequest, JsonResponse

from .models import Poll


def polls_list(request: HttpRequest) -> JsonResponse:
    print('Called')
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:MAX_OBJECTS]
    data = {'results': list(polls.values('question', 'created_by__username', 'published_at'))}
    return JsonResponse(data)

def polls_detail(request: HttpRequest, pk: int) -> JsonResponse:
    poll = get_object_or_404(Poll, pk=pk)
    data = {'result': {
        'question': poll.question,
        'created_by': poll.created_by.username,
        'published_at': poll.published_at,
    }}
    return JsonResponse(data)
