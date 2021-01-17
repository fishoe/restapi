import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .team import Team
from .team import build_team

from .channel import Channel

from .utils import error_response
# Create your views here.

__all__=["build_team","Team","Channel"]

def test(request):
    print(asyncio.iscoroutine(test2(request)))
    return test2(request)

async def test2(request):
    await asyncio.sleep(2.5)
    return JsonResponse(data={})