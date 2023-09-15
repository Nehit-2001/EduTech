from django import template
from ..models import *

register = template.Library()

@register.simple_tag
def price_after_discount(price, discount):
    
    if discount is 0 or discount is None:
        return price
    
    sp = price
    
    sp = sp - (sp * discount * 0.01)
    return int(sp)

@register.simple_tag
def is_enroll(request, course):
    user = None
    
    try:
        if not request.session['name']:
            return False
    except:
        return False
    
    
    user = Signup.objects.get(email=request.session['email'])
    
    
    try:
        user_course = User_Course.objects.get(user=user, course=course)
        return True
    
    except:
        return False