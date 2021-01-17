"""
chat_app urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('team', views.build_team),
    path('team/<team_id>', views.Team.as_view()),
    path('channel/<channel_id>',views.Channel.as_view()),
]
