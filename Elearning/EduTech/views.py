from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from .models import *
import razorpay
from django.contrib.auth.hashers import check_password, make_password
from Elearning.settings import *
from time import time


client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def home(request):
    
    course_dtls = Course_details.objects.all()
    context = {
        'course_dtls' : course_dtls,
    }
    
    return render(request, 'index.html', context=context)


def contact(request):
    return render(request, 'contact.html')


def sign_up(request):
    if request.method == 'POST':
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        email_id = request.POST.get('email')
        password = request.POST.get('password')
        mobile_no = request.POST.get('mobile')
        gender = request.POST.get('gender')
        
        sign_obj = Signup(
            first_name = f_name,
            last_name = l_name,
            email = email_id,
            password = make_password(password),
            mobile = mobile_no,
            gender = gender,
        )
        
        sign_obj.save()
        return HttpResponse("Registration successful")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
           email_id = Signup.objects.get(email = email)
        
           if email_id:
               if check_password(password, email_id.password):
                   request.session['name'] = email_id.first_name
                   request.session['email'] = email_id.email
                   return redirect('home')
               else:
                   return HttpResponse("wrong password")
        except:
            return HttpResponse("email does not exist")


def logout(request):
    request.session.clear()
    return redirect('home')
    
    
def course(request, slug):
    course = Course_details.objects.get(slug=slug)
    s_no = request.GET.get('serial_no')
    
    if s_no is None:
        s_no = 1
    
    try:
        video = Videos.objects.get(video_belong=course, video_seq=s_no)
        if video.is_preview is False:
            if request.session.get('name') is None:
                return redirect('home')
            
            else:
                user_id = Signup.objects.get(
                    email = request.session['email'])
                print(user_id)
        
    except:
        return redirect('home')
    
    return render(request, 'course.html',{'video_fetch': course, 'video': video})


def checkout(request, slug):
    course = Course_details.objects.get(slug=slug)
    
    
    payment = None
    order = None
    create_payment = request.GET.get('action')
    if create_payment == "payment":
        data = { 
                "amount": 500, 
                "currency": "INR", 
                "receipt": f"Elearning-{int(time())}" 
        }
        order = client.order.create(data=data) 
        payment = Payment()
        
    
    context = {
        'course':course,
         'pay' : payment,
        'order': order   
    }
    
    return render(request, 'checkout.html', context=context)
        
    
    