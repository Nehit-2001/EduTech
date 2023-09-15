from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from .models import *
import razorpay
from django.contrib.auth.hashers import check_password, make_password
from Elearning.settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt, csrf_protect


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
                # print(user_id)
        
    except:
        return redirect('home')
    
    return render(request, 'course.html',{'video_fetch': course, 'video': video})


def checkout(request, slug):
    course = Course_details.objects.get(slug=slug)
    coupon_code = request.GET.get('coupon')
    
    
    try:
       user_id = Signup.objects.get(
                     email = request.session['email'])
    
    except:
        return redirect('home')
    
    
    payment = None
    order = None
    order_id = None
    error = None
    coup_msg = None
    coup = None
    amount = None
    if error is None:
        amount = int(course.price - (course.price * course.discount * 0.01))
        amount = amount * 100
    
    if coupon_code:
        try:
            coup = Ref_code.objects.get(code=coupon_code, course=course)
            amount = int(course.price - (course.price * coup.discount * 0.01))
            amount = amount * 100
            # coup_msg = "Successfully Applied"
            # print(coup_msg)
            # print("coupon code", "-----", amount)
            # print(amount)
        except:
            coup_msg = "Invalid Coupon Code"
    
    create_payment = request.GET.get('action')
    if create_payment == "payment":
        try:
            user_course = User_Course.objects.get(user=user_id, course=course)
            return HttpResponse("You have already purchesed this course")
        except:
            pass
        
        
        data = { 
                "amount": amount, 
                "currency": "INR", 
                "receipt": f"Elearning-{int(time())}" 
        }
        order = client.order.create(data=data) 
        
        order_id = order.get('id')
        payment = Payment()
        payment.order_id = order_id
        payment.course = course
        payment.user_info =  user_id
        payment.save()
        
    
    context = {
        'course':course,
        'pay' : 1,
        'order': order,  
        'order_id': order_id,
        'amount' : amount,
        'coupon_msg' : coup_msg,
        'coup' : coup
    }
    
    return render(request, 'checkout.html', context=context)


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        # print(request.POST)
        data = request.POST
        client.utility.verify_payment_signature(
        # 'razorpay_order_id': razorpay_order_id,
        # 'razorpay_payment_id': razorpay_payment_id,
        # 'razorpay_signature': razorpay_signature
        data
        )
        payment = Payment.objects.get(order_id = data['razorpay_order_id'])
        payment.payment_id = data['razorpay_payment_id']
        payment.status = True
       
        
        usercourse = User_Course(user = payment.user_info, course = payment.course)
        usercourse.save()
        
        payment.course_info = usercourse
        
        payment.save()
        
    try:
        return redirect('mycourse')
    except:
        return redirect('not working')
    
    
def mycourse(request):
    user = Signup.objects.get(email=request.session['email'])
    
    user_course = User_Course.objects.filter(user=user)
    
    context = {
        'user_course' : user_course
    }
    
    return render (request, 'mycourse.html', context=context)

        
    
    