from django.shortcuts import render,redirect,HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import *
from .models import TbVideo,Campaignvideo,TbCampaignquestion,Campaignquestionresponse,TbQuestion,TbUserrole,cVideoId,TbStatus,TbUser,TbApprove,video_Details,TbapproverQuestion,Profile
import pandas as pd
import json

# 
import whisper

import uuid
from django.contrib import messages
from django.db import connection
import os
from datetime import datetime

#login
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.decorators import login_required



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
        recent=TbStatus.objects.filter(userid=id,status="Rejected").order_by('-createddate').values()[:3]
        q = status.values()
        df = pd.DataFrame.from_records(q)
        if len(df) == 0:
            val=id
            return redirect('/dm/createrupload/'+str(val))
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
        print(df['createddate'])
        df['createddate']=df['createddate'].str.slice(0, -10)
        video_count = df.groupby('createddate')['videoname'].count().reset_index()
        DateValue=video_count['createddate'].values.tolist()
        videoC=video_count['videoname'].values.tolist()

        print(DateValue)

        file_type_counts = df['creative'].value_counts().reset_index()
        file_type_counts.columns = ['File_Type', 'Count']
        File_Type=file_type_counts['File_Type'].values.tolist()
        File_TypeC=file_type_counts['Count'].values.tolist()
        return render(request,'tc_DigitalMarketing/dash_index.html',{'id':id,'status':status,'Approved':Approved,'Rejected':Rejected,'Pending':Pending,'UserName':UN,
                                                                     'DateValue':DateValue,"videoC":videoC,'upload_img_gif_count':upload_img_gif_count,'File_Type':File_Type,
                                                                     'File_TypeC':File_TypeC,'recent':recent,
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
        return render(request,'tc_DigitalMarketing/filterpage.html',{'id':id,'status':status,'user_status':user_status})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
@login_required(login_url='/')
def myvideos(request,id):
    try:
        if request.method == "POST":
             return render(request,'tc_DigitalMarketing/myvideos.html',{'id':id})
        videodetails=video_Details.objects.filter(userid=id)
        return render(request,'tc_DigitalMarketing/myvideos.html',{'id':id,'videodetails':videodetails})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
@login_required(login_url='/')
def creater_upload(request,id):
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
                    filename = fs.save(myfile.name, myfile)
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
                    new_id = uuid.uuid4()
                    str(new_id)
                    print(str(new_id))

                    video_id = cVideoId(VideoID=new_id)
                    video_id.save()

                    T=Title1
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

                    username=Profile.objects.get(userid = id)
                    userroleid = username.userroleid
                    print(userroleid)
                    userrolename=TbUserrole.objects.get(userroleid = userroleid)
                    userrolename=userrolename.userrolename
                    print(userrolename)


                    return render(request,'tc_DigitalMarketing/upload-page.html',{"k":id,"video":url,"text":text,
                                                                                    'qT':questionsText,
                                                                                    'qR':QuestionResponse,
                                                                                    "data":data,'dataQ':dataQ,
                                                                                    'status':status,'Title':Title1,
                                                                                    'imgurl':image_url,'gifurl':Gif_url,
                                                                                    'userrolename':userrolename,
                                                                                    })
            

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
            userrolename=TbUserrole.objects.get(userroleid = userroleid)
            userrolename=userrolename.userrolename 

            if userrolename=='Uploader':
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/uploaderdashboard/'+id)
            else:
                messages.success(request, 'submitted succesfully')
                return redirect('/dm/approver/'+id)
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


            return render(request,'tc_DigitalMarketing/upload-page.html',{'k':a,'status':status,
                                                                          'videodetails':videodetails,
                                                                          'videodetails1':videodetails1,
                                                                          'userrolename':userrolename})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
    
def transcribe_video_audio(video_path):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = BASE_DIR+video_path
    model = whisper.load_model("tiny")
    audio_dir = os.path.dirname(file_path)
    print(audio_dir)
    audio_path = os.path.join(audio_dir, "audio.wav")
    command = f'ffmpeg -i "{file_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}"'
    os.system(command)
    result = model.transcribe(audio_path)
    os.remove(audio_path)
    return result["text"]

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # # file_path = BASE_DIR+video_path
    # file_path="app\media\ACA_4_dSkaCEo.mp4"
    # print(file_path)
    # model = whisper.load_model("tiny")
    # result = model.transcribe(file_path)
    # return result["text"]


def unique_numbers(numbers):
    # this will take only unique numbers from the tuple
    return tuple(set(numbers))

# THIS is no needed Rechecking is pending
def user_indexpage(request):
    try:
        if request.method == 'POST':
            userName = request.POST.get('username')
            Password = request.POST.get('pass')
            data = TbUser.objects.filter(username=userName,password=Password).values()
            for i in data:
                print(i)
                a=i
            if data:
                value=a.get('userroleid_id')
                print(value)
                if value == "U1":
                    val=a.get('userid')
                    
                    return redirect('/dm/uploaderdashboard/'+str(val)) 
                if value == "R1":
                    val=a.get('userid')
                    
                    return redirect('/dm/approver/'+str(val))
                
                if value == "S1":
                    val=a.get('userid')
                    
                    return redirect('/dm/approver/'+str(val))
            messages.error(request, 'Invalid! userName or password')
            return redirect('/dm/UserIndexpage')    
        else:
            return render(request, 'tc_DigitalMarketing/UserindexPage.html')
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

@login_required(login_url='/')
def approver(request,id):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/createrupload.html')
        else:
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
                df['createddate']=df['createddate'].str.slice(0, -22)
                video_count = df.groupby('createddate')['videoname'].count().reset_index()
                DateValue=video_count['createddate'].values.tolist()
                videoC=video_count['videoname'].values.tolist()
                print(videoC)

                file_type_counts = df['creative'].value_counts().reset_index()
                file_type_counts.columns = ['File_Type', 'Count']
                File_Type=file_type_counts['File_Type'].values.tolist()
                File_TypeC=file_type_counts['Count'].values.tolist()
                return render(request,'tc_DigitalMarketing/approver_index.html',{'status':status,'id':id,'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                            'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                            'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent})
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
            print(upload_img_gif_count)


            df['createddate']=df['createddate'].astype(str)
            df['createddate']=df['createddate'].str.slice(0, -22)
            video_count = df.groupby('createddate')['videoname'].count().reset_index()
            DateValue=video_count['createddate'].values.tolist()
            videoC=video_count['videoname'].values.tolist()
            print(videoC)

            file_type_counts = df['creative'].value_counts().reset_index()
            file_type_counts.columns = ['File_Type', 'Count']
            File_Type=file_type_counts['File_Type'].values.tolist()
            File_TypeC=file_type_counts['Count'].values.tolist()
            print(File_Type)
            print(File_TypeC)

            # return render(request,'tc_DigitalMarketing/approver.html',{'status':status,'id':id})
            return render(request,'tc_DigitalMarketing/approver_index.html',{'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                            'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                            'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent,
                                                                            'upload_img_gif_count':upload_img_gif_count})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


@login_required(login_url='/')
def admin(request,id):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/admin_index.html')
        else:
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
                df['createddate']=df['createddate'].str.slice(0, -22)
                video_count = df.groupby('createddate')['videoname'].count().reset_index()
                DateValue=video_count['createddate'].values.tolist()
                videoC=video_count['videoname'].values.tolist()

                file_type_counts = df['creative'].value_counts().reset_index()
                file_type_counts.columns = ['File_Type', 'Count']
                File_Type=file_type_counts['File_Type'].values.tolist()
                File_TypeC=file_type_counts['Count'].values.tolist()
                return render(request,'tc_DigitalMarketing/admin_index.html',{'status':status,'id':id,'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                            'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                            'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent})
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
            df['createddate']=df['createddate'].str.slice(0, -22)
            video_count = df.groupby('createddate')['videoname'].count().reset_index()
            DateValue=video_count['createddate'].values.tolist()
            videoC=video_count['videoname'].values.tolist()

            file_type_counts = df['creative'].value_counts().reset_index()
            file_type_counts.columns = ['File_Type', 'Count']
            File_Type=file_type_counts['File_Type'].values.tolist()
            File_TypeC=file_type_counts['Count'].values.tolist()

            # return render(request,'tc_DigitalMarketing/approver.html',{'status':status,'id':id})
            return render(request,'tc_DigitalMarketing/admin_index.html',{'status':status,'id':id,'Approved':Approved,'Rejected':Rejected,
                                                                            'Pending':Pending,'UserName':UN,'DateValue':DateValue,"videoC":videoC,
                                                                            'File_Type':File_Type,'File_TypeC':File_TypeC,'recent':recent})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


@login_required(login_url='/')
def approver_view(request,id,uid):
    try:
        if request.method == "POST":
                q0 = request.POST.get('q0')
                q1 = request.POST.get('q1')
                q2 = request.POST.get('q2')
                q3 = request.POST.get('q3')
                q4 = request.POST.get('q4')
                q5 = request.POST.get('q5')
                q6 = request.POST.get('q6')
                Qlist=[q0,q1,q2,q3,q4,q5,q6]
                tb = request.POST.get('ReasonTextbox')
                transcription = request.POST.get('cmdtranscript')
                transcription1 = request.POST.get('cmdtranscript1')
                print(transcription1)
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
                    vP='/'+video.videopath
                    vN=video.videoname
                    vP1='/'+video.videopath1
                    pN=video.platform

                    user=TbUser.objects.get(userid=uid)
                    getApproverName=user.username
                    print(getApproverName)
                    
                    userName=connection.cursor()
                    userName.execute("select UserName from tb_User where UserID='{val}'".format(val=uid))
                    userName=userName.fetchall()
                    UN=userName[0][0]
                    
                    approve = TbApprove(userid=TbUser.objects.get(userid=uid),
                                        videoid=id,videotitle=vN,videopath=vP,uploadername=UN)
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
                    if transcription1 != None:
                        videodetails.videotranscription1=transcription1
                    videodetails.save()


                    Campaignquestionresponse.objects.filter(campaignquestionid=id).delete()
                    TbCampaignquestion.objects.filter(campaignquestionid=id).delete()

                    messages.success(request, 'Approved succesfully')
                    return redirect('/dm/approver/'+str(uid))

                    # deleteQuestionsres=connection.cursor()
                    # deleteQuestionsres.execute("DELETE campaignquestionresponse FROM campaignquestionresponse INNER JOIN tb_campaignquestion ON campaignquestionresponse.campaignquestionid = tb_campaignquestion.campaignquestionid WHERE tb_campaignquestion.campaignvideoid='{value}';".format(value=id))
                    # cqr.delete()
                    # cq.delete()


                else:
                    # NO NEED THIS CODE /25/6/23
                    # deletestatus=connection.cursor()
                    # deletestatus.execute("DELETE FROM tb_Status WHERE videoID='{value}';".format(value=id))
                    
                    video=TbVideo.objects.get(videoid =id)
                    vP='/'+video.videopath
                    vN=video.videoname
                    vP1='/'+video.videopath1
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
                    video.approver=getApproverName[0][0]
                    video.MainReason=tb
                    video.save()

                    videodetails=TbVideo.objects.get(videoid=id)
                    if transcription != None:
                        videodetails.videotranscription=transcription
                    if transcription1 != None:
                        videodetails.videotranscription1=transcription1
                    videodetails.save()



                    # ____new Delete lines added here__
                    # deleteQuestionsres=connection.cursor()
                    # deleteQuestionsres.execute("DELETE CampaignQuestionResponse FROM CampaignQuestionResponse inner join tb_CampaignQuestion on CampaignQuestionResponse.CampaignQuestionID = tb_CampaignQuestion.CampaignQuestionID WHERE tb_CampaignQuestion.CampaignVideoID='{value}';".format(value=id))
                    Campaignquestionresponse.objects.filter(campaignquestionid=id).delete()
                    TbCampaignquestion.objects.filter(campaignquestionid=id).delete()
                    
                    
                    messages.error(request, 'rejected succesfully')
                    return redirect('/dm/approver/'+str(uid))
            # return render(request,'tc_DigitalMarketing/approverview.html',{})
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
            vP='/'+video.videopath
            vT=video.videotranscription
            vN=video.videoname
            Platform=video.platform
            vP1='/'+video.videopath1
            vT1=video.videotranscription1
            LOB='/'+video.lob
            imgUrl=video.Imageurl
            gifUrl=video.Gifurl
            Creative=video.creative
            Vendor=video.vendor

            print(gifUrl)
            print(imgUrl)
            print(Creative)
            print(vP)
            print(vP1)
            return render(request,'tc_DigitalMarketing/approverviewnew.html',{'qT':questionsText,
                                                                              'qR':QuestionResponse,
                                                                              'uploaderName':uploaderName,
                                                                              'R':result,
                                                                              'video':vP,
                                                                              'Transcribe':vT,
                                                                              'vname':vN,
                                                                              'id':uid,
                                                                              'video1':vP1,
                                                                              'Transcribe1':vT1,
                                                                              'Vendor':Vendor,
                                                                              'LOB':LOB,
                                                                              'Creative':Creative,
                                                                              'Platform':Platform,
                                                                              'Questions':Question,
                                                                              'imgUrl':imgUrl,
                                                                              'gifUrl':gifUrl})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  



@login_required(login_url='/')
def status_view(request,id1):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/createrupload.html')
        else:
            # status=Status.objects.filter(userid=id)
            print(id1)
            status=connection.cursor()
            status.execute("select reason,UploaderName FROM tb_Status WHERE VideoID='{value1}';".format(value1=id1))
            response=status.fetchall()

            # cursor1=connection.cursor()
            # cursor1.execute("select VideoPath,VideoName from CampaignVideo cv inner join tb_Video v on v.VideoID=cv.VideoID AND cv.CampaignVideoID='{val}'".format(val=id1))
            # VideoDeatails=cursor1.fetchall()
            # vP='/'+VideoDeatails[0][0]
            # vName=VideoDeatails[0][1]

            video=TbVideo.objects.get(videoid = id1)
            vP='/'+video.videopath
            vT=video.videotranscription
            vN=video.videoname
            Platform=video.platform
            vP1='/'+video.videopath1
            vT1=video.videotranscription1
            LOB='/'+video.lob
            imgUrl=video.Imageurl
            gifUrl=video.Gifurl
            Creative=video.creative
            Vendor=video.vendor

            import ast
            res = ast.literal_eval(response[0][0])

            print(res)
            return render(request,'tc_DigitalMarketing/statusview.html',{'approverres':res[0],
                                                                        'approvercmd':res[1],
                                                                        'reason':res[2],
                                                                        'id':id,
                                                                        'video':vP,
                                                                        'vid':id1,
                                                                        'Transcribe':vT,
                                                                        'vname':vN,
                                                                        'video1':vP1,
                                                                        'Transcribe1':vT1,
                                                                        'Vendor':Vendor,
                                                                        'LOB':LOB,
                                                                        'Creative':Creative,
                                                                        'Platform':Platform,
                                                                        'uploadername':response[0][1],
                                                                        'imgUrl':imgUrl,
                                                                        "gifUrl":gifUrl
                                                                        })
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
        cursor1=connection.cursor()
        cursor1.execute("select VideoPath,VideoTranscription,VideoName from CampaignVideo cv inner join tb_Video v on v.VideoID=cv.VideoID AND cv.CampaignVideoID='{val}'".format(val=id))
        VideoDeatails=cursor1.fetchall()
        vP='/'+VideoDeatails[0][0]
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

# def upload_again(request,id,id1):
#     if request.method == "POST":
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         print(uploaded_file_url)
#         url=uploaded_file_url
#         url1=url[1:]

#         text='--'

#         record = TbVideo.objects.get(videoid=id)
#         record.videopath1 = uploaded_file_url
#         record.videotranscription1 = text
#         record.save()
#         videoDetails = video_Details(userid=TbUser.objects.get(userid=id1),VideoPath=uploaded_file_url)
#         videoDetails.save()
#         messages.success(request, 'submitted succesfully')
#         return render(request,'tc_DigitalMarketing/uploadagain.html',{"video":url,'text':text,'id':id1})
#     else:
#         status='Waiting'
#         videodetails=video_Details.objects.filter(userid=id1)
#         return render(request,'tc_DigitalMarketing/uploadagainnew.html',{'videodetails':videodetails,'status':status})
    

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
                filename = fs.save(myfile.name, myfile)
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
                    # text=transcribe_video_audio(url)
                    text=' Are you an American over 25 and earning less than $50,000? Well you might have already qualified for this $5,200 healthcare assistance program available in the US. Just CLICK the link below and see how much you might get back.'
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
            return redirect('/dm/uploaderdashboard/'+id1)

        
        else:
            status='Waiting'
            videodetails=video_Details.objects.filter(userid=id1)
            return render(request,'tc_DigitalMarketing/uploadagainnew.html',{'videodetails':videodetails,'status':status,'id':id1,})
        
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  
    

def login_view(request):
    try:
        next = request.GET.get('next')
        print(next)
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
            #customized redirect i need to check this
            #     return redirect(next)
                if user.profile.userroleid == "U1":
                        
                        return redirect('/dm/uploaderdashboard/'+str(user.profile.userid)) 
                if user.profile.userroleid == "R1":

                        return redirect('/dm/approver/'+str(user.profile.userid))   
                        
                if user.profile.userroleid == "S1":

                        return redirect('/dm/superadmin/'+str(user.profile.userid))  
                
                if user.profile.userroleid == "D1": 
                
                        return redirect('/dm/superadmin/'+str(user.profile.userid)) 
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
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            if next:
                return redirect(next)
            return redirect('/')

        context = {
            'form': form,
        }
        return render(request, "tc_DigitalMarketing/signup.html", context)
    
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  


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
                    filename = fs.save(myfile.name, myfile)
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
            
            messages.success(request, 'submitted succesfully')
            return redirect('/dm/uploaderdashboard/'+id)
        else:
            a=id
            status='Waiting'
            videodetails1=video_Details.objects.filter(userid=id)
            videodetails="video_Details.objects.filter(userid=id)"

            return render(request,'tc_DigitalMarketing/upload-page.html',{'k':a,'status':status,'videodetails':videodetails,'videodetails1':videodetails1})
    
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

def update_view(request,id,id1):
    try:
        if request.method == "POST":
            return render(request,'tc_DigitalMarketing/createrupload.html')
        else:
            status=TbStatus.objects.filter(videoid=id1)

            cursor1=connection.cursor()
            cursor1.execute("select VideoPath,VideoName from CampaignVideo cv inner join tb_Video v on v.VideoID=cv.VideoID AND cv.CampaignVideoID='{val}'".format(val=id1))
            VideoDeatails=cursor1.fetchall()
            vP='/'+VideoDeatails[0][0]
            vName=VideoDeatails[0][1]


            return render(request,'tc_DigitalMarketing/update.html',{'id':id,'video':vP,'vname':vName,'vid':id1,'status':status})
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
            user_status=TbStatus.objects.filter(status='Approved',downloadaccess='Notyet').order_by('-createddate').values()
            # return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,})
            messages.success(request, 'Access given succesfully')
            return redirect('/dm/superadmindetail_view/'+id)
        else:
            user=TbUser.objects.filter(userroleid='D1')
            user_status=TbStatus.objects.filter(status='Approved',downloadaccess='Notyet').order_by('-createddate').values()
            accessed_video='yes'
            return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,'user':user,'accessed_video':accessed_video})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

@login_required(login_url='/')
def superadmindetail_downloader_view(request,id):
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
            user_status=TbStatus.objects.filter(status='Approved',downloadaccess='download').order_by('-createddate').values()
            # return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,})
            messages.success(request, 'Access given succesfully')
            return redirect('/dm/superadmindetail_downloader_view/'+id)
        else:
            user=TbUser.objects.filter(userroleid='D1')
            user_status=TbStatus.objects.filter(status='Approved',downloadaccess='download').order_by('-createddate').values()
            return render(request,'tc_DigitalMarketing/downloadaccesspage.html',{'user_status':user_status,'id':id,'user':user,})
    except Exception as e:
        error={'error':e}
        return render(request,'tc_DigitalMarketing/error.html',context=error)  

from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)     

