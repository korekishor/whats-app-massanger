import pytesseract
import cv2
from upload_image.settings import MEDIA_ROOT
import mysql.connector
import mysql
from django.shortcuts import render,HttpResponse
from .models import Image
import json
from django.http import JsonResponse
from django.http import JsonResponse
import random
import uuid

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="employeedb",
)

mycursor = mydb.cursor()    


def home(request):
    global mycursor

    if request.method == "POST":

        image = request.FILES['img']
        save_image = Image(photo=image)
        save_image.save()

        image_path_from_user = "{}".format(str(image))

        insert_image_query = "INSERT INTO path_image_table (path_image) VALUES (%s)"

        image_path_with_media_root = [
            f"media/images/{str(image_path_from_user)}"] 

        mycursor.execute(insert_image_query, (image_path_with_media_root))
 

        select_path = "select path_image from path_image_table where path_image= %s"
        mycursor.execute(select_path, (image_path_with_media_root))

        get_image_path = mycursor.fetchone()

        root_image = str(MEDIA_ROOT).replace('\\', '/')+"/images/"+str(image)

        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kishor kore\AppData\Local\Tesseract-OCR\tesseract.exe'

        img = cv2.imread(r"{}".format(root_image), cv2.IMREAD_GRAYSCALE)

        text = pytesseract.image_to_string(img)

        return render(request, "home.html", {'image': image_path_with_media_root[0], 'text': text})

    return render(request, 'home.html')

def index(request,groupname):
    return render(request,'websocket_html/index.html',{'groupname':groupname})

def login_user(request):
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['psw']

        select_path = "select User_access_id from massage_user where password= %s"
        mycursor.execute(select_path, ([str(password)]))

        get_image_path = mycursor.fetchone()     

        if get_image_path is not None:
            if username==get_image_path[0]:
                return render (request,'websocket_html/chatroom.html',{'used_username':username})
            else:
                return HttpResponse ("filL")

        return render(request, 'websocket_html/login.html')
    return render(request, 'websocket_html/login.html')


def signup(request):
    if request.method=='GET':
        user_id = request.GET.get('user_id1',None)
        user_password = request.GET.get('psw1',None)
        
        uniq_code=uuid.uuid4().hex
        
        insert_image_query = "insert into massage_user ( User_access_id,Uniq_id,password) VALUES (%s,%s,%s)"
        
        mycursor.execute(insert_image_query, (user_id,uniq_code, user_password))
        mydb.commit()
        jsondata = {'data': ['']}
      
        return JsonResponse (jsondata)
         
def chatroom(request):
    return render(render,'websocket_html/chatroom.html')

def get_url_to_talk(request):
    if request.method=="GET":
        user_id = request.GET.get('user_name',None)
        talk_to = request.GET.get('talk_to',None)
        
        
        select_with_chat_uniq_id = "select Uniq_id from massage_user where User_access_id= %s"
        mycursor.execute(select_with_chat_uniq_id, ([str(talk_to)]))
        select_with_chat_uniq_id = mycursor.fetchone()

        select_with_chat_uniq_id=select_with_chat_uniq_id[0]

        user_uiniq_query = "select Uniq_id from massage_user where User_access_id= %s"
        mycursor.execute(user_uiniq_query, ([str(user_id)]))
        talk_to_uniq_id = mycursor.fetchone()
        talk_to_uniq_id=talk_to_uniq_id[0] 

        user_uniq_id,talk_to_uniq_id,s=select_with_chat_uniq_id,talk_to_uniq_id,''
        
        if user_uniq_id<talk_to_uniq_id:
            s=user_uniq_id+talk_to_uniq_id
        else:
            s=talk_to_uniq_id+user_uniq_id

        jsondata = {'data': [s]}
      
        return JsonResponse (jsondata)

    return HttpResponse("got connected")