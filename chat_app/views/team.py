from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from django.http import HttpResponse
# from django.dispatch import receiver
# from django.core.signals import request_started

from chat_app.models import team as team_model
from chat_app.models import team_member as member_model
from chat_app.models import channel as ch_model
from .utils import error_response, login_req

@method_decorator(csrf_exempt)
@login_req
def build_team(request):
    """
    login required
    input team_name
    """
    if request.method == "POST" :
        #팀 이름, 유저 가져오기
        teamname = request.POST['name']
        user = request.user
        #팀만들기
        new_team = team_model(name=teamname,owner=request.user)
        new_team.save()
        #팀 멤버 추가
        new_member = member_model(team=new_team,user=user)
        new_member.save()
        #팀 채널 추가
        new_ch = ch_model(name="channel",team=new_team,ctg=None)
        new_ch.save()
        #팀 기본 규칙 추가(미정)

        #생성 팀 정보 반환
        return JsonResponse(data={
            "id" : new_team.id,
            "name": teamname,
            "owner" : user.username,
            "channels" : [{
                "id":new_ch.id,
                "name":new_ch.name,
            }],
        })
    return error_response(400,"invalid request")

@method_decorator(csrf_exempt, name='dispatch')
class Team(View):

    @method_decorator(login_req)
    def get(self,request,team_id):
        """
        get team information
        """
        user = request.user
        data = {}
        try :
            team = team_model.objects.get(id=team_id)
            data={
                'id' : team.pk,
                'name' : team.name,
                'owner' : team.owner.pk
            }
            member = member_model.objects.get(team=team,user=user)
            member_list = list(team.members.all().values())
            data['members']=member_list
            chs = list(team.channels.all().values())
            data['channels']=chs
        except team_model.DoesNotExist :
            error_response(400,"there is no team has that id")
        except member_model.DoesNotExist :
            data['members']=[]
            data['channels']=[]
        finally :
            return JsonResponse(data=data)

    @method_decorator(login_req)
    def post(self,request,team_id):
        """
        채널을 만드는 요청.
        권한 확인 후 post에 있는 정보에 따라 채널을 만든다
        채널을 만든 후에는 채널의 정보를 반환한다.
        """
        #권한 확인
        
        #입력 검사

        #team
        team = team_model.objects.get(id=team_id)
        ch_name = request.POST['name']

        new_ch = ch_model(name=ch_name,team=team,ctg=None)
        new_ch.save()
        #info
        chlist = list(team.channels.all().values())
        return JsonResponse(data={
            "team":team.name,
            "channels":chlist
        })
    
    def delete(self,request,team_id):
        team = team_model.objects.get(id=team_id)
        if team.owner == request.user:
            team_name = team.name
            team.delete()
            return JsonResponse(data={
                "id":team.id,
                "team":team.name
            })
        return error_response(403,"you are not team owner")
    def put(self,request,team_id):
        team = team_model.objects.get(id=team_id)
        is_joined = len(team.users.filter(pk=request.user.id))
        if is_joined :
            return JsonResponse(data={
                "message":"already joined"
            })
        else :
            new_member = member_model(team=team,user=request.user,team_name="",invited_by=None)
            new_member.save()
            return JsonResponse(data={
                "message":f"joined in {team.name}"
            })
