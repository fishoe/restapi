from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.utils import timezone

from chat_app.models import team as team_model
from chat_app.models import team_member as member_model
from chat_app.models import channel as ch_model
from chat_app.models import team_message as msg_model
from chat_app.models import unread_tm as unread_model
from .utils import error_response, login_req

@method_decorator(csrf_exempt, name='dispatch')
class Channel(View):
    def get(self,request,channel_id):
        ch = ch_model.objects.get(id=channel_id)
        is_member = len(ch.team.users.filter(id=request.user.id))
        if is_member :
            last_msg = request.GET.get('last',None)
            if last_msg is not None :
                msgs_qset = ch.messages.filter(id__gt=last_msg).order_by("-date")
            else :
                msgs_qset = ch.messages.all().order_by("-date")
            #read_check
            unreads = unread_model.objects.filter(
                message__in=msgs_qset,
                reciever__user=request.user,
                is_read=False
            )
            if len(unreads) > 0:
                unreads.update(is_read=True,checked_date=timezone.now())
            msgs = list(msgs_qset.values())
            return JsonResponse(data={
                "id":ch.id,
                "messages":msgs
            })
        return error_response(403,"permission error, not member")

    def post(self,request,channel_id):
        try:
            ch = ch_model.objects.get(id=channel_id)
            text = request.POST.get('context',"")
            member = member_model.objects.get(team=ch.team,user=request.user)
            new_messages = msg_model(channel=ch,author=member,context=text)
            new_messages.save()
            #unread
            recievers = ch.team.members.all().exclude(user=request.user)
            
            new_messages.unread.set(
                recievers,
                through_defaults={
                    "is_read":False,
                    "checked_date":None
                }
            )
            
            return JsonResponse(data={
                "id":ch.id,
                "message": {
                    "id":new_messages.id,
                    "channel":ch.id,
                    "author":member.id,
                    "context":text,
                    "date":new_messages.date
                }
            })
        except Exception:
            return error_response(400,"bad req")

    def delete(self,request,channel_id):
        return error_response(400,"bad req")