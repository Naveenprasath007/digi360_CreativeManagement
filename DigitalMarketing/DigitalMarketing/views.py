from django.shortcuts import render,redirect,HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import *
from .models import TbVideo,Campaignvideo,TbCampaignquestion,Campaignquestionresponse,TbQuestion,TbUserrole,cVideoId,TbStatus,TbUser,TbApprove,video_Details,TbapproverQuestion,Profile
import pandas as pd
import json
import whisper
import uuid
from django.contrib import messages
from django.db import connection
import os
from datetime import datetime
import ast
from django.template.defaulttags import register
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.decorators import login_required
import pathlib
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.template.loader import render_to_string
from datetime import date


today = date.today()
today=today.strftime("%b_%d_%Y")




@login_required(login_url='/')
def uploadfile(request,id):
        if request.method == "POST":
            folder='media/'+str(today)+'/' 
            type=request.POST.get('creative')
            myfile = request.FILES['fileToUpload']
            fs = FileSystemStorage(location=folder)

            file_ext = fs.url(myfile)

            allowed_file_types = {
            'Video': ('.mp4', '.ogg', '.mov'),  
            'Image': ('.jpg', '.jpeg', '.png'), 
            'Gif': ('.gif',),
            }
            file_extension = pathlib.Path(file_ext).suffix.lower()
            if file_extension not in allowed_file_types.get(type, ()):
                messages.warning(request, 'Invalid file type for the selected creative type')
                return redirect('/dm/uploadfile/'+ id)

            file = fs.save(myfile.name.replace(" ", ""), myfile)
            url = fs.url(file)
            filename=file
            VID = uuid.uuid4()
            VID=str(VID)
            return redirect('/dm/createrupload/'+id+'/'+str(filename)+'/'+type+'/'+VID)
        else:
            a=id
            username=Profile.objects.get(userid = id)
            userroleid = username.userroleid
            print(userroleid)
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename
            print(userrolename)
            getdetails="yes"
            uploadfile='yes'
            uploadform='yes'
            userdetails=Profile.objects.get(userid = id)
            return render(request,'tc_DigitalMarketing/upload-page.html',{'k':a,'userrolename':userrolename,
                                                                             'id':id,'Uploadfile':uploadfile,
                                                                             'uploadform':uploadform,'userdetails':userdetails})



@login_required(login_url='/')
def creater_upload(request,id,fname,type,vid):
    try:
        if request.method == "POST":
            
            Vendor=request.POST.get('Vendor')
            Lob=request.POST.get('LOB')
            Platform=request.POST.getlist('Platform')
            upload=request.POST.get('Upload')
            Creator=request.POST.get('Creator')
            Title=request.POST.get('title')
            question = request.POST.getlist('question')
            Qlist=list(filter(None,question))
            folder='/media/'+str(today)+'/' 

            print(vid)
            fname=str(fname)
            Creative=type
            VID=vid

            if upload == "Upload":
                    if type == 'Image':
                        image_url = folder+fname
                        Gif_url = '--'
                        video_url = '--'

                        video_details2 = TbVideo(videoid=VID,videoname=Title,
                        previousvideoid=0,videotranscription='--',
                        vendor=Vendor,lob=Lob,creative=Creative,
                        platform=Platform,creater=Creator,Gifurl=Gif_url,
                        Imageurl=image_url)
                        
                        video_details2.save()
                        
                        video_details2 = TbVideo(videoid=VID,videoname=Title,
                        previousvideoid=0,videotranscription='--',videopath=video_url,
                        videopath1='--',videopath2='--',
                        vendor=Vendor,lob=Lob,creative=Creative,
                        platform=Platform,creater=Creator,Gifurl=Gif_url,
                        Imageurl=image_url)
                            
                        video_details2.save()

                        video_details3 = Campaignvideo(campaignvideoid=VID,
                                        videoid=TbVideo.objects.get(videoid = VID)
                                        ,campaignid=1,previousvideoid=0)
                        video_details3.save()

                        username=Profile.objects.get(userid = id)
                        urid = username.userroleid
                        user=TbUser.objects.get(userid=id)
                        UN=user.username

                        video_details4 = TbCampaignquestion(campaignquestionid=str(VID)+str(1),
                        campaignvideoid=Campaignvideo.objects.get(campaignvideoid=VID)
                        ,userroleid=TbUserrole.objects.get(userroleid=urid),
                        questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                        status = TbStatus(userid=TbUser.objects.get(userid=id),videoid=VID,status='Pending',videoname=Title,approver='---',uploadername=UN,
                                        videoPath=video_url,videoPath1='--',videoPath2='--',platform=Platform,Imageurl=image_url,Gifurl=Gif_url,creative=Creative)
                        status.save()

                        videoDetails = video_Details(userid=TbUser.objects.get(userid=id),VideoPath=video_url,VideoName=Title,creative=Creative)
                        videoDetails.save()


                        userrolename=TbUserrole.objects.get(userroleid = urid)
                        userrolename=userrolename.userrolename
                        print(userrolename)
                        # finalsubmit='yes'

                        if userrolename=='Uploader':
                            messages.success(request, 'submitted succesfully')
                            return redirect('/dm/uploaderdashboard/'+id)
                        elif userrolename=='Reviewer':
                            messages.success(request, 'submitted succesfully')
                            return redirect('/dm/approver/'+id)
                        else:
                            messages.success(request, 'submitted succesfully')
                            return redirect('/dm/superadmin/'+id)

                    elif type == 'Gif':
                        Gif_url = folder+fname
                        image_url = '--'
                        video_url = '--'

                        video_details2 = TbVideo(videoid=VID,videoname=Title,
                        previousvideoid=0,videotranscription='--',
                        vendor=Vendor,lob=Lob,creative=Creative,
                        platform=Platform,creater=Creator,Gifurl=Gif_url,
                        Imageurl=image_url)
                        
                        video_details2.save()
                        
                        video_details2 = TbVideo(videoid=VID,videoname=Title,
                        previousvideoid=0,videotranscription='--',videopath=video_url,
                        videopath1='--',videopath2='--',
                        vendor=Vendor,lob=Lob,creative=Creative,
                        platform=Platform,creater=Creator,Gifurl=Gif_url,
                        Imageurl=image_url)
                            
                        video_details2.save()

                        video_details3 = Campaignvideo(campaignvideoid=VID,
                                        videoid=TbVideo.objects.get(videoid = VID)
                                        ,campaignid=1,previousvideoid=0)
                        video_details3.save()

                        username=Profile.objects.get(userid = id)
                        urid = username.userroleid
                        user=TbUser.objects.get(userid=id)
                        UN=user.username

                        video_details4 = TbCampaignquestion(campaignquestionid=str(VID)+str(1),
                        campaignvideoid=Campaignvideo.objects.get(campaignvideoid=VID)
                        ,userroleid=TbUserrole.objects.get(userroleid=urid),
                        questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                        status = TbStatus(userid=TbUser.objects.get(userid=id),videoid=VID,status='Pending',videoname=Title,approver='---',uploadername=UN,
                                        videoPath=video_url,videoPath1='--',videoPath2='--',platform=Platform,Imageurl=image_url,Gifurl=Gif_url,creative=Creative)
                        status.save()

                        videoDetails = video_Details(userid=TbUser.objects.get(userid=id),VideoPath=video_url,VideoName=Title,creative=Creative)
                        videoDetails.save()


                        userrolename=TbUserrole.objects.get(userroleid = urid)
                        userrolename=userrolename.userrolename
                        print(userrolename)
                        # finalsubmit='yes'

                        if userrolename=='Uploader':
                            messages.success(request, 'submitted succesfully')
                            return redirect('/dm/uploaderdashboard/'+id)
                        elif userrolename=='Reviewer':
                            messages.success(request, 'submitted succesfully')
                            return redirect('/dm/approver/'+id)
                        else:
                            messages.success(request, 'submitted succesfully')
                            return redirect('/dm/superadmin/'+id)


                    elif type == 'Video':                        
                        video_url =folder+fname
                        image_url = '--'
                        Gif_url = '--'

                    # if Creative != 'Video':
                        video_details2 = TbVideo(videoid=VID,videoname=Title,
                                    previousvideoid=0,videotranscription='--',
                                    vendor=Vendor,lob=Lob,creative=Creative,
                                    platform=Platform,creater=Creator,Gifurl=Gif_url,
                                    Imageurl=image_url)
                        
                        video_details2.save()
                        
                        video_details2 = TbVideo(videoid=VID,videoname=Title,
                        previousvideoid=0,videotranscription='--',videopath=video_url,
                        videopath1='--',videopath2='--',
                        vendor=Vendor,lob=Lob,creative=Creative,
                        platform=Platform,creater=Creator,Gifurl=Gif_url,
                        Imageurl=image_url)
                            
                        video_details2.save()

                        video_details3 = Campaignvideo(campaignvideoid=VID,
                                        videoid=TbVideo.objects.get(videoid = VID)
                                        ,campaignid=1,previousvideoid=0)
                        video_details3.save()

                        username=Profile.objects.get(userid = id)
                        urid = username.userroleid
                        user=TbUser.objects.get(userid=id)
                        UN=user.username

                        video_details4 = TbCampaignquestion(campaignquestionid=str(VID)+str(1),
                        campaignvideoid=Campaignvideo.objects.get(campaignvideoid=VID)
                        ,userroleid=TbUserrole.objects.get(userroleid=urid),
                        questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                        status = TbStatus(userid=TbUser.objects.get(userid=id),videoid=VID,status='Pending',videoname=Title,approver='---',uploadername=UN,
                                        videoPath=video_url,videoPath1='--',videoPath2='--',platform=Platform,Imageurl=image_url,Gifurl=Gif_url,creative=Creative)
                        status.save()

                        videoDetails = video_Details(userid=TbUser.objects.get(userid=id),VideoPath=video_url,VideoName=Title,creative=Creative)
                        videoDetails.save()

                        data=TbQuestion.objects.all()

                        dataQ = TbCampaignquestion.objects.filter(campaignvideoid=VID)
                        listOfDataQ=[]
                        for i in dataQ:
                            output=i.questionid
                            listOfDataQ.append(output)
                        lenOfList=len(listOfDataQ)

                        listOfQuestion=[]
                        for i in listOfDataQ:
                            output=i.questiontext
                            listOfQuestion.append(output)
                        questionsText = {}
                        for i in range(0,lenOfList):
                            QT=listOfQuestion[i]
                            questionsText["q"+str(i)] = QT

                        listOfQuestionResponse=[]
                        for i in listOfDataQ:
                            output=i.questionresponse.split("|")
                            listOfQuestionResponse.append(output)

                        QuestionResponse = {}
                        for i in range(0,lenOfList):
                            lQR=listOfQuestionResponse[i]
                            QuestionResponse["k"+str(i)] = lQR

                        print(data)
                        userrolename=TbUserrole.objects.get(userroleid = urid)
                        userrolename=userrolename.userrolename
                        print(userrolename)
                        finalsubmit='yes'

                        return render(request,'tc_DigitalMarketing/upload-page.html',{"k":id,'userrolename':userrolename,'id':id,
                                                                                    'imgurl':image_url,'gifurl':Gif_url,
                                                                                    'finalsubmit':finalsubmit,'fname':fname})


            elif upload =='transcribe':
                    try:
                        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        folder='/media/'+str(today)+'/' 
                        file_path=BASE_DIR+folder+fname
                        print(file_path)

                        model = whisper.load_model("tiny")
                        result = model.transcribe(file_path)
                        print(result["text"])
                        text=result["text"]
                        # return result["text"]
                        username=Profile.objects.get(userid = id)
                        urid = username.userroleid
                        user=TbUser.objects.get(userid=id)
                        UN=user.username
                        userrolename=TbUserrole.objects.get(userroleid = urid)
                        userrolename=userrolename.userrolename
                        print(userrolename)
                        finalsubmit='yes'

                    except Exception as e:
                        text="The transcription of this video is not supported."
                        username=Profile.objects.get(userid = id)
                        urid = username.userroleid
                        user=TbUser.objects.get(userid=id)
                        UN=user.username
                        userrolename=TbUserrole.objects.get(userroleid = urid)
                        userrolename=userrolename.userrolename
                        print(userrolename)
                        finalsubmit='yes'
                    print(text)
                    return render(request,'tc_DigitalMarketing/upload-page.html',{"k":id,'userrolename':userrolename,'id':id,
                                                                                'finalsubmit':finalsubmit,'fname':fname,'text':text})


            else:
                folder='media/'+str(today)+'/' 
                text=request.POST.get('text')
                switch=request.POST.get('switch')
                ascpect1=request.POST.get('ascpect1')
                ascpect2=request.POST.get('ascpect2')
                if ascpect1:
                    myfile = request.FILES['file2']
                    fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
                    filename = fs.save(myfile.name.replace(" ", ""), myfile)
                    video_url1="/"+folder+str(filename)
                else:
                    video_url1='--'
                if ascpect2:
                    myfile = request.FILES['file3']
                    fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
                    filename = fs.save(myfile.name.replace(" ", ""), myfile)
                    video_url2="/"+folder+str(filename)
                else:
                    video_url2='--'

                print(video_url1)
                print(video_url2)
                if switch == 'yes':
                    ans='yes'
                else: 
                    ans='no'
                
                tbvideo = TbVideo.objects.get(videoid=VID)
                tbvideo.videotranscription=text
                tbvideo.videopath1=video_url1
                tbvideo.videopath2=video_url2
                tbvideo.save()

                status = TbStatus.objects.get(videoid=VID)
                status.videoPath1=video_url1
                status.videoPath2=video_url2
                status.save() 

                username=Profile.objects.get(userid = id)
                urid = username.userroleid

                user=TbUser.objects.get(userid=id)
                UN=user.username
                userrolename=TbUserrole.objects.get(userroleid = urid)
                userrolename=userrolename.userrolename
                print(userrolename)


                if userrolename=='Uploader':
                    messages.success(request, 'submitted succesfully')
                    return redirect('/dm/uploaderdashboard/'+id)
                elif userrolename=='Reviewer':
                    messages.success(request, 'submitted succesfully')
                    return redirect('/dm/approver/'+id)
                else:
                    messages.success(request, 'submitted succesfully')
                    return redirect('/dm/superadmin/'+id)
                
        else:
            folder='/media/'+str(today)+'/' 
            a=id
            username=Profile.objects.get(userid = id)
            userroleid = username.userroleid
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename
            submitform="yes"
            uploadform="yes"
            url=folder+fname
            print(url)
            userdetails=Profile.objects.get(userid = id)


            return render(request,'tc_DigitalMarketing/upload-page.html',{'k':a,'userrolename':userrolename,
                                                                                'id':id,'submitform':submitform,
                                                                                'creative':type,'url':url
                                                                                ,'uploadform':uploadform,"userdetails":userdetails})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

      
def transcribe_video_audio(video_path):
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = BASE_DIR+video_path
        print(file_path)
        model = whisper.load_model("tiny")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return "The transcription of this video is not supported."


def unique_numbers(numbers):
    # this will take only unique numbers from the tuple
    return tuple(set(numbers))


@login_required(login_url='/')
def approver(request,id):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/createrupload.html')
        else:
            #this try catch i need to modify 
            try:
                userName=connection.cursor()
                userName.execute("select UserName from tb_User where UserID='{val}';".format(val=id))
                userName=userName.fetchall()
                UN=userName[0][0]
                status=TbStatus.objects.all().order_by('-createddate').values()
                recent=TbStatus.objects.filter(status = 'Pending' ).order_by('-createddate').values()[:4]
                user_status=TbStatus.objects.filter(approver = UN)
                q = user_status.values()
                # q = status.values()
                df = pd.DataFrame.from_records(q)
                if len(df) == 0:
                    val=id
                    Approved = 0
                    Rejected = 0


                    q1 = status.values()
                    df = pd.DataFrame.from_records(q1)
                    filter1 =df["status"].isin(['Pending'])
                    Pending = df[filter1]
                    Pending =len(Pending)


                    filter4 =df["creative"].isin(['image','GIF'])
                    upload_img_gif = df[filter4]
                    upload_img_gif_count =len(upload_img_gif)
                    print(upload_img_gif_count)


                    df['createddate']=df['createddate'].astype(str)
                    df['createddate']=df['createddate'].str.slice(0, -15)
                    video_count = df.groupby('createddate')['videoname'].count().reset_index()
                    DateValue=video_count['createddate'].values.tolist()
                    videoC=video_count['videoname'].values.tolist()
                    print(videoC)
                    print(DateValue)

                    file_type_counts = df['creative'].value_counts().reset_index()
                    file_type_counts.columns = ['File_Type', 'Count']
                    File_Type=file_type_counts['File_Type'].values.tolist()
                    File_TypeC=file_type_counts['Count'].values.tolist()
                    creators = Profile.objects.filter(userroleid='U1')
                    return render(request,'tc_DigitalMarketing/approver_index.html',{'status':status,'id':id,'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                                'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                                'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent,'creators':creators})

                filter2 =df["status"].isin(['Rejected'])
                Rejected = df[filter2]
                Rejected =len(Rejected)
                filter3 =df["status"].isin(['Approved'])
                Approved = df[filter3]
                Approved =len(Approved)

                q1 = status.values()
                df = pd.DataFrame.from_records(q1)
                filter1 =df["status"].isin(['Pending'])
                Pending = df[filter1]
                Pending =len(Pending)


                filter4 =df["creative"].isin(['image','GIF'])
                upload_img_gif = df[filter4]
                upload_img_gif_count =len(upload_img_gif)
                print(upload_img_gif_count)


                df['createddate']=df['createddate'].astype(str)
                df['createddate']=df['createddate'].str.slice(0, -15)
                video_count = df.groupby('createddate')['videoname'].count().reset_index()
                DateValue=video_count['createddate'].values.tolist()
                videoC=video_count['videoname'].values.tolist()
                print(videoC)
                print(DateValue)

                file_type_counts = df['creative'].value_counts().reset_index()
                file_type_counts.columns = ['File_Type', 'Count']
                File_Type=file_type_counts['File_Type'].values.tolist()
                File_TypeC=file_type_counts['Count'].values.tolist()
                print(File_Type)
                print(File_TypeC)
                creators = Profile.objects.filter(userroleid='U1')

                # return render(request,'tc_DigitalMarketing/approver.html',{'status':status,'id':id})
                return render(request,'tc_DigitalMarketing/approver_index.html',{'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                                'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                                'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent,
                                                                                'upload_img_gif_count':upload_img_gif_count,'creators':creators})
            except:
                return redirect('/dm/createrupload/'+str(val))

    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


@login_required(login_url='/')
def admin(request,id):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/admin_index.html')
        else:
            #this try catch i need to modify 
            try:
                userName=connection.cursor()
                userName.execute("select UserName from tb_User where UserID='{val}';".format(val=id))
                userName=userName.fetchall()
                UN=userName[0][0]
                status=TbStatus.objects.all().order_by('-createddate').values()
                recent=TbStatus.objects.filter(status = 'Pending' ).order_by('-createddate').values()[:4]
                user_status=TbStatus.objects.filter(approver = UN)
                q = user_status.values()
                # q = status.values()
                df = pd.DataFrame.from_records(q)
                if len(df) == 0:
                    val=id
                    Approved = 0
                    Rejected = 0


                    q1 = status.values()
                    df = pd.DataFrame.from_records(q1)
                    filter1 =df["status"].isin(['Pending'])
                    Pending = df[filter1]
                    Pending =len(Pending)


                    filter4 =df["creative"].isin(['image','GIF'])
                    upload_img_gif = df[filter4]
                    upload_img_gif_count =len(upload_img_gif)


                    df['createddate']=df['createddate'].astype(str)
                    df['createddate']=df['createddate'].str.slice(0, -15)
                    print(df['createddate'])
                    video_count = df.groupby('createddate')['videoname'].count().reset_index()
                    DateValue=video_count['createddate'].values.tolist()
                    videoC=video_count['videoname'].values.tolist()

                    file_type_counts = df['creative'].value_counts().reset_index()
                    file_type_counts.columns = ['File_Type', 'Count']
                    File_Type=file_type_counts['File_Type'].values.tolist()
                    File_TypeC=file_type_counts['Count'].values.tolist()
                    
                    userdetails=Profile.objects.get(userid = id)
                    creators = Profile.objects.filter(userroleid='U1')

                    return render(request,'tc_DigitalMarketing/admin_index.html',{'status':status,'id':id,'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                                'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                                'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent,'userdetails':userdetails,'creators':creators})
                    # return redirect('/dm/createrupload/'+str(val))
                # filter1 =df["status"].isin(['Pending'])
                # Pending = df[filter1]
                # Pending =len(Pending)
                filter2 =df["status"].isin(['Rejected'])
                Rejected = df[filter2]
                Rejected =len(Rejected)
                filter3 =df["status"].isin(['Approved'])
                Approved = df[filter3]
                Approved =len(Approved)

                q1 = status.values()
                df = pd.DataFrame.from_records(q1)
                filter1 =df["status"].isin(['Pending'])
                Pending = df[filter1]
                Pending =len(Pending)


                filter4 =df["creative"].isin(['image','GIF'])
                upload_img_gif = df[filter4]
                upload_img_gif_count =len(upload_img_gif)


                df['createddate']=df['createddate'].astype(str)
                df['createddate']=df['createddate'].str.slice(0, -15)
                print(df['createddate'])
                video_count = df.groupby('createddate')['videoname'].count().reset_index()
                DateValue=video_count['createddate'].values.tolist()
                videoC=video_count['videoname'].values.tolist()
                print(DateValue)

                file_type_counts = df['creative'].value_counts().reset_index()
                file_type_counts.columns = ['File_Type', 'Count']
                File_Type=file_type_counts['File_Type'].values.tolist()
                File_TypeC=file_type_counts['Count'].values.tolist()
                
                userdetails=Profile.objects.get(userid = id)
                creators = Profile.objects.filter(userroleid='U1')

                # return render(request,'tc_DigitalMarketing/approver.html',{'status':status,'id':id})
                return render(request,'tc_DigitalMarketing/admin_index.html',{'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                                'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                                'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent,'userdetails':userdetails,
                                                                                'creators':creators})
            except:
                return redirect('/dm/Activation/'+str(id))

    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


@login_required(login_url='/')
def approver_view(request,id,uid):
    try:
        if request.method == "POST":
                #rechecking is pending
                q0 = request.POST.get('q0')
                q1 = request.POST.get('q1')
                q2 = request.POST.get('q2')
                q3 = request.POST.get('q3')
                q4 = request.POST.get('q4')
                q5 = request.POST.get('q5')
                q6 = request.POST.get('q6')
                Qlist=[q0,q1,q2,q3,q4,q5,q6]
                # Qlist=request.POST.getlist('questions')
                tb = request.POST.get('ReasonTextbox')
                transcription = request.POST.get('cmdtranscript')
                print(transcription)

                command1 = request.POST.get('command1')
                command2 = request.POST.get('command2')
                command3 = request.POST.get('command3')
                commandlist=[command1,command2,command3]
                

                inlineRadioOptions1= request.POST.get('inlineRadioOptions1')
                inlineRadioOptions2= request.POST.get('inlineRadioOptions2')
                inlineRadioOptions3= request.POST.get('inlineRadioOptions3')
                qResList=[inlineRadioOptions1,inlineRadioOptions2,inlineRadioOptions3]



                # i need to check
                Qlist=list(filter(None,Qlist))
                btn=request.POST.get('btn')
                
                qResList=list(filter(None,qResList))
                Total=qResList.count("Yes")
                print(Total)
                print(len(qResList))

                
                if Total == len(qResList):  


                    video=TbVideo.objects.get(videoid =id)
                    vP=video.videopath
                    vN=video.videoname
                    vP1=video.videopath1
                    vP2=video.videopath2
                    pN=video.platform

                    user=TbUser.objects.get(userid=uid)
                    getApproverName=user.username
                    print(getApproverName)
                    
                    userName=connection.cursor()
                    userName.execute("select UserName from tb_User where UserID='{val}'".format(val=uid))
                    userName=userName.fetchall()
                    UN=userName[0][0]
                    
                    approve = TbApprove(userid=TbUser.objects.get(userid=uid),
                                        videoid=id,videotitle=vN,videopath=vP,videopath1=vP1,uploadername=UN)
                    approve.save()

                    Question = TbapproverQuestion.objects.all()
                    l=[]
                    res = {}
                    for key in Question:
                        for value in qResList:
                            res[key.questiontext] = value
                            qResList.remove(value)
                            break   

                    res_command = {}
                    for key in Question:
                        for value in commandlist:
                            res_command[key.questiontext] = value
                            commandlist.remove(value)
                            break    
                    l.append(res)
                    l.append(res_command)
                    l.append(tb)
                    print(l)

                    video = TbStatus.objects.get(videoid=id)
                    video.status='Approved'
                    video.reason=l
                    video.approver=getApproverName
                    video.MainReason=tb
                    video.downloadaccess='Notyet'
                    video.save()

                    videodetails=TbVideo.objects.get(videoid=id)
                    if transcription != None:
                        videodetails.videotranscription=transcription
                    videodetails.save()


                    Campaignquestionresponse.objects.filter(campaignquestionid=id).delete()
                    TbCampaignquestion.objects.filter(campaignquestionid=id).delete()

                    username=Profile.objects.get(userid = uid)
                    userroleid = username.userroleid
                    print(userroleid)
                    userrolename=TbUserrole.objects.get(userroleid = userroleid)
                    userrolename=userrolename.userrolename
                    print(userrolename)

                    # messages.success(request, 'Approved succesfully')
                    # return redirect('/dm/approver/'+str(uid))

                    # deleteQuestionsres=connection.cursor()
                    # deleteQuestionsres.execute("DELETE campaignquestionresponse FROM campaignquestionresponse INNER JOIN tb_campaignquestion ON campaignquestionresponse.campaignquestionid = tb_campaignquestion.campaignquestionid WHERE tb_campaignquestion.campaignvideoid='{value}';".format(value=id))
                    # cqr.delete()
                    # cq.delete()

                    if userrolename=='Reviewer':
                        messages.success(request, 'Approved succesfully')
                        return redirect('/dm/approver/'+str(uid))

                    else:
                        messages.success(request, 'Approved succesfully')
                        return redirect('/dm/superadmin/'+str(uid))


                else:
                    # NO NEED THIS CODE /25/6/23
                    # deletestatus=connection.cursor()
                    # deletestatus.execute("DELETE FROM tb_Status WHERE videoID='{value}';".format(value=id))
                    
                    video=TbVideo.objects.get(videoid =id)
                    vP=video.videopath
                    vN=video.videoname
                    vP1=video.videopath1
                    vP2=video.videopath2
                    pN=video.platform

                    user=TbUser.objects.get(userid=uid)
                    getApproverName=user.username
                    print(getApproverName)
                    
                    userName=connection.cursor()
                    userName.execute("select UserName from tb_User where UserID='{val}'".format(val=uid))
                    userName=userName.fetchall()
                    UN=userName[0][0]
                    


                    Question = TbapproverQuestion.objects.all()
                    l=[]
                    res = {}
                    for key in Question:
                        for value in qResList:
                            res[key.questiontext] = value
                            qResList.remove(value)
                            break   

                    res_command = {}
                    for key in Question:
                        for value in commandlist:
                            res_command[key.questiontext] = value
                            commandlist.remove(value)
                            break    
                    l.append(res)
                    l.append(res_command)
                    l.append(tb)
                    print(l)


                    video = TbStatus.objects.get(videoid=id)
                    video.status='Rejected'
                    video.reason=l
                    video.approver=getApproverName
                    video.MainReason=tb
                    video.save()

                    videodetails=TbVideo.objects.get(videoid=id)
                    if transcription != None:
                        videodetails.videotranscription=transcription
                    videodetails.save()



                    # ____new Delete lines added here__
                    # deleteQuestionsres=connection.cursor()
                    # deleteQuestionsres.execute("DELETE CampaignQuestionResponse FROM CampaignQuestionResponse inner join tb_CampaignQuestion on CampaignQuestionResponse.CampaignQuestionID = tb_CampaignQuestion.CampaignQuestionID WHERE tb_CampaignQuestion.CampaignVideoID='{value}';".format(value=id))
                    Campaignquestionresponse.objects.filter(campaignquestionid=id).delete()
                    TbCampaignquestion.objects.filter(campaignquestionid=id).delete()
                    
                    username=Profile.objects.get(userid = uid)
                    userroleid = username.userroleid
                    print(userroleid)
                    userrolename=TbUserrole.objects.get(userroleid = userroleid)
                    userrolename=userrolename.userrolename
                    print(userrolename)
                    
                    # messages.error(request, 'rejected succesfully')
                    # return redirect('/dm/approver/'+str(uid))
            # return render(request,'tc_DigitalMarketing/approverview.html',{})
                    if userrolename=='Reviewer':
                        messages.success(request, 'rejected succesfully')
                        return redirect('/dm/approver/'+str(uid))

                    else:
                        messages.success(request, 'rejected succesfully')
                        return redirect('/dm/superadmin/'+str(uid))

        else:
            CVID=id
            dataQ = TbCampaignquestion.objects.filter(campaignvideoid=CVID)
            listOfDataQ=[]
            for i in dataQ:
                output=i.questionid
                listOfDataQ.append(output)
            lenOfList=len(listOfDataQ)

            listOfQuestion=[]
            for i in listOfDataQ:
                output=i.questiontext
                listOfQuestion.append(output)
            questionsText = {}
            for i in range(0,lenOfList):
                QT=listOfQuestion[i]
                questionsText["q"+str(i)] = QT

            print(questionsText)

            listOfQuestionResponse=[]
            for i in listOfDataQ:
                output=i.questionresponse.split("|")
                listOfQuestionResponse.append(output)

            QuestionResponse = {}
            for i in range(0,lenOfList):
                lQR=listOfQuestionResponse[i]
                QuestionResponse["k"+str(i)] = lQR

            uploaderName=connection.cursor()
            uploaderName.execute("select UploaderName from tb_Status where VideoID='{val}'".format(val=id))
            uploaderName=uploaderName.fetchall()
            uploaderName=uploaderName[0][0]


            
            Question = TbapproverQuestion.objects.all()

            

            # ___This for get question and responces__
            cursor=connection.cursor()
            cursor.execute("select QuestionText,Response from CampaignQuestionResponse cqr inner join tb_CampaignQuestion cquestion on cqr.CampaignQuestionID = cquestion.CampaignQuestionID AND cquestion.CampaignVideoID ='{value}' inner join tb_Question question on cquestion.QuestionID = question.QuestionID;".format(value=CVID))
            result=cursor.fetchall()
            print(result)
            
            video=TbVideo.objects.get(videoid = CVID)
            vP=video.videopath
            vT=video.videotranscription
            vN=video.videoname
            Platform=video.platform
            vP1=video.videopath1
            vP2=video.videopath2
            LOB=video.lob
            imgUrl=video.Imageurl
            gifUrl=video.Gifurl
            Creative=video.creative
            Vendor=video.vendor


            print(gifUrl)
            print(imgUrl)
            print(Creative)
            print(vP)
            print(vP1)
            print(vP2)


            username=Profile.objects.get(userid = uid)
            userroleid = username.userroleid
            print(userroleid)
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename
            print(userrolename)
            userdetails=Profile.objects.get(userid = uid)

            return render(request,'tc_DigitalMarketing/approverviewnew.html',{'qT':questionsText,
                                                                              'qR':QuestionResponse,
                                                                              'uploaderName':uploaderName,
                                                                              'R':result,
                                                                              'url':vP,
                                                                              'Transcribe':vT,
                                                                              'vname':vN,
                                                                              'id':uid,
                                                                              'url1':vP1,
                                                                              'url2':vP2,
                                                                              'Vendor':Vendor,
                                                                              'LOB':LOB,
                                                                              'Creative':Creative,
                                                                              'Platform':Platform,
                                                                              'Questions':Question,
                                                                              'imgUrl':imgUrl,
                                                                              'gifUrl':gifUrl,
                                                                              'userrolename':userrolename,"userdetails":userdetails})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  



@login_required(login_url='/')
def status_view(request,id1,uid):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/createrupload.html')
        else:
            # status=Status.objects.filter(userid=id)
            print(id1)
            status=connection.cursor()
            status.execute("select reason,UploaderName FROM tb_Status WHERE VideoID='{value1}';".format(value1=id1))
            response=status.fetchall()

            video=TbVideo.objects.get(videoid = id1)
            vP=video.videopath
            vP1=video.videopath1
            vP2=video.videopath2
            vT=video.videotranscription
            vN=video.videoname
            Platform=video.platform
            LOB=video.lob
            imgUrl=video.Imageurl
            gifUrl=video.Gifurl
            Creative=video.creative
            Vendor=video.vendor
            print(Creative)


            import ast
            res = ast.literal_eval(response[0][0])

            print(res)

            username=Profile.objects.get(userid = uid)
            userroleid = username.userroleid
            print(userroleid)
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename
            userdetails=Profile.objects.get(userid = uid)
            return render(request,'tc_DigitalMarketing/statusview.html',{'approverres':res[0],
                                                                        'approvercmd':res[1],
                                                                        'reason':res[2],
                                                                        'id':uid,
                                                                        'url':vP,
                                                                        'vid':id1,
                                                                        'Transcribe':vT,
                                                                        'vname':vN,
                                                                        'url1':vP1,
                                                                        'url2':vP2,
                                                                        'Vendor':Vendor,
                                                                        'LOB':LOB,
                                                                        'Creative':Creative,
                                                                        'Platform':Platform,
                                                                        'uploadername':response[0][1],
                                                                        'imgUrl':imgUrl,
                                                                        "gifUrl":gifUrl,
                                                                        'userdetails':userdetails,
                                                                        'userrolename':userrolename,
                                                                        })
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


@login_required(login_url='/')
def uploaderdashboard(request,id):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/dash_index.html',{})
        userName=connection.cursor()
        userName.execute("select UserName from tb_User where UserID='{val}'".format(val=id))
        userName=userName.fetchall()
        UN=userName[0][0]
        status=TbStatus.objects.filter(userid=id).order_by('-createddate').values()
        recent=TbStatus.objects.filter(userid=id).order_by('-createddate').values()[:3]
        q = status.values()
        df = pd.DataFrame.from_records(q)
        if len(df) == 0:
            val=id
            return redirect('/dm/uploadfile/'+str(val))
        filter1 =df["status"].isin(['Pending'])
        Pending = df[filter1]
        Pending =len(Pending)
        filter2 =df["status"].isin(['Rejected'])
        Rejected = df[filter2]
        Rejected =len(Rejected)
        filter3 =df["status"].isin(['Approved'])
        Approved = df[filter3]
        Approved =len(Approved)
        filter4 =df["creative"].isin(['image','GIF'])
        upload_img_gif = df[filter4]
        upload_img_gif_count =len(upload_img_gif)

        #  = pd.to_datetime(df['createddate'])
        df['createddate']=df['createddate'].astype(str)
        # print(df['createddate'])
        df['createddate']=df['createddate'].str.slice(0, -15)
        print(df['createddate'])
        video_count = df.groupby('createddate')['videoname'].count().reset_index()
        DateValue=video_count['createddate'].values.tolist()
        videoC=video_count['videoname'].values.tolist()

        print(video_count)

        file_type_counts = df['creative'].value_counts().reset_index()
        file_type_counts.columns = ['File_Type', 'Count']
        File_Type=file_type_counts['File_Type'].values.tolist()
        File_TypeC=file_type_counts['Count'].values.tolist()
        userdetails=Profile.objects.get(userid = id)
        admin_approver = Profile.objects.filter(userroleid='S1') | Profile.objects.filter(userroleid='R1') 
        
        return render(request,'tc_DigitalMarketing/dash_index.html',{'id':id,'status':status,'Approved':Approved,'Rejected':Rejected,'Pending':Pending,'UserName':UN,
                                                                     'DateValue':DateValue,"videoC":videoC,'upload_img_gif_count':upload_img_gif_count,'File_Type':File_Type,
                                                                     'File_TypeC':File_TypeC,'recent':recent,'admin_approver':admin_approver,'userdetails':userdetails
                                                                     })
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
    
@login_required(login_url='/')
def filterpage(request,id,id1,id2):
    try:
        if request.method == "POST":
             return render(request,'tc_DigitalMarketing/filterpage.html',{'id':id,'status':status,})
        
        user_status=""
        status=""
        videodetails=""
        if id2 == 'User':
            status=TbStatus.objects.filter(userid=id,status=id1).order_by('-createddate').values()

        elif id2 == 'Apporver':
            userName=connection.cursor()
            userName.execute("select UserName from tb_User where UserID='{val}';".format(val=id))
            userName=userName.fetchall()
            UN=userName[0][0]
            user_status=TbStatus.objects.filter(approver=UN,status=id1).order_by('-createddate').values()
        
        elif id1 == 'Pending': 
            user_status=TbStatus.objects.filter(status=id1).order_by('-createddate').values()

        username=Profile.objects.get(userid = id)
        userroleid = username.userroleid
        print(userroleid)
        userrolename=TbUserrole.objects.get(userroleid = userroleid)
        userrolename=userrolename.userrolename
        print(userrolename)
        userdetails=Profile.objects.get(userid = id)
        return render(request,'tc_DigitalMarketing/filterpage.html',{'id':id,'status':status,
                                                                     'user_status':user_status
                                                                     ,'userrolename':userrolename,
                                                                     'userdetails':userdetails})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
    
@login_required(login_url='/')
def myvideos(request,id):
    try:
        if request.method == "POST":
             return render(request,'tc_DigitalMarketing/myvideos.html',{'id':id})
        videodetails=video_Details.objects.filter(userid=id)
        userdetails=Profile.objects.get(userid = id)
        return render(request,'tc_DigitalMarketing/myvideos.html',{'id':id,'videodetails':videodetails,
                                                                   'userdetails':userdetails})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  



@login_required(login_url='/')
def download_view(request,id,id1):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/downloadview.html')
        else:
            # status=Status.objects.filter(userid=id)
            print(id1)
            status=connection.cursor()
            status.execute("select reason FROM tb_Status WHERE userid='{value}' AND VideoID='{value1}';".format(value=id,value1=id1))
            response=status.fetchall()

            approvedvideos=connection.cursor()
            approvedvideos.execute("select reason FROM tb_Approve WHERE userid='{value}' AND VideoID='{value1}';".format(value=id,value1=id1))
            response=approvedvideos.fetchall()

            cursor1=connection.cursor()
            cursor1.execute("select VideoPath,VideoName from CampaignVideo cv inner join tb_Video v on v.VideoID=cv.VideoID AND cv.CampaignVideoID='{val}'".format(val=id1))
            VideoDeatails=cursor1.fetchall()
            vP='/'+VideoDeatails[0][0]
            vName=VideoDeatails[0][1]

            import ast
            res = ast.literal_eval(response[0][0])


            datas = []
            for item in res[1].items:
                # create new dictionary combining values required
                data = {'name':item.name, 'rev':item.rev, 'val':item.val}
                datas.append(data)
            print(datas)

            print(res)
            return render(request,'tc_DigitalMarketing/downloadview.html',{'approverres':res[0],'approvercmd':res[1],'reason':res[2],'id':id,'video':vP,'vname':vName,'vid':id1,})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

@login_required(login_url='/')
def download(request,id):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/Download.html',{'approvedvid':approvedvid,})
        else:
            # status=TbStatus.objects.filter(userid=id).order_by('-createddate').values()
            approvedvid=TbApprove.objects.filter(downloadaccess = 'download')
            q = approvedvid.values()
            df = pd.DataFrame.from_records(q)
            df=df.fillna("0")
            print(df)
            filter1 = df.downloader.apply(lambda x: id in x)
            df = df[filter1]
            print(df)  

            json_records = df.reset_index().to_json(orient ='records')
            arr = []
            arr = json.loads(json_records)
            print(arr)
            return render(request,'tc_DigitalMarketing/Download.html',{'approvedvid1':approvedvid,'approvedvid':arr})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


def download_video(request,id):
        video=TbVideo.objects.get(videoid = id)
        vP=video.videopath
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = BASE_DIR+vP
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response

def delete_video(request,id,id1):
        cursor1=connection.cursor()
        cursor1.execute("select VideoName from CampaignVideo cv inner join tb_Video v on v.VideoID=cv.VideoID AND cv.CampaignVideoID='{val}'".format(val=id))
        VideoDeatails=cursor1.fetchall()
        vName=VideoDeatails[0][0]

        getpath=connection.cursor()
        getpath.execute("SELECT VideoPath FROM tb_Video WHERE videoID='{value}';".format(value=id))
        getpath=getpath.fetchall()
        v_path=getpath[0][0]
        print(v_path)

        deletestatus=connection.cursor()
        deletestatus.execute("DELETE FROM tb_Status WHERE videoID='{value}';".format(value=id))

        deleteQuestionsres=connection.cursor()
        deleteQuestionsres.execute("DELETE CampaignQuestionResponse FROM CampaignQuestionResponse inner join tb_CampaignQuestion on CampaignQuestionResponse.CampaignQuestionID = tb_CampaignQuestion.CampaignQuestionID WHERE tb_CampaignQuestion.CampaignVideoID='{value}';".format(value=id))
        # deleteQuestions.execute("DELETE FROM CampaignQuestionResponse CQR inner join tb_CampaignQuestion CQ on CQ.CampaignQuestionID = CQR.CampaignQuestionID WHERE CQ.CampaignVideoID='{value}';".format(value=id))
        
        
        # This for deleting videoID
        deleteQuestions=connection.cursor()
        deleteQuestions.execute("DELETE tb_CampaignQuestion WHERE CampaignVideoID='{value}';".format(value=id))

        deleteCampVideo=connection.cursor()
        deleteCampVideo.execute("DELETE CampaignVideo WHERE VideoID='{value}';".format(value=id))
       
        video=connection.cursor()
        video.execute("DELETE tb_Video WHERE VideoID='{value}';".format(value=id))


        os.remove(v_path)
        messages.error(request, 'Video Details Deleted succesfully')
        return redirect('/dm/createrupload/'+str(id1))

   

@login_required(login_url='/')
def upload_again(request,id,id1):
    try:
        Creative=request.POST.get('Creative')
        upload=request.POST.get('Upload')

        if request.method == "POST":
            if upload == 'Upload':
                image_url=''
                Gif_url=''
                url=''
                url1=''
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name.replace(" ", ""), myfile)
                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)
                # url=uploaded_file_url
                # text=videotranscribe(url1)
                # text=str(text)
                text='--'
                # UpdateQuery=connection.cursor()
                # UpdateQuery.execute("UPDATE tb_Video SET VideoPath1 = '{value1}' WHERE VideoID = '{value}';".format(value1=uploaded_file_url,value=id))

                if Creative == 'image':
                    image_url=uploaded_file_url
                    text='--'


                if Creative == 'Video':
                    url=uploaded_file_url
                    # url=url.replace("/",'\\')
                    # url=url.replace('%20',' ')
                    text=transcribe_video_audio(url)
                    # text=' Are you an American over 25 and earning less than $50,000? Well you might have already qualified for this $5,200 healthcare assistance program available in the US. Just CLICK the link below and see how much you might get back.'
                    # text='--'
                
                if Creative == 'GIF':
                    Gif_url=uploaded_file_url
                    # text=transcribe(url1)
                    text='--'

                record = TbVideo.objects.get(videoid=id)
                record.videopath1 = uploaded_file_url
                record.videotranscription1 = text
                record.Imageurl1=image_url
                record.Gifurl1=Gif_url
                record.save()
                videoDetails = video_Details(userid=TbUser.objects.get(userid=id1),VideoPath=uploaded_file_url)
                videoDetails.save()

                status = TbStatus.objects.get(videoid=id)
                status.videoPath1=uploaded_file_url
                status.save()



                status='Uploaded'
                return render(request,'tc_DigitalMarketing/uploadagainnew.html',{"video":url,'text':text,'id':id1,'status':status,
                                                                                'imgurl':image_url,'gifurl':Gif_url})

            messages.success(request, 'submitted succesfully')

            username=Profile.objects.get(userid = id1)
            userroleid = username.userroleid
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename 

            if userrolename=='Uploader':
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/uploaderdashboard/'+id1)
            elif userrolename=='Reviewer':
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/approver/'+id1)
            else:
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/superadmin/'+id1)
            # return redirect('/dm/uploaderdashboard/'+id1)

        
        else:
            status='Waiting'
            videodetails=video_Details.objects.filter(userid=id1)
            return render(request,'tc_DigitalMarketing/uploadagainnew.html',{'videodetails':videodetails,'status':status,'id':id1,})
        
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

def account(request,id):
    if request.method == "POST":
        folder='media/Profile/' 
        picture = request.FILES['profilepic']
        fs = FileSystemStorage(location=folder)
        filename = fs.save(picture.name.replace(" ", ""), picture)
        uploaded_file_url = '/'+folder+filename
        print(uploaded_file_url)
        profile=Profile.objects.get(userid = id)   
        profile.profile_pic=uploaded_file_url
        profile.save()


    profile=Profile.objects.get(userid = id)   
    return render(request,'tc_DigitalMarketing/account.html',{'context':profile})  

def login_view(request):
    try:
        # next = request.GET.get('next')
        # print(next)
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.profile.userroleid == "U1":
                
                return redirect('/dm/uploaderdashboard/'+str(user.profile.userid)) 
            if user.profile.userroleid == "R1":

                return redirect('/dm/approver/'+str(user.profile.userid))
            
            if user.profile.userroleid == "S1":

                return redirect('/dm/superadmin/'+str(user.profile.userid))   

            if user.profile.userroleid == "D1":
                
                return redirect('/dm/Download/'+str(user.profile.username))   


        context = {
            'form': form,
        }
        return render(request, "tc_DigitalMarketing/Login.html", context)

    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

def register_view(request):
    try:
        next = request.GET.get('next')
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email').lower()
            user.set_password(password)
            Role = form.cleaned_data.get('Role')
            Name = form.cleaned_data.get('Name')
            
            user.save()

            if Role == 'Creator':
                rid='U1'
            elif Role == 'Approver':
                rid='R1'
            elif Role == 'Downloader':
                rid='D1'     

            new_id = uuid.uuid4()
            str(new_id)

            profile=Profile.objects.get(user=user)
            profile.userid=new_id
            profile.username=Name
            profile.userroleid=''
            profile.vendor='adsparks'
            profile.email=email
            profile.save()
            # print(Role)
            
            tbuser=TbUser(userid=new_id,username=Name,userroleid=TbUserrole.objects.get(userroleid=rid),password='test',vendor='adsparks')
            tbuser.save()
    
            if Role == 'Creator':
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient = [user.email,]
                html = render_to_string('email\creator.html', {
                    'user_name': user.username,
                    'user_email': user.email,
                })
                send_mail('Welcome to Creative Management!', 'This is the message', email_from, recipient, html_message=html)
                print("messsage sent")

                # mail send to admin 
                recipient = ['sainath.guddemmagari@speridian.com','pranav.vijay@truecoverage.com','naveen.kumaran@truecoverage.com',]
                html = render_to_string('email\default.html', {
                    'user_name': user.username,
                    'user_email': user.email,
                    'user_Role' : Role,
                })
                send_mail('New to our plateform!', 'This is the message', email_from, recipient, html_message=html)
                print("default messsage sent")

            if Role == 'Approver':
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient = [user.email,]
                html = render_to_string('email\approver.html', {
                    'user_name': user.username,
                    'user_email': user.email,
                })
                send_mail('Welcome to Creative Management!', 'This is the message', email_from, recipient, html_message=html)
                print("messsage sent")

                # mail sendto admin 
                recipient = ['sainath.guddemmagari@speridian.com','pranav.vijay@truecoverage.com','naveen.kumaran@truecoverage.com',]
                html = render_to_string('email\default.html', {
                    'user_name': user.username,
                    'user_email': user.email,
                    'user_Role' : Role,
                })
                send_mail('New to our plateform!', 'This is the message', email_from, recipient, html_message=html)
                print("default messsage sent")

            if Role == 'Downloader':
                #adding download list in status table
                queryset = TbStatus.objects.all() 
                for q in queryset:
                    a=q.downloader 
                    print(a)
                    if a != None:
                        downloader_list = ast.literal_eval(a)
                        downloader_list.append(user.username)
                        print(a)
                        q.downloader = downloader_list
                        q.save()

                email_from = settings.DEFAULT_FROM_EMAIL
                recipient = [user.email,]
                html = render_to_string('email\downloader.html', {
                    'user_name': user.username,
                    'email': user.email,
                })
                send_mail('Welcome to Creative Management!', 'This is the message', email_from, recipient, html_message=html)
                print("messsage sent")

                recipient = ['sainath.guddemmagari@speridian.com','pranav.vijay@truecoverage.com','naveen.kumaran@truecoverage.com',]
                html = render_to_string('email\default.html', {
                    'user_name': user.username,
                    'user_email': user.email,
                    'user_Role' : Role,
                })
                send_mail('New to our plateform!', 'This is the message', email_from, recipient, html_message=html)
                print("default messsage sent")

            new_user = authenticate(username=user.username, password=password,)
            login(request, new_user)
            if next:
                messages.success(request, 'Account created successfully, awaiting activation')
                return redirect(next)
            messages.success(request, 'Account created successfully, awaiting activation')
            return redirect('/')

        context = {
            'form': form,
        }
        return render(request, "tc_DigitalMarketing/signup.html", context)
    
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


def activate(request,id):
    # try:
        if request.method == "POST":
            email = request.POST.get('email')
            status = request.POST.get('status')
            Role = request.POST.get('Role')
            print(email)
            print(status)
            print(Role)

            if status == 'Deactivate':
                profilesave=Profile.objects.get(email=email)
                profilesave.userroleid=''
                profilesave.save()
            else:
                profilesave=Profile.objects.get(email=email)
                profilesave.userroleid=Role
                profilesave.save()

                email_from = settings.DEFAULT_FROM_EMAIL
                recipient = [email,]
                html = render_to_string('email/activation.html')
                send_mail('Your Account Activated!', 'This is the message', email_from, recipient, html_message=html)
                print("messsage sent")

            messages.success(request, 'Profile Updated Successfully')
            return redirect ("/dm/Activation/"+id)
        
            # profile=Profile.objects.all()
            # return render(request, "tc_DigitalMarketing/activation.html",{"profile":profile})
        else:
            profile=Profile.objects.all()
            userdetails=Profile.objects.get(userid = id)
            return render(request, "tc_DigitalMarketing/activation.html",{"profile":profile,'id':id,"userdetails":userdetails})

    # except Exception as e:
    #     form = ActivationForm(request.POST or None)
    #     context = {
    #             'form': form,
    #         }
    #     messages.success(request, 'Your Details is not found')
    #     return render(request, "tc_DigitalMarketing/activation.html",context)


def logout_view(request):
    logout(request)
    return redirect('/')

    
@login_required(login_url='/')
def creater_update_video(request,id,id1):
    try:
        if request.method == "POST":
            q0 = request.POST.get('q0')
            q1 = request.POST.get('q1')
            q2 = request.POST.get('q2')
            q3 = request.POST.get('q3')
            q4 = request.POST.get('q4')
            q5 = request.POST.get('q5')
            q6 = request.POST.get('q6')
            Vendor=request.POST.get('Vendor')
            Lob=request.POST.get('LOB')
            Creative=request.POST.get('Creative')
            Platform=request.POST.get('Platform')
            upload=request.POST.get('Upload')
            Creater=request.POST.get('Creater')
            Qlist=[q0,q1,q2,q3,q4,q5,q6]
            Qlist=list(filter(None,Qlist))


            if upload == 'Upload':
                    image_url=''
                    Gif_url=''
                    url=''
                    url1=''
                    Title1=request.POST.get('Videotitle').capitalize()
                    myfile = request.FILES['myfile']
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name.replace(" ", ""), myfile)
                    uploaded_file_url = fs.url(filename)
                    print(uploaded_file_url)

                    if Creative == 'image':
                         image_url=uploaded_file_url
                         text='--'


                    if Creative == 'Video':
                        url=uploaded_file_url
                        url1=url[1:]
                        text=transcribe_video_audio(url)
                        #text=' Are you an American over 25 and earning less than $50,000? Well you might have already qualified for this $5,200 healthcare assistance program available in the US. Just CLICK the link below and see how much you might get back.'
                    
                    if Creative == 'GIF':
                        Gif_url=uploaded_file_url
                        # text=transcribe(url1)
                        text='--'

                    data=TbQuestion.objects.all()

                    # Generate a new UUID
                
                    new_id = id1
                    str(new_id)
                    print(str(new_id))

                    video_id = cVideoId(VideoID=new_id)
                    video_id.save()

                    T=Title1
                    # TbStatus.objects.get(videoid=id)



                    video_details2 = TbVideo(videoid=new_id,videoname=T,videopath=url1,
                                            previousvideoid=0,videotranscription=text,
                                            vendor=Vendor,lob=Lob,creative=Creative,
                                            platform=Platform,videopath1='--',
                                            videotranscription1='--',creater=Creater,
                                            Gifurl=Gif_url,Imageurl=image_url,Imageurl1='--',Gifurl1='--'
                                            )
                    video_details2.save()

                    video_details3 = Campaignvideo(campaignvideoid=new_id,
                                                videoid=TbVideo.objects.get(videoid = new_id)
                                                ,campaignid=1,previousvideoid=0)
                    video_details3.save()
                    
                    #config question based on platform
                    if Platform == 'Facebook':    
                        video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(1),
                                                    campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                                                    ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                                                    questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                        # video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(2),
                        #                             campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                        #                             ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                        #                             questionid=TbQuestion.objects.get(questionid='2'))
                        # video_details4.save()

                        # video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(3),
                        #                             campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                        #                             ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                        #                             questionid=TbQuestion.objects.get(questionid='3'))
                        # video_details4.save()

                        # video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(4),
                        #                             campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                        #                             ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                        #                             questionid=TbQuestion.objects.get(questionid='4'))
                        # video_details4.save()
                    
                    if Platform == 'Youtube':    

                        video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(3),
                                                    campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                                                    ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                                                    questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                        # video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(4),
                        #                             campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                        #                             ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                        #                             questionid=TbQuestion.objects.get(questionid='6'))
                        # video_details4.save()
                    
                    if Platform == 'GDN':    

                        video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(3),
                                                    campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                                                    ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                                                    questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                    if Platform == 'TikTok':    

                        video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(3),
                                                    campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                                                    ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                                                    questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()
                    
                    if Platform == 'Native':    

                        video_details4 = TbCampaignquestion(campaignquestionid=str(new_id)+str(3),
                                                    campaignvideoid=Campaignvideo.objects.get(campaignvideoid=new_id)
                                                    ,userroleid=TbUserrole.objects.get(userroleid='U1'),
                                                    questionid=TbQuestion.objects.get(questionid='1'))
                        video_details4.save()

                    dataQ = TbCampaignquestion.objects.filter(campaignvideoid=new_id)
                    listOfDataQ=[]
                    for i in dataQ:
                        output=i.questionid
                        listOfDataQ.append(output)
                    lenOfList=len(listOfDataQ)

                    listOfQuestion=[]
                    for i in listOfDataQ:
                        output=i.questiontext
                        listOfQuestion.append(output)
                    questionsText = {}
                    for i in range(0,lenOfList):
                        QT=listOfQuestion[i]
                        questionsText["q"+str(i)] = QT

                    listOfQuestionResponse=[]
                    for i in listOfDataQ:
                        output=i.questionresponse.split("|")
                        listOfQuestionResponse.append(output)

                    QuestionResponse = {}
                    for i in range(0,lenOfList):
                        lQR=listOfQuestionResponse[i]
                        QuestionResponse["k"+str(i)] = lQR
                    status='Uploaded'

                    return render(request,'tc_DigitalMarketing/upload-page.html',{"k":id,"video":url,"text":text,
                                                                                    'qT':questionsText,
                                                                                    'qR':QuestionResponse,
                                                                                    "data":data,'dataQ':dataQ,
                                                                                    'status':status,'Title':Title1,
                                                                                    'imgurl':image_url,'gifurl':Gif_url})
            
            CVID = cVideoId.objects.all().order_by('-id').first()
            CVID=str(CVID)

            video=TbVideo.objects.get(videoid = CVID)
            vP='/'+video.videopath
            vN=video.videoname
            pN=video.platform
            vP1='/'+video.videopath1
            img='/'+video.Imageurl
            gifurl=video.Gifurl
            Cre=video.creative

            user=TbUser.objects.get(userid=id)
            UN=user.username

            status = TbStatus(userid=TbUser.objects.get(userid=id),videoid=CVID,status='Pending',videoname=vN,approver='---',uploadername=UN,platform=pN,videoPath=vP,videoPath1=vP1,Imageurl=img,Gifurl=gifurl,creative=Cre)
            status.save()
  
            cQresponse=TbCampaignquestion.objects.filter(campaignvideoid=CVID)
            print(cQresponse)
            lenOfList=len(cQresponse)
            listOfcQresponse=[]
            for i in cQresponse:
                output=i.campaignquestionid
                listOfcQresponse.append(output)
            print(listOfcQresponse)
            import itertools

            for (a, b) in itertools.zip_longest(listOfcQresponse,Qlist):
                    video_details5 = Campaignquestionresponse(campaignquestionid=TbCampaignquestion.objects.get(campaignquestionid = a),
                                            userid=TbUser.objects.get(userid = str(id)),response= b)
                    video_details5.save()  
            
            videoDetails = video_Details(userid=TbUser.objects.get(userid=id),VideoPath=vP,VideoName=vN)
            videoDetails.save()
            
            if q0=='No':
                messages.success(request, 'Upload other Placements Creative')
                a=CVID
                return redirect('/dm/uploadagain/'+str(a)+str('/')+id)

            username=Profile.objects.get(userid = id)
            userroleid = username.userroleid
            print(userroleid)
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename
            print(userrolename)
            
            if userrolename=='Uploader':
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/uploaderdashboard/'+id)
            elif userrolename=='Reviewer':
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/approver/'+id)
            else:
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/superadmin/'+id)

        else:
            a=id
            status='Waiting'
            videodetails1=video_Details.objects.filter(userid=id)
            videodetails="video_Details.objects.filter(userid=id)"
            username=Profile.objects.get(userid = id)
            userroleid = username.userroleid
            print(userroleid)
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename
            print(userrolename)


            return render(request,'tc_DigitalMarketing/upload-page.html',{'k':a,'status':status,'videodetails':videodetails,'videodetails1':videodetails1,'userrolename':userrolename})
    
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

def update_view(request,id,id1):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/createrupload.html')
        else:
            status=TbStatus.objects.filter(videoid=id1)
            video=TbVideo.objects.get(videoid = id1)
            vP=video.videopath
            vT=video.videotranscription
            vN=video.videoname
            Platform=video.platform
            vP1=video.videopath1
            vP2=video.videopath2
            LOB=video.lob
            imgUrl=video.Imageurl
            gifUrl=video.Gifurl
            Creative=video.creative
            Vendor=video.vendor
            print(vP)
            print(vP1)
            print(Creative)
            userdetails=Profile.objects.get(userid = id)
            return render(request,'tc_DigitalMarketing/update.html',{
                                                                        'id':id,
                                                                        'url':vP,
                                                                        'vid':id1,
                                                                        'Transcribe':vT,
                                                                        'vname':vN,
                                                                        'url1':vP1,'url2':vP2,
                                                                        'Vendor':Vendor,
                                                                        'LOB':LOB,
                                                                        'Creative':Creative,
                                                                        'Platform':Platform,
                                                                        'imgUrl':imgUrl,
                                                                        "gifUrl":gifUrl, 
                                                                        'userdetails':userdetails,                                                                    
                                                                     })
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
     

def detailed_view(request,id):
    try:
     
        status=TbStatus.objects.filter(userid=id).order_by('-createddate').values()
        return render(request,'tc_DigitalMarketing/filterpage.html',{'status':status,'id':id})
    
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

def approverdetail_view(request,id):
    try:
        user_status=TbStatus.objects.all().order_by('-createddate').values()
        return render(request,'tc_DigitalMarketing/filterpage.html',{'user_status':user_status,'id':id})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
    
@login_required(login_url='/')
def superadmindetail_view(request,id):
    try:
        if request.method == "POST":
            getvalue=TbStatus.objects.filter(status='Approved')
            listofvideoid=[]
            for value in getvalue:
                print("selectoption"+value.videoid)
                a=request.POST.get('selectoption'+value.videoid)
                listofvideoid.append(a)
            print(listofvideoid)
            listofvideoid=list(filter(None,listofvideoid))
            print(listofvideoid)

            listofdownloader=[]
            user=TbUser.objects.filter(userroleid='D1')
            for value in user:
                b=request.POST.get('downloader'+str(value.userid))
                listofdownloader.append(b)
            print(listofdownloader)
            listofdownloader=list(filter(None,listofdownloader))
            print(listofdownloader)

            for i in listofvideoid:
                print(i)
                approver = TbApprove.objects.get(videoid=i)
                approver.downloadaccess='download'
                approver.downloader=listofdownloader
                approver.save()
                
                status= TbStatus.objects.get(videoid=i)
                status.downloadaccess='download'
                status.downloader=listofdownloader
                status.save()
            user_status=TbStatus.objects.filter(status='Approved').order_by('-createddate').values()
            # return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,})
            messages.success(request, 'Access given succesfully')
            return redirect('/dm/superadmindetail_view/'+id)
        else:
            user=TbUser.objects.filter(userroleid='D1')
            user_status=TbStatus.objects.filter(status='Approved').order_by('-createddate').values()
            accessed_video='yes'
            return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,'user':user,'accessed_video':accessed_video})
            # return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,'user':user,'accessed_video':accessed_video})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

@login_required(login_url='/')
def superadmindetail_downloader_view(request,id):
    try:
        uid=id
        if request.method == "POST":
            getvalue=TbStatus.objects.filter(status='Approved')
            listofvideoid=[]
            for value in getvalue:
                print("selectoption"+value.videoid)
                a=request.POST.get('selectoption'+value.videoid)
                listofvideoid.append(a)
            print(listofvideoid)
            listofvideoid=list(filter(None,listofvideoid))
            print(listofvideoid)

            listofdownloader=[]
            user=TbUser.objects.filter(userroleid='D1')
            for value in user:
                b=request.POST.get('downloader'+str(value.userid))
                print(b)
                listofdownloader.append(b)
            print(listofdownloader)
            listofdownloader=list(filter(None,listofdownloader))
            print(listofdownloader)

            for i in listofvideoid:
                print(i)
                approver = TbApprove.objects.get(videoid=i)
                approver.downloadaccess='download'
                approver.downloader=listofdownloader
                approver.save()
                
                status= TbStatus.objects.get(videoid=i)
                status.downloadaccess='download'
                status.downloader=listofdownloader
                status.save()
            user_status=TbStatus.objects.filter(status='Approved',downloadaccess='download').order_by('-createddate').values()
            # return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,})
            messages.success(request, 'Access given succesfully')
            return redirect('/dm/superadmindetail_downloader_view/'+id)
        else:
            user=TbUser.objects.filter(userroleid='D1')
            user_status=TbStatus.objects.filter(status='Approved',downloadaccess='download').order_by('-createddate').values()
            return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,'user':user})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)     

def remove_common(a, b):
 
    for i in a[:]:
        if i in b:
            # a.remove(i)
            b.remove(i)

def remove_common1(a1, b1):
        for i in a1[:]:
            if i in b1:
                # a1.remove(i)
                b1.remove(i)

def daccess(request,id):

        if request.method == "POST":
            rest = request.POST.getlist('reset')
            save = request.POST.getlist('save')
            down_list = request.POST.getlist('top[]')
            downaccess_list = request.POST.getlist('topics[]')
            print(save)
            print(rest)
            print('downaccess_list',downaccess_list)
            print('downloader_list',down_list)

            # id="3c2271e1-d10f-4680-b86c-8b62f41b7594"
            downloader=[]
            downloaders=TbUser.objects.filter(userroleid='D1')
            for i in downloaders:
                downloader.append(i.username)
            downloaderstatus= TbStatus.objects.get(videoid=id)

            if downloaderstatus.downloader ==None or downloaderstatus.downloader ==[]:
                downloaderstatus.downloader=downloader
                downloaderstatus.save() 

            if downloaderstatus.downloader !=None or downloaderstatus.downloader ==[]:
                downloader=(downloaderstatus.downloader)
                downloader_list = ast.literal_eval(downloader)
                # print(downloader_list)
            else:
                downloader_list=[]

            if downloaderstatus.downloadaccesslist !=None or downloaderstatus.downloader ==[]: 
                downloaderaccess=(downloaderstatus.downloadaccesslist)
                downloaderaccess_list = ast.literal_eval(downloaderaccess)
                # print(downloaderaccess_list)
            else:
                downloaderaccess_list=[]

            a=downaccess_list
            b=downloader_list
            remove_common(a, b)
            # print(a)
            # print(b)
            approver = TbApprove.objects.get(videoid=id)
            approver.downloadaccess='download'
            approver.downloader=b
            approver.save()


            if str(down_list) == '[]':
                downloaderstatus.downloader=b
                downloaderstatus.downloadaccesslist=a+downloaderaccess_list
                downloaderstatus.downloadaccess='download'
                downloaderstatus.save() 

                approver = TbApprove.objects.get(videoid=id)
                approver.downloadaccess='download'
                approver.downloader=a+downloaderaccess_list
                approver.save()




            #TILL THIS WORKING FINE


            if str(downaccess_list) =='[]':
                a1=down_list+downloader_list
                b1=downloaderaccess_list
                remove_common1(a1, b1)
                print(a1)
                print(b1)

                downloaderstatus.downloader=down_list+downloader_list
                downloaderstatus.downloadaccesslist=b1
                downloaderstatus.save() 

                approver = TbApprove.objects.get(videoid=id)
                approver.downloadaccess='download'
                approver.downloader=b1
                approver.save()

            return redirect ('/dm/daccess/'+id)


        else:

            downloader=[]
            downloaders=TbUser.objects.filter(userroleid='D1')
            for i in downloaders:
                downloader.append(i.username)
            downloaderstatus= TbStatus.objects.get(videoid=id)

            if downloaderstatus.downloader == None:
                downloaderstatus.downloader=downloader
                downloaderstatus.save() 
                return redirect ('/dm/daccess/'+id)

            if downloaderstatus.downloader != None or str(downloaderstatus.downloader) =='[]':
                downloader=(downloaderstatus.downloader)
                downloader_list = ast.literal_eval(downloader)
                print(downloader_list)
            else:
                downloader_list=[]

            if downloaderstatus.downloadaccesslist != None or str(downloaderstatus.downloader) == '[]': 
                downloaderaccess=(downloaderstatus.downloadaccesslist)
                downloaderaccess_list = ast.literal_eval(downloaderaccess)
                print(downloaderaccess_list)
            else:
                downloaderaccess_list=[]

            return render (request,'tc_DigitalMarketing/daccess.html',{"a_list":downloader_list,"b_list":downloaderaccess_list })


