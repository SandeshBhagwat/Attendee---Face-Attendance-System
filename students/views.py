from email import message
import email
from urllib import request
from cv2 import WINDOW_AUTOSIZE, namedWindow
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
import cv2,os
from pathlib import Path
from Attendance.settings import BASE_DIR
import os
from PIL import Image
import numpy as np
from Attendance.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from students.models import classAttendance,studAttendance
import datetime
from datetime import timedelta


def login(request):    
  
    if request.method == "POST":
        username= request.POST['username'] 
        password = request.POST['password']

        if username=='faculty':   
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request,'Faculty member logged in successfully!')
                return redirect("teachers/dashboard/")
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('/')
        else:
            try:
                user=auth.authenticate(username=User.objects.get(email=username), password=password)
                messages.success(request,'Student logged in successfully!')
            except:
                user=auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request,'Student logged in successfully!')
                    return redirect("students/dashboard/")
                else:
                    messages.error(request, 'Invalid credentials')
                    return redirect('/')
    else:
        return render(request,'login.html')


def register(request):
    
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        conf_pass = request.POST['conf_pass']
        email = request.POST['email']
                   
                  
        if password==conf_pass:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username is already taken!')            
                return redirect('/register')

            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email ID already registered!')
                return redirect('/register')
                  
            else: 
                user = User.objects.create_user(username=username, password=conf_pass, email=email,first_name=first_name, last_name=last_name)
                user.save();
                messages.success(request,'Registeration completed successfully!')
                return redirect('/')

        else:
            messages.error(request,'Password and confirm password does not match!')
            return redirect('/register')

    else:
        return render(request,'register.html')
    
    

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def feedback(request):
    return render(request,'feedback.html')

def contactus(request):
    return render(request,'contactus.html')


@login_required(login_url="/")
def students(request):
    return render(request,'studentDashboard.html')

@login_required(login_url="/")
def capture(request):
    return render(request,'capture.html')

@login_required(login_url="/")
def teachers(request):

    user=User.objects.filter(is_staff=False)
    # return render(request, 'teacherDashboard.html')
    print("this is user", user)
    return render(request,'teacherDashboard.html', {'user':user})

def logout(request):
        auth.logout(request)
        return redirect("/")


