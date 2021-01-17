from django.db import models
from django.conf import settings
from django.db.models.constraints import UniqueConstraint

# Create your models here.

#user models
user_model = settings.AUTH_USER_MODEL

#uploaded files
class uploaded_file(models.Model):
    owner = models.ForeignKey(user_model, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=250)
    location = models.FileField() #something detail
    uploaded_date = models.DateTimeField(auto_now=True)
    size_byte = models.IntegerField()
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

#team messaging system
class team(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(user_model, related_name='own_teams', on_delete=models.DO_NOTHING)
    users = models.ManyToManyField(
        user_model,
        through='team_member',
        through_fields=('team','user'),
    )

class invite(models.Model):
    host = models.ForeignKey(
        user_model,
        related_name='published_invites',
        on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        team,
        related_name='invites',
        on_delete=models.CASCADE
    )
    limit = models.IntegerField(null=True)
    max_limit = models.IntegerField(null=True, default=None)
    expired_date = models.DateTimeField(null = True, default=None)
    published_date = models.DateTimeField(auto_now_add=True)

class team_member(models.Model):
    """
    M:N relation model
    team and user in the team.
    """
    user = models.ForeignKey(user_model, related_name="teams", on_delete=models.CASCADE)
    team = models.ForeignKey(team, related_name="members", on_delete=models.CASCADE)
    team_name = models.CharField(max_length=150, blank=True)
    invited_by = models.ForeignKey(invite, null=True, on_delete=models.SET_NULL, default=None)
    joined_date = models.DateTimeField(auto_now_add=True)

    roles = models.ManyToManyField(
        "role",
        through="member_role"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'team'], name="unique_member"),
        ]

class category(models.Model):
    team = models.ForeignKey(
        team,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=150)

class channel(models.Model):
    team = models.ForeignKey(
        team,
        related_name="channels",
        on_delete=models.CASCADE,
    )
    ctg = models.ForeignKey(
        category,
        related_name="channels",
        null=True,
        on_delete=models.SET_NULL,
        default=None
    )
    name = models.CharField(max_length=40)

class permission(models.Model):
    class permission_level(models.IntegerChoices):
        TEAM = 1,           "TEAM"          #team setting, team default rule, almost admin
        CATEGORY = 2,       "CATEGORY"      #create update delete ctg
        CHANNEL = 3,        "CHANNEL"       #create update delete ch, channel role set
        MESSAGE = 4,        "MESSAGE"       #create update delete msg
        MEMBER = 5,         "MEMBER"        #invite, kick , mute(not planned yet)
        ROLE = 6,           "ROLE"          #make set delete roles

    name = models.CharField(max_length=100)
    level = models.IntegerField(choices=permission_level.choices)

class role(models.Model):
    team = models.ForeignKey(
        team,
        related_name="roles",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=6)
    priority = models.IntegerField()

class role_perms_team(models.Model):
    """
    M:N relation model
    role : team 
    """
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    team = models.ForeignKey(team, on_delete=models.CASCADE)
    perm = models.ForeignKey(permission, on_delete=models.CASCADE)
    status = models.IntegerField()

    class Meta():
        constraints = [
            UniqueConstraint(fields=['role', 'team', 'perm'], name="unique_role_team"),
        ]

class role_perms_ctg(models.Model):
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    ctg = models.ForeignKey(category, on_delete=models.CASCADE)
    perm = models.ForeignKey(permission, on_delete=models.CASCADE)
    status = models.IntegerField()

    class Meta():
        constraints = [
            UniqueConstraint(fields=['role', 'ctg', 'perm'], name="unique_role_ctg"),
        ]

class role_perms_channel(models.Model):
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    ch = models.ForeignKey(channel, on_delete=models.CASCADE)
    perm = models.ForeignKey(permission, on_delete=models.CASCADE)
    status = models.IntegerField()

    class Meta():
        constraints = [
            UniqueConstraint(fields=['role', 'ch', 'perm'], name="unique_role_ch"),
        ]

class member_role(models.Model):
    member = models.ForeignKey(team_member, on_delete=models.CASCADE)
    role = models.ForeignKey(role, on_delete=models.CASCADE)

class team_message(models.Model):
    author = models.ForeignKey(
        team_member,
        null=True,
        on_delete=models.SET_NULL,
        related_name="messages"
    )
    channel = models.ForeignKey(
        channel,
        related_name="messages",
        on_delete=models.CASCADE
    )
    context = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    attachments = models.ManyToManyField(
        uploaded_file,
        through="tm_attachments"
    )
    unread = models.ManyToManyField(
        team_member,
        through="unread_tm"
    )

class tm_attachments(models.Model):
    message = models.ForeignKey(team_message, on_delete=models.CASCADE)
    attached_file = models.ForeignKey(
        uploaded_file,
        related_name="tms",
        null=True,
        on_delete=models.SET_NULL
    )

class unread_tm(models.Model):
    message = models.ForeignKey(team_message, related_name="unread_members" ,on_delete=models.CASCADE)
    reciever = models.ForeignKey(team_member, related_name="new_messages" ,on_delete=models.CASCADE)
    is_read = models.BooleanField(default=True)
    checked_date = models.DateTimeField(null=True, default=None)

#dm/group messaging system

class dm_group(models.Model):
    name = models.CharField(max_length=150)

class group_member(models.Model):
    group = models.ForeignKey(dm_group, on_delete=models.CASCADE)
    member = models.ForeignKey(user_model, related_name="members", on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

class direct_message(models.Model):
    author = models.ForeignKey(group_member,null=True, on_delete=models.SET_NULL)
    receive = models.ForeignKey(dm_group, related_name="messages", on_delete=models.CASCADE)
    context = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    attachments = models.ManyToManyField(
        uploaded_file,
        through="dm_attachments"
    )

class unread_dm(models.Model):
    message = models.ForeignKey(direct_message, on_delete=models.CASCADE)
    member = models.ForeignKey(group_member, related_name="new_dms", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    checked_date = models.DateTimeField(null=True, default=None)

class dm_attachments(models.Model):
    message = models.ForeignKey(direct_message, on_delete=models.CASCADE)
    attached_file = models.ForeignKey(
        uploaded_file,
        related_name="dms",
        null=True,
        on_delete=models.SET_NULL,
    )
