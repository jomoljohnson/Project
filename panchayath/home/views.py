from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
#from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib import messages
# Create your views here.




def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def contact(request):
    return render(request,'contact.html')
#def dashuser(request):
    #return render(request,'dashuser.html')
#def dashworker(request):
    #return render(request,'dashworker.html')
#def dashmember(request):
    #return render(request,'dashmember.html')



@never_cache
@login_required(login_url='login')
def dashuser(request):
    if 'username' in request.session:
        response = render(request,"dashuser.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')
    
@never_cache
@login_required(login_url='login')
def dashworker(request):
    if 'username' in request.session:
        response = render(request,"dashworker.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')



@never_cache
@login_required(login_url='login')
def dashmember(request):
    if 'username' in request.session:
        response = render(request,"dashmember.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')
    


@never_cache
def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # Make sure this matches your form field name
        user_type = request.POST['user_type']

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'registration.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        # You may want to do additional processing here if needed
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')  # Redirect to login page after successful registration

    return render(request,'registration.html')



from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
@never_cache
def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        password = request.POST.get('password')

        if loginusername and password:
            user = authenticate(request, username=loginusername, password=password)

            if user is not None:
                auth_login(request, user)
                request.session['username'] = user.username
                # Check the user's role and redirect accordingly
                if user.user_type == 'User':
                    return redirect('dashuser')
                elif user.user_type == 'worker':
                    return redirect('dashworker')
                elif user.user_type == 'Member':
                    return redirect('dashmember')
                # Pass the user's first name to the template
               # return render(request, 'login.html', {'username': user.username})
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = 'Username and password are required'
            return render(request, 'login.html', {'error_message': error_message})

    response = render(request,"login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response





@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')



@never_cache
def logout(request):
    auth.logout(request)
    return redirect("/")