@login_required
def create_dataset(request):
    if request.method=="POST":
        #print request.POST
        user = request.user
        print('this is user id')
        print (user.id)
        # print cv2.__version__
        # Detect face
        #Creating a cascade image classifier
        faceDetect = cv2.CascadeClassifier('ml/haarcascade_frontalface_default.xml')
        #camture images from the webcam and process and detect the face
        # takes video capture id, for webcam most of the time its 0.
        cam = cv2.VideoCapture(0)

        # Our identifier
        # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
        id = user.id
        # Our dataset naming counter
        sampleNum = 0
        # Capturing the faces one by one and detect the faces and showing it on the window
        while(True):
            # Capturing the image
            #cam.read will return the status variable and the captured colored image
            ret, img = cam.read()
            #the returned img is a colored image but for the classifier to work we need a greyscale image
            #to convert
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #To store the faces
            #This will detect all the images in the current frame, and it will return the coordinates of the faces
            #Takes in image and some other parameter for accurate result
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            #In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
            for(x,y,w,h) in faces:
                # Whenever the program captures the face, we will write that is a folder
                # Before capturing the face, we need to tell the script whose face it is
                # For that we will need an identifier, here we call it id
                # So now we captured a face, we need to write it in a file
                sampleNum = sampleNum+1
                # Saving the image dataset, but only the face part, cropping the rest
                # cv2.imwrite(BASE_DIR+'/ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])
                cv2.imwrite('ml/dataset/user.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[y:y+h,x:x+w])#######

                # @params the initial point of the rectangle will be x,y and
                # @params end point will be x+width and y+height
                # @params along with color of the rectangle
                # @params thickness of the rectangle
                cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
                # Before continuing to the next loop, I want to give it a little pause
                # waitKey of 100 millisecond
                cv2.waitKey(250)

            #Showing the image in another window
            #Creates a window with window name "Face" and with the image img
            cv2.imshow("Face Cropper",img)
            #Before closing it we need to give a wait command, otherwise the open cv wont work
            # @params with the millisecond of delay 1
            cv2.waitKey(1)
            #To get out of the loop
            if(sampleNum>50):
                break
        #releasing the cam
        cam.release()
        # destroying all the windows
        cv2.destroyAllWindows()
        trainer()
        return redirect('/students/capture/')
        
    
    return render(request, 'capture.html')



def trainer():
    #  Creating a recognizer to train
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            #Path of the samples
            path = 'ml/dataset'
   
            def getImagesWithID(path):
               
                imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
                imagePaths.pop(0) #concatinate the path with the image name
                #print imagePaths
               
                # Now, we loop all the images and store that userid and the face with different image list
                faces = []
                Ids = []
                for imagePath in imagePaths:
                    # First we have to open the image then we have to convert it into numpy array
                    faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
                    # converting the PIL image to numpy array
                
                    # @params takes image and convertion format
                    faceNp = np.array(faceImg, 'uint8')
                    # Now we need to get the user id, which we can get from the name of the picture
                    # for this we have to slit the path() i.e dataset/user.1.7.jpg with path splitter and then get the second part only i.e. user.1.7.jpg
                    # Then we split the second part with . splitter
                    # Initially in string format so hance have to convert into int format
                    ID = int(os.path.split(imagePath)[-1].split('.')[1]) # -1 so that it will count from backwards and slipt the second index of the '.' Hence id
                    # Images
                    faces.append(faceNp)
                    # Label
                    Ids.append(ID)
                    #print ID
                    # cv2.imshow("training", faceNp)
                    cv2.waitKey(10)
                return np.array(Ids), np.array(faces)

            # Fetching ids and faces
            ids, faces = getImagesWithID(path)

            #Training the recognizer
            # For that we need face samples and corresponding labels
            recognizer.train(faces, ids)

            # Save the recogzier state so that we can access it later
            recognizer.save('ml/recognizer/trainingData.yml')
            cv2.destroyAllWindows()
            
           


@login_required
def recognize(request):
            # recognizer = cv2.face.LBPHFaceRecognizer_create()
            # #Path of the samples
            # path = 'ml/dataset'
   
            # def getImagesWithID(path):
               
            #     imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
            #     imagePaths.pop(0) #concatinate the path with the image name
            #     #print imagePaths
               
            #     # Now, we loop all the images and store that userid and the face with different image list
            #     faces = []
            #     Ids = []
            #     for imagePath in imagePaths:
            #         # First we have to open the image then we have to convert it into numpy array
            #         faceImg = Image.open(imagePath).convert('L') #convert it to grayscale
            #         # converting the PIL image to numpy array
                
            #         # @params takes image and convertion format
            #         faceNp = np.array(faceImg, 'uint8')
            #         # Now we need to get the user id, which we can get from the name of the picture
            #         # for this we have to slit the path() i.e dataset/user.1.7.jpg with path splitter and then get the second part only i.e. user.1.7.jpg
            #         # Then we split the second part with . splitter
            #         # Initially in string format so hance have to convert into int format
            #         ID = int(os.path.split(imagePath)[-1].split('.')[1])
            #         print("this is id from trainerr",ID)
            #          # -1 so that it will count from backwards and slipt the second index of the '.' Hence id
            #         # Images
            #         faces.append(faceNp)
            #         # Label
            #         Ids.append(ID)
            #         #print ID
            #         # cv2.imshow("training", faceNp)
            #         cv2.waitKey(10)
            #     return np.array(Ids), np.array(faces)

            # # Fetching ids and faces
            # ids, faces = getImagesWithID(path)
            # # print("this are ids",ids)
            # # print("this are faces",faces)

            # #Training the recognizer
            # # For that we need face samples and corresponding labels
            # recognizer.train(faces, ids)

            # # Save the recogzier state so that we can access it later
            # recognizer.save('ml/recognizer/trainingData.yml')
            # cv2.destroyAllWindows()

            faceDetect = cv2.CascadeClassifier('ml/haarcascade_frontalface_default.xml')
        
            cam = cv2.VideoCapture(0)
            # creating recognizer
            rec = cv2.face.LBPHFaceRecognizer_create();
            # loading the training data
            rec.read('ml/recognizer/trainingData.yml')
            getId = 0
            font = cv2.FONT_HERSHEY_SIMPLEX
            userId = 0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                for(x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)

                    getId,conf = rec.predict(gray[y:y+h, x:x+w]) #This will predict the id of the face
                    print("this is get id",getId)

                    print (conf)
                    userId = (request.user).id
                    print("this is user id",userId)  
                    if(getId==userId):
                        if conf>20:
                            print("no1")
                            cv2.putText(img, (request.user).first_name + (request.user).last_name,(x,y+h), font, 1, (0,255,0),2)
                            print((request.user).first_name)
                            class_id=classAttendance.objects.latest('id').id
                            currentStudent=studAttendance.objects.filter(class_id=class_id).filter(student_id=userId)
                            print("This is current student",currentStudent)
                            currentStudent.update(status=True)
                            
                            # else:
                            #     cv2.putText(img, "Unknown",(x,y+h), font, 1, (0,0,255),2)
                        else:
                            print("no11")
                            cv2.putText(img, "Unknown",(x,y+h), font, 1, (0,0,255),2)

                            
                    else:
                        print("no2")
                        cv2.putText(img, "Unknown",(x,y+h), font, 1, (0,0,255),2)

                        # Printing that number below the face
                        # @Prams cam image, id, location,font style, color, stroke
                    
                    cv2.imshow("Face",img)
                    if(cv2.waitKey(1) == ord('q')):
                        print("no3")
                        break
                    # elif(userId != 0):
                    #     print("no4")
                    #     cv2.waitKey(1000)
                    #     cam.release()
                    #     cv2.destroyAllWindows()
                    #     return render(request,'students.html')
                if(cv2.waitKey(1) == ord('q')):
                        print("no3")
                        break

            cam.release()
            print("cam release")
            cv2.destroyAllWindows()
            return redirect('/students/giveattendance/')  


@login_required
def takeAttendance(request):
    if request.method=="POST":
        print("inside")
        class_Date=request.POST['class_date']
        start_time=request.POST['start_time']
        end_time=request.POST['end_time']
        subject=request.POST['subject']

        create_date=datetime.datetime.now()
        print(create_date)
        n=5
        close_date = create_date + timedelta(minutes=n)
        print(close_date)

        
        classAttendance.objects.create(start_Time=start_time,end_Time=end_time,date=class_Date,subject_name=subject,create_time=create_date
        ,close_time=close_date).save();

        class_id=(classAttendance.objects.latest('id')).id



        queryset=User.objects.filter(is_staff=False).values('id')
        print(queryset)
        # # print("------ ",User.objects.get(id))
        

        for u in queryset:

            student_id=u['id']
            print(student_id)
            studAttendance.objects.create(student_id=student_id,class_id=class_id).save();


        # flag=False
        # class_id=(classAttendance.objects.latest('id')).id

        # ongoingClass=classAttendance.objects.get(id=class_id)
        # current_time=datetime.datetime.now()
        # current_time=current_time.strftime("%H:%M:%S")

        # c_time=datetime.datetime.strptime(str(ongoingClass.create_time),'%Y-%m-%d %H:%M:%S.%f+00:00')
        # e_time=datetime.datetime.strptime(str(ongoingClass.close_time), '%Y-%m-%d %H:%M:%S.%f+00:00')
        # active=False
        # if c_time.strftime("%H:%M:%S")<= current_time and e_time.strftime("%H:%M:%S")>=current_time:
        #     active=True
            
        # context={''}

        



        

        
        # return render(request,'takeAttendance.html',{'flag':flag})
    # flag=True
    class_id=(classAttendance.objects.latest('id')).id

    ongoingClass=classAttendance.objects.get(id=class_id)
    current_time=datetime.datetime.now()
    current_time=current_time.strftime("%H:%M:%S")

    c_time=datetime.datetime.strptime(str(ongoingClass.create_time),'%Y-%m-%d %H:%M:%S.%f+00:00')
    e_time=datetime.datetime.strptime(str(ongoingClass.close_time), '%Y-%m-%d %H:%M:%S.%f+00:00')
    active=True
    flag=0
    if c_time.strftime("%H:%M:%S")<= current_time and e_time.strftime("%H:%M:%S")>=current_time:
        active=False
        classes=classAttendance.objects.all().order_by('-id').exclude(id=class_id)
        classes_history=[]
        for i in classes:
            total_student=studAttendance.objects.filter(class_id=i.id).count()
            present_student=studAttendance.objects.filter(class_id=i.id ,status=True).count()
            class_info=[i.id,i.subject_name,i.date,i.start_Time,i.end_Time,present_student,total_student]
            classes_history.append(tuple(class_info))

        context={'class_name':ongoingClass.subject_name,'start_time':ongoingClass.start_Time.strftime("%I:%M %p"),'date':ongoingClass.date,
        'end_time':ongoingClass.end_Time,'create_time':ongoingClass.create_time.strftime("%I:%M:%S %p"),'close_time':ongoingClass.close_time.strftime("%I:%M:%S %p"),'subject':ongoingClass.subject_name,'active':active,'classes':classes_history}
        print("innnnnnnnnnnn")
    #     flag=1
    # if flag:
    #     return redirect('/teachers/attendance/',context)
    else:
        classes=classAttendance.objects.all().order_by('-id')
        classes_history=[]
        for i in classes:
          
            total_student=studAttendance.objects.filter(class_id=i.id).count()
            present_student=studAttendance.objects.filter(class_id=i.id ,status=True).count()
            class_info=[i.id,i.subject_name,i.date,i.start_Time,i.end_Time,present_student,total_student]
            classes_history.append(tuple(class_info))
            
        context={'active':active,'classes':classes_history}
        print("outttttttttt")
    

    return render(request,'takeAttendance.html',context)


@login_required
def giveAttendance(request):

    class_id=(classAttendance.objects.latest('id')).id

    ongoingClass=classAttendance.objects.get(id=class_id)
    current_time=datetime.datetime.now()
    current_time=current_time.strftime("%H:%M:%S")
    print(current_time)
    c_time=datetime.datetime.strptime(str(ongoingClass.create_time),'%Y-%m-%d %H:%M:%S.%f+00:00')
    e_time=datetime.datetime.strptime(str(ongoingClass.close_time), '%Y-%m-%d %H:%M:%S.%f+00:00')
    active=False
    # context={'active':active}
    print(c_time.strftime("%H:%M:%S"))
    print(e_time.strftime("%H:%M:%S"))
    astatus=studAttendance.objects.filter(class_id=class_id).filter(student_id=(request.user).id).values('status').get()
    print("this is status",astatus['status'])
    if astatus['status']:
        status="Present"
    else:
        status="Absent"
    context={'class_name':ongoingClass.subject_name,'start_time':ongoingClass.start_Time.strftime("%I:%M %p"),
            'end_time':ongoingClass.end_Time.strftime("%I:%M %p"),'date':ongoingClass.date,'active':active,'status':status}
    
    if not astatus['status']:
        if c_time.strftime("%H:%M:%S")<= current_time and e_time.strftime("%H:%M:%S")>=current_time:
            active=True
            print("inside")
            context={'class_name':ongoingClass.subject_name,'start_time':ongoingClass.start_Time.strftime("%I:%M %p"),
            'end_time':ongoingClass.end_Time.strftime("%I:%M %p"),'create_time':e_time,'date':ongoingClass.date,'close_time':e_time.strftime("%I:%M:%S %p"),'active':active}
    
    

    return render(request,'giveAttendance.html',context)



@login_required
def record(request):
    print("infor1")
    context={}
    # report=classAttendance.objects.all().exclude((classAttendance.objects.latest('id')).id)
    if request.method=="POST":
        print("infor2")
        classId=request.POST['class_id']
        print(classId)
        classIs=classAttendance.objects.get(id=classId)
        print("this is class",classIs)
        studentsRecord=studAttendance.objects.filter(class_id=int(classId))
        print("This is stud",studentsRecord)
        records=[]

        for s in studentsRecord:
            user=User.objects.get(id=int(s.student_id))
            print("this is user",s.student_id)
            print(user)
            if(s.status):
                status="Present"
            else:
                status="Absent"
            student_row=[s.student_id,user,classIs.subject_name,classIs.date,classIs.start_Time,classIs.end_Time,status]
            print(student_row)
            records.append(tuple(student_row))
        
        

        context={'records':records}
    

    



        # return render(request,'record.html',context)
    classes_id=classAttendance.objects.all().order_by('-id')
    context['classes_id']=classes_id
    
    return render(request,'record.html',context)


@login_required
def teacherTimetable(request):
    return render(request,'teacherTimetable.html')


@login_required
def studentTimetable(request):
    return render(request,'studentTimetable.html')


@login_required
def myAttendance(request):

    myHistory=studAttendance.objects.filter(student_id=(request.user).id).order_by('-id')

    history=[]
    for m in myHistory:
        classId=classAttendance.objects.get(id=m.class_id)
        if(m.status):
            status="Present"
        else:
            status="Absent"

        records=[m.student_id,classId.subject_name,classId.date,classId.start_Time,classId.end_Time,status]
        history.append(tuple(records))






    return render(request,'myAttendance.html',{'history':history})
    