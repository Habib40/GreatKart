from django.shortcuts import render,redirect
from.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login
from .models import Account
from django.contrib import messages,auth
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from carts. models import Cart,CartItem
from carts. views import _cart_id
# for email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import requests


class RegisterView(View):
    def get(self, request):
        forms = RegistrationForm()
        return render(request, 'accounts/register.html', {'forms': forms})

    def post(self, request):
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            first_name = forms.cleaned_data['first_name']
            last_name = forms.cleaned_data['last_name']
            phone_number = forms.cleaned_data['phone_number']
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            
            # Create the user using the custom manager
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=email.split('@')[0],  # Assuming email before @ as username
                email=email,
                password=password
            )
            user.phone_number = phone_number
           
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            mail_body = render_to_string('accounts/account_activate_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)             
            })
            to_email = email
            from_email = 'habibkb5080@gmail.com'  # Replace with your sender email
            send_mail(mail_subject, mail_body, from_email, [to_email], fail_silently=False)

            return redirect("/accounts/login/?commands=verification&email=" +email)
        else:
            # If the form is not valid, show error messages
            for error in forms.errors.values():
                messages.error(request, error)

        return render(request, 'accounts/register.html', {'forms': forms})

def login_view(request):
    if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(request, email=email, password=password)
            if user is not None:
                
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        # getting the products variation by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))
                            #Get the cart items from user to access their product variations
                            cart_item = CartItem.objects.filter(user=user)
                            ex_vari_list = []
                            id = []
                            for item in cart_item:
                                existing_variation = item.variations.all()
                                ex_vari_list.append(list(existing_variation))
                                id.append(item.id)
                        # Check product_variation list in ex_vari_list
                            for pr in product_variation:
                                if pr in ex_vari_list:
                                    index = ex_vari_list.index(pr)
                                    item_id = id[index]
                                    item = CartItem.objects.get(id=item_id)
                                    item.quantity += 1  # Increase quantity by 1
                                    item.user= user
                                    item.save()
                                else:
                                    cart_item = CartItem.objects.filter(cart=cart)
                                    for item in cart_item:
                                       item.user= user
                                       item.save() 
                                    
                except:
                    pass
                auth.login(request, user)
                messages.success(request, 'You are logged in!')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                     nextPage = params['next']
                    return redirect(nextPage)
                except:
                  return redirect('dashboard') # Redirect to a success page after login
            else:
             messages.error(request, 'Invalid login credential.')
             return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def Logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out!")
    return redirect('login')
   
   
   
def Activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        
        
@login_required(login_url='login')        
def Dashboard(request):
    return render(request, 'accounts/dashboard.html')


def FogotPassword(request):
    if request.method=='POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user =Account.objects.get(email__exact=email)
          
            current_site = get_current_site(request)
            mail_subject = 'Reset Password To Access Your Account'
            mail_body = render_to_string('accounts/forgot_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)             
            })
            to_email = email
            from_email = 'habibkb5080@gmail.com'  # Replace with your sender email
            send_mail(mail_subject, mail_body, from_email, [to_email], fail_silently=False)
            messages.success(request,'To reset your password, please check your email.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist with this email.')
            return redirect('forgotPassword') 
    return render(request, 'accounts/forgotPsaaword.html')




def ResetPasswordValidation(request, uidb64, token):
    try:
        # Decode the uidb64 and convert to a string or integer
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid  # Store the uid in the session
        messages.success(request, 'Please reset your password.')
        return redirect(reverse('resetPassword'))
    else:
        messages.error(request, 'Invalid token.')
        return redirect(reverse('forgotPassword'))
            
def ResetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password and confirm_password:  # Check if both values are present
            if password == confirm_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request,'Password reset successfull.Now you can login')
                return redirect('login')
            else:
                messages.error(request, 'Password does not match!')
                return redirect('resetPassword')  
    else:          
      return render(request, 'accounts/resetPassword.html')