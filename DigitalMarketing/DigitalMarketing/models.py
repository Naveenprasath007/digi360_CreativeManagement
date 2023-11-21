from django.db import models
from .validators import file_size
from datetime import datetime

#django authentication
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class cVideoId(models.Model):
    VideoID = models.CharField(db_column='videoID', max_length=250) 
    userID = models.CharField(db_column='userID', max_length=250, null=True) 
    def __str__(self):
        return self.VideoID
    




class Campaignquestionresponse(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    campaignquestionid = models.ForeignKey('TbCampaignquestion', models.DO_NOTHING, db_column='campaignquestionid', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='userid', blank=True, null=True)  # Field name made lowercase.
    response = models.CharField(db_column='response',  max_length=2000)
    # response = models.CharField(db_column='response',primary_key=True, max_length=2000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'campaignquestionresponse'


class Campaignvideo(models.Model):
    campaignvideoid = models.CharField(db_column='campaignvideoid', primary_key=True, max_length=255)  # Field name made lowercase.
    videoid = models.ForeignKey('TbVideo', models.DO_NOTHING, db_column='videoid', blank=True, null=True)  # Field name made lowercase.
    campaignid = models.CharField(db_column='campaignid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    previousvideoid = models.CharField(db_column='previousvideoid', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'campaignvideo'


class TbApprove(models.Model):
    userid = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='userid')  # Field name made lowercase.
    videoid = models.CharField(db_column='videoid', max_length=250,primary_key=True)  # Field name made lowercase.
    videotitle = models.CharField(db_column='videotitle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    videopath = models.CharField(db_column='videopath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    videopath1 = models.CharField(db_column='videopath1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uploadername = models.CharField(db_column='uploadername', max_length=255, blank=True, null=True)  # Field name made lowercase.
    approveddate = models.DateTimeField(default=datetime.now)  # Field name made lowercase.
    downloadaccess = models.CharField(db_column='downloadaccess', max_length=255, blank=True, null=True)
    downloader = models.CharField(db_column='downloader', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_approve'


class TbCampaignquestion(models.Model):
    campaignquestionid = models.CharField(db_column='campaignquestionid',primary_key=True, max_length=255)  # Field name made lowercase.
    campaignvideoid = models.ForeignKey(Campaignvideo, models.DO_NOTHING, db_column='campaignvideoid', blank=True, null=True)  # Field name made lowercase.
    userroleid = models.ForeignKey('TbUserrole', models.DO_NOTHING, db_column='userroleid', blank=True, null=True)  # Field name made lowercase.
    questionid = models.ForeignKey('TbQuestion', models.DO_NOTHING, db_column='questionid', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_campaignquestion'


class TbQuestion(models.Model):
    questionid = models.CharField(db_column='questionid', primary_key=True, max_length=255)  # Field name made lowercase.
    questiontext = models.CharField(db_column='questiontext', max_length=2000)  # Field name made lowercase.
    questionresponse = models.CharField(db_column='questionresponse', max_length=4000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_question'


class TbStatus(models.Model):
    userid = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='userid')  # Field name made lowercase.
    videoid = models.CharField(db_column='videoid', max_length=250, primary_key=True)  # Field name made lowercase.
    reason = models.CharField(db_column='reason', max_length=255, blank=True, null=True)  # Field name made lowercase.
    videoname = models.CharField(db_column='videoname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    approver = models.CharField(db_column='approver', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uploadername = models.CharField(db_column='uploadername', max_length=255, blank=True, null=True)  # Field name made lowercase.
    platform = models.CharField(db_column='platform', max_length=2000)  # Field name made lowercase.
    createddate = models.DateTimeField(default=datetime.now)# Field name made lowercase.
    videoPath1 = models.CharField(db_column='videopath1', max_length=2000,blank=True, null=True)  # Field name made lowercase.
    videoPath2 = models.CharField(db_column='videopath2', max_length=255, blank=True, null=True)
    videoPath = models.CharField(db_column='videopath', max_length=2000,blank=True, null=True)  # Field name made lowercase.
    Imageurl = models.CharField(db_column='imgurl', max_length=255, blank=True, null=True)
    Gifurl = models.CharField(db_column='gifurl', max_length=255, blank=True, null=True)
    creative = models.CharField(db_column='creative', max_length=255)  # Field name made lowercase.
    MainReason = models.CharField(db_column='mainreason', max_length=2000,blank=True, null=True)  # Field name made lowercase.
    downloadaccess = models.CharField(db_column='downloadaccess', max_length=255, blank=True, null=True)
    downloader = models.CharField(db_column='downloader', max_length=255, blank=True, null=True)
    downloadaccesslist = models.CharField(db_column='downloadaccesslist', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_status'


class TbUser(models.Model):
    userid = models.CharField(db_column='userid', primary_key=True, max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='username', max_length=250)  # Field name made lowercase.
    userroleid = models.ForeignKey('TbUserrole', models.DO_NOTHING, db_column='userroleid', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vendor=models.CharField(db_column='vendor', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_user'


class TbUserrole(models.Model):
    userroleid = models.CharField(db_column='userroleid', primary_key=True, max_length=255)  # Field name made lowercase.
    userrolename = models.CharField(db_column='userrolename', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_userrole'


class TbVideo(models.Model):
    videoid = models.CharField(db_column='videoid', primary_key=True, max_length=255)  # Field name made lowercase.
    previousvideoid = models.CharField(db_column='previousvideoid', max_length=255, blank=True, null=True)  # Field name made lowercase.
    videoname = models.CharField(db_column='videoname', max_length=2000)  # Field name made lowercase.
    videopath = models.CharField(db_column='videopath', max_length=2000)  # Field name made lowercase.
    videotranscription = models.TextField(db_column='videotranscription')  # Field name made lowercase.
    vendor = models.CharField(db_column='vendor', max_length=2000)  # Field name made lowercase.
    lob = models.CharField(db_column='lob', max_length=2000)  # Field name made lowercase.
    creative = models.CharField(db_column='creative', max_length=2000)  # Field name made lowercase.
    platform = models.CharField(db_column='platform', max_length=2000)  # Field name made lowercase.
    videopath1 = models.CharField(db_column='videopath1', max_length=2000,blank=True, null=True)  # Field name made lowercase.
    creater = models.CharField(db_column='creater', max_length=255, blank=True, null=True)
    Imageurl = models.CharField(db_column='imgurl', max_length=255, blank=True, null=True)
    Gifurl = models.CharField(db_column='gifurl', max_length=255, blank=True, null=True)
    videopath2 = models.CharField(db_column='videopath2', max_length=255, blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'tb_video'

class video_Details(models.Model):
    userid = models.ForeignKey('TbUser', models.DO_NOTHING, db_column='userid')  # Field name made lowercase.
    VideoPath = models.CharField(db_column='videopath',primary_key=True, max_length=2000)  # Field name made lowercase.
    VideoName = models.CharField(db_column='videoname', blank=True,max_length=255)
    creative = models.CharField(db_column='creative', max_length=2000) 
    class Meta:
        managed = False
        db_table = 'videodetails'


class TbapproverQuestion(models.Model):
    questionid = models.CharField(db_column='questionid', primary_key=True, max_length=255)  # Field name made lowercase.
    questiontext = models.CharField(db_column='questiontext', max_length=2000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tb_approverquestion'



#extend django user class
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.CharField(db_column='UserID', blank=True, max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', blank=True,max_length=255)  # Field name made lowercase.
    userroleid = models.CharField(db_column='UserRoleId', blank=True,max_length=255)  # Field name made lowercase.
    vendor=models.CharField(db_column='Vendor', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='email', blank=True,max_length=255)
    profile_pic = models.ImageField(default = "\media\Profile\Default.jpg",null=True, blank=True)

    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()