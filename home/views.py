from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
#from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import user_passes_test
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
        worker_users = CustomUser.objects.filter(user_type='worker')
        mentor_user = CustomUser.objects.filter(is_mentor=True, user_type='worker').first()
    
        context = {
            'worker_users': worker_users,
            'mentor_user': mentor_user
        }
        response = render(request,"dashmember.html",context)
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
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type, is_verified=False)
        # You may want to do additional processing here if needed
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')  # Redirect to login page after successful registration

    return render(request,'registration.html')



from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
@never_cache
def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('email')
        password = request.POST.get('password')

        if loginusername == "panchayath01@gmail.com" and password == "Panchayath@123":
             #For the superuser, redirect to admin_index.html with user list and count
            return render(request, 'admindashboard.html')

            
        else:
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
                    if not user.is_verified:
                        error_message = 'Your account is not yet verified. Please wait for admin approval.'
                        return render(request, 'login.html', {'error_message': error_message})
                    return redirect('dashmember')
                else:
                    return redirect('admindashboard')
                # Pass the user's first name to the template
               # return render(request, 'login.html', {'username': user.username})
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})

    response = render(request,"login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse



#@user_passes_test(lambda u: u.is_authenticated, login_url='login')
def member(request):
    members_to_approve = CustomUser.objects.filter(user_type='Member', is_verified=False)
    member_users = CustomUser.objects.filter(user_type='Member')

    context = {
        'members_to_approve': members_to_approve,
        'member_users': member_users,
        'member_count': member_users.count(),
    }

    return render(request, 'member.html', context)


# views.py

# views.py

from django.http import JsonResponse
from .models import CustomUser
import json

def toggle_member_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, user_type='Member')

    # Toggle the member's status
    user.is_verified = not user.is_verified
    user.save()

    return HttpResponseRedirect(reverse('member'))




# views.py
from django.shortcuts import render, redirect
from .models import Member

def add_member(request):
    if request.method == 'POST':
        ward_number = request.POST.get('ward_number')
        member_name = request.POST.get('member_name')
        member_email = request.POST.get('member_email')

        Member.objects.create(
            ward_number=ward_number,
            member_name=member_name,
            member_email=member_email
        )


    return render(request, 'add_member.html')



def worker(request):
    worker_users = CustomUser.objects.filter(user_type='worker')
    worker_count=worker_users.count()
    context = {
                'worker_users': worker_users,
                'worker_count':worker_count,
             }
    return render(request,'worker.html',context)


def user(request):
    #user_profile = CustomUser.objects.get(user=request.user)
    regular_users = CustomUser.objects.filter(user_type='User')
    regular_count=regular_users.count()
    context = {
                #'user_profile':user_profile,
                'regular_users': regular_users,
                'regular_count':regular_count
             }
    return render(request,'user.html',context)




@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')



@never_cache
def logout(request):
    auth.logout(request)
    return redirect("/")

#@user_passes_test(lambda u: u.is_authenticated, login_url='admin:login')
@never_cache
@login_required
def admindashboard(request):
    users = CustomUser.objects.exclude(is_superuser=True)
    return render(request, 'admindashboard')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Panchayath


@user_passes_test(lambda u: u.is_authenticated, login_url='admin:login')
#@login_required(login_url='login')  # Adjust 'login' to your actual login URL
def panchayath_details(request):
    users = CustomUser.objects.exclude(is_superuser=True)

    if request.method == 'POST':
        # Retrieve the Panchayath name from the user input
        panchayath_name = request.POST.get('panchayath_name')

        # Check if the name is not empty
        Panchayath.objects.create(name=panchayath_name)

    return render(request, 'panchayath_details.html')







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404

def deactivate_user(request, user_id):
    User = get_user_model()

    try:
        user = get_object_or_404(User, id=user_id)

        if user.is_active:
            user.is_active = False
            user.save()
            
            # Send deactivation email
            subject = 'Account Deactivation'
            message = 'Your account has been deactivated by the admin.'
            from_email = 'jomolmariyajohnson2024b@mca.ajce.in'  # Replace with your email
            recipient_list = [user.email]
            html_message = render_to_string('deactivation_mail.html', {'user': user})

            send_mail(subject, message, from_email, recipient_list, html_message=html_message)

            messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
        else:
            messages.warning(request, f"User '{user.username}' is already deactivated.")

        return redirect('member')

    except Http404:
        # Handle the case where the user with the provided ID does not exist
        messages.error(request, "User not found.")
        return redirect('member')


def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'jomolmariyajohnson2024b@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('member')
#def user_login(request):
   # if request.method == 'POST':
    #    username = request.POST['username']
     #   password = request.POST['password']
#
 #       if username == "jeejay" and password == "jee123":
            # For the superuser, redirect to admin_index.html with user list and count
           # users = CustomUser.objects.exclude(is_superuser='1')  # Exclude superusers
            #user_count = users.count()
            #context = {
               # "users": users,
                #"user_count": user_count
            #}
           # return render(request, 'admin_index.html', context)
       # else:
    # For regular users, attempt to authenticate
            #user = authenticate(request, username=username, password=password)
          #  if user is not None:
               # login(request, user)
                #request.session['username'] = user.username
               # return redirect('home')
         #   else:
          #      messages.error(request, 'Invalid credentials!!')  # Set the error message
          #      return render(request, 'login.html')

   # return render(request, 'login.html')



from django.http import JsonResponse
  # Replace with your actual User model import

def get_user_data(request, user_type):
    if user_type == 'user':
        users = CustomUser.objects.filter(user_type='user').values('id', 'username', 'email')
    elif user_type == 'worker':
        users = CustomUser.objects.filter(user_type='worker').values('id', 'username', 'email')
    elif user_type == 'member':
        users = CustomUser.objects.filter(user_type='member').values('id', 'username', 'email')
    else:
        return JsonResponse({'error': 'Invalid user type'}, status=400)

    return JsonResponse(list(users), safe=False)





from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def fetchAndDisplayUsers(request, userType):
    users = CustomUser.objects.filter(user_type=userType).order_by('id')
    
    page = request.GET.get('page')
    paginator = Paginator(users, 10)  # Show 10 users per page

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'admindashboard.html', {'user_list': users, 'user_type': userType})






from .models import JobCard
@never_cache
@login_required(login_url='login')
def job_card_application(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Handle unauthenticated user (redirect to login page, show an error message, etc.)
            return redirect('login')  
        applicant_name = request.POST.get('applicant_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        house_name = request.POST.get('house_name')
        house_number = request.POST.get('house_number')
        panchayath = request.POST.get('panchayath')
        city = request.POST.get('city')
        district = request.POST.get('district')
        ration_card_number = request.POST.get('ration_card_number')
        category = request.POST.get('category')
        household_latrine = request.POST.get('household_latrine') == 'Yes'
        indira_avas_yojana = request.POST.get('indira_avas_yojana') == 'Yes'
        rofr_act = request.POST.get('rofr_act') == 'Yes'
        
        job_card = JobCard.objects.create(
            user=request.user,
            applicant_name=applicant_name,
            phone_number=phone_number,
            email=email,
            house_name=house_name,
            house_number=house_number,
            panchayath=panchayath,
            city=city,
            district=district,
            ration_card_number=ration_card_number,
            category=category,
            household_latrine=household_latrine,
            indira_avas_yojana=indira_avas_yojana,
            rofr_act=rofr_act
        )
        #job_card = JobCard.objects.filter(user=request.user)

        messages.success(request, 'Job Card submitted successfully!')
        
        #return redirect('view_user_jobcard', {'job_cards': job_card})  # Redirect to a confirmation page

    return render(request, 'job_card_application.html')
#def success(request):
 #   return render(request, 'user_dashboard/success.html')

def admin_view_job_cards(request):
    job_cards = JobCard.objects.all()
    return render(request, 'admin_view_job_cards.html', {'job_cards': job_cards})


@never_cache
@login_required(login_url='login')
def view_user_jobcard(request):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect to login page, show an error message, etc.)
        return redirect('login')  
    user = request.user 
    #user_profile = CustomUser.objects.get(username=request.user.username)
    job_cards = JobCard.objects.filter(user=user)

    return render(request, 'view_user_jobcard.html', {
        'user': user,
        'job_cards': job_cards,
    })


@never_cache
@login_required(login_url='login')
def edit_application(request, job_card_id):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect to login page, show an error message, etc.)
        return redirect('login') 
    job_card = get_object_or_404(JobCard, id=job_card_id, user=request.user)

    if request.method == 'POST':
        # Update the job card with the form data
        job_card.applicant_name = request.POST.get('applicant_name', '')
        job_card.phone_number = request.POST.get('phone_number', '')
        job_card.email = request.POST.get('email', '')
        job_card.house_name = request.POST.get('house_name', '')
        job_card.house_number = request.POST.get('house_number', '')
        job_card.panchayath = request.POST.get('panchayath', '')
        job_card.city = request.POST.get('city', '')
        job_card.district = request.POST.get('district', '')
        job_card.ration_card_number = request.POST.get('ration_card_number', '')
        job_card.category = request.POST.get('category', '')
        job_card.household_latrine = request.POST.get('household_latrine') == 'Yes'
        job_card.indira_avas_yojana = request.POST.get('indira_avas_yojana') == 'Yes'
        job_card.rofr_act = request.POST.get('rofr_act') == 'Yes'


        # Save the changes
        job_card.save()

        # Redirect to the user's job cards page
        return redirect('view_user_jobcard')

    return render(request, 'edit_application.html', {'job_card': job_card})



@never_cache
@login_required(login_url='login')
def delete_job_card(request, job_card_id):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect to login page, show an error message, etc.)
        return redirect('login')  

    # Ensure that the job card being deleted belongs to the logged-in user
    job_card = get_object_or_404(JobCard, id=job_card_id, user=request.user)

    # Perform the deletion
    job_card.delete()

    messages.success(request, 'Job Card deleted successfully!')
    
    return redirect('view_user_jobcard')





@never_cache
@login_required(login_url='login')
def edit_profile(request):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect to login page, show an error message, etc.)
        return redirect('login') 
    if request.method == 'POST':
        # Get updated data from the form
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        panchayath_name = request.POST['panchayath_name']
        ward_number = request.POST['ward_number']
        # Update the user's profile with the new data
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.panchayath_name = panchayath_name
        user.ward_number = ward_number
        request.user.has_edited_profile = True
        request.user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('myprofile')

    return render(request, 'edit_user_profile.html', {'user': request.user})


@never_cache
@login_required(login_url='login')

def worker_profile(request):
    if not request.user.is_authenticated:
            # Handle unauthenticated user (redirect to login page, show an error message, etc.)
            return redirect('login') 
    if request.method == 'POST':
        # Get updated data from the form
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        panchayath_name = request.POST['panchayath_name']
        ward_number = request.POST['ward_number']
        # Update the user's profile with the new data
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.panchayath_name = panchayath_name
        user.ward_number = ward_number
        user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('worker_view_profile')

    return render(request, 'worker_profile.html', {'user': request.user})


def worker_view_profile(request):
    return render(request,'worker_view_profile.html')

@never_cache
@login_required(login_url='login')
def myprofile(request):
    return render(request, 'myprofile.html')









# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import JobCard
from django.contrib import messages

def admin_approve_reject(request, job_card_id, action):
    #if not request.user.is_staff:
        # Redirect non-admin users to an appropriate page or show an error
        #return redirect('home')

    job_card = get_object_or_404(JobCard, id=job_card_id)

    if action == 'approve':
        job_card.approval_status = 'Approved'
        messages.success(request, 'Job Card approved successfully!')
    elif action == 'reject':
        job_card.approval_status = 'Rejected'
        messages.success(request, 'Job Card rejected successfully!')

    job_card.save()
    return redirect('admin_view_job_cards')






#def member_view_worker_list(request):
#    worker_users = CustomUser.objects.filter(user_type='worker')
#    worker_count=worker_users.count()
#    context = {
#                'worker_users': worker_users,
#                'worker_count':worker_count,
#             }
#    return render(request, 'member_view_worker_list.html',context)


'''from django.http import JsonResponse

def member_view_worker_list(request):
    if request.method == 'POST':
        # Get the user object
        user = CustomUser.objects.get(user_type='worker')
        
        # Update the mentor status
        is_mentor = request.POST.get('is_mentor', False)  # Assuming 'is_mentor' is sent in the request data
        user.is_mentor = is_mentor
        user.save()

        return JsonResponse({'message': 'Mentor status updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)'''

# views.py

#from django.shortcuts import render
#from .models import CustomUser  # Replace 'User' with your actual user model

from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser
@never_cache
@login_required(login_url='login')
def toggle_mentor_status(request):
     # Get all worker users
    worker_users = CustomUser.objects.filter(user_type='worker')
    mentor_user = CustomUser.objects.filter(is_mentor=True, user_type='worker').first()
    
    context = {
        'worker_users': worker_users,
        'mentor_user': mentor_user
    }
    return render(request, 'toggle_mentor_status.html', context)



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import CustomUser  # Assuming you have a CustomUser model
from django.contrib.auth.decorators import login_required
@never_cache
@login_required(login_url='login')
def add_remove_mentor(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        is_mentor = not user.is_mentor  # Toggle the mentor status
        user.is_mentor = is_mentor
        user.save()
        return redirect('toggle_mentor_status')  # Redirect after toggling mentor status
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


'''from django.http import JsonResponse
from .models import CustomUser

def toggle_mentor_status(request, user_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            user = CustomUser.objects.get(pk=user_id)
            if user:
                # Toggle mentor status
                user.is_mentor = not user.is_mentor
                user.save()
                return JsonResponse({'message': 'Mentor status toggled successfully.'})
            else:
                return JsonResponse({'error': 'User not found.'}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)'''



def add_mentor(request, worker_id):
    worker = CustomUser.objects.get(id=worker_id)
    worker.is_mentor = True
    worker.save()
    return redirect('member_view_worker_list')  # Replace 'worker_list' with your actual URL name

def remove_mentor(request, worker_id):
    worker = CustomUser.objects.get(id=worker_id)
    worker.is_mentor = False
    worker.save()
    return redirect('member_view_worker_list') 








def submit_job_card(request):
    # Logic for handling job card submission goes here
    # For example, save the submitted data to the database

    return render(request, 'submit_job_card.html')

def take_job(request):
    # Logic for handling taking a job goes here
    # For example, display available jobs or a form to request a job

    return render(request, 'take_job.html')







# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Job, Notification, UserProfile, UserSelectedJob, MemberApproval
from datetime import datetime, timedelta


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job, UserSelectedJob
from datetime import datetime, timedelta

@never_cache
@login_required(login_url='login')
def select_user_job(request):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect to login page, show an error message, etc.)
        return redirect('login') 
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            job = Job.objects.get(id=job_id)
            user = request.user

            # Perform validation or additional checks if needed

            # Create UserJobSelection object and save to the database
            user_job_selection = UserSelectedJob(user=user, job=job, start_date=start_date, end_date=end_date)
            user_job_selection.save()

            messages.success(request, 'Job selection saved successfully.')
        except Job.DoesNotExist:
            messages.error(request, 'Invalid job selection.')

    # Retrieve all selected jobs for the current user
    selected_jobs = UserSelectedJob.objects.filter(user=request.user)

    # Calculate remaining working days for all selected jobs for an entire year
    total_working_days_per_year = 100  # Total working days for each job in a year
    remaining_working_days = total_working_days_per_year

    for selected_job in selected_jobs:
        start_date = selected_job.start_date
        end_date = selected_job.end_date

        # Ensure the selected dates are within the same year
        if start_date.year == end_date.year == datetime.now().year:
            # Calculate the difference in days between start and end dates
            days_difference = (end_date - start_date).days + 1

            # Subtract the days for the current job from remaining_working_days
            remaining_working_days -= days_difference

    jobs = Job.objects.all()
    return render(request, 'select_user_job.html', {'jobs': jobs, 'selected_jobs': selected_jobs, 'remaining_working_days': remaining_working_days})




def member_approve_reject(request, user_selected_job_id, status):
    user_selected_job = UserSelectedJob.objects.get(id=user_selected_job_id)
    member = request.user

    if status == 'approve':
        user_selected_job.status = 'Approved'
        user_selected_job.save()

        # Send notification to worker
        Notification.objects.create(user=user_selected_job.user, job=user_selected_job.job, date=user_selected_job.start_date, is_confirmed=True)

        messages.success(request, f"The job request for '{user_selected_job.job.title}' has been approved.")
    elif status == 'reject':
        rejection_reason = request.POST.get('rejection_reason')
        user_selected_job.status = 'Rejected'
        user_selected_job.rejection_reason = rejection_reason
        user_selected_job.save()

        # Notify the user about the rejection
        messages.success(request, f"The job request for '{user_selected_job.job.title}' has been rejected with reason: {rejection_reason}")

    # Create a record for member approval
    MemberApproval.objects.create(member=member, user_selected_job=user_selected_job, status=status)

    return redirect('dashboard')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Job
@never_cache
def add_jobs(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        Job.objects.create(title=job_title)
        # You can add additional logic or redirect to another page
        return redirect('view_add_job')
    return render(request, 'add_jobs.html')

def view_add_job(request):
    # Fetch all jobs from the database
    jobs = Job.objects.all()

    # Pass the jobs to the template
    return render(request, 'view_add_job.html', {'jobs': jobs})


def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    if request.method == 'POST':
        # Update job attributes based on form data
        job.title = request.POST.get('job_title')  # Add other fields as needed
        job.save()
        return redirect('view_add_job')  # Redirect to the admin dashboard or another page

    return render(request, 'edit_job.html', {'job': job})

def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    job.delete()
    return redirect('view_add_job') 




from django.shortcuts import render, get_object_or_404
from .models import UserSelectedJob
@never_cache
@login_required(login_url='login')
def view_select_user_job(request):
    user_selected_jobs = UserSelectedJob.objects.select_related('job').filter(user=request.user)
    context = {
        'user_selected_jobs': user_selected_jobs,
    }
    return render(request, 'view_select_user_job.html', context)


@never_cache
@login_required(login_url='login')
def edit_select_user_job(request, user_select_job_id):
    user_select_job = get_object_or_404(UserSelectedJob, id=user_select_job_id)

    # Assuming 'jobs' is a queryset of available jobs
    jobs = Job.objects.all()

    context = {
        'user_select_job': user_select_job,
        'jobs': jobs,
        # Add other context data as needed
    }

    return render(request, 'edit_select_user_job.html', context)


@never_cache
@login_required(login_url='login')
def delete_select_user_job(request, job_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    # Get the UserSelectedJob instance to be deleted
    user_selected_job = get_object_or_404(UserSelectedJob, id=job_id, user=request.user)

    # Handle the POST request for deletion
    user_selected_job.delete()

    return redirect('view_select_user_job')





from django.shortcuts import render, redirect
from .models import UserSelectedJob

def admin_view_user_job(request):
    #pw_details = CustomUser.objects.get(panchayath=panchayath_name,ward=ward_number)
    user_jobs = UserSelectedJob.objects.all()
    return render(request, 'admin_view_user_job.html', {'user_jobs': user_jobs})


'''def admin_toggle_approval(request, user_job_id):
    user_selected_job = UserSelectedJob.objects.get(pk=user_job_id)

    # Check the submitted button value
    action = request.POST.get('action', None)

    if action == 'approve':
        user_selected_job.status = 'Approved'
    elif action == 'reject':
        user_selected_job.status = 'Rejected'

    user_selected_job.save()

    # Add any additional logic or messages as needed
    messages.success(request, f'The job has been {user_selected_job.status.lower()} successfully.')

    return redirect('admin_view_user_job')'''
# views.py
from django.contrib import messages
from django.shortcuts import redirect
from .models import UserSelectedJob, Notification

def admin_toggle_approval(request, user_job_id):
    user_selected_job = UserSelectedJob.objects.get(pk=user_job_id)

    # Check the submitted button value
    action = request.POST.get('action', None)

    if action == 'approve':
        user_selected_job.status = 'Approved'
        # Save notification to the database
        save_notification(user_selected_job.user.username, user_selected_job.job.title, user_selected_job.start_date, user_selected_job.end_date)
    elif action == 'reject':
        user_selected_job.status = 'Rejected'

    user_selected_job.save()

    # Add any additional logic or messages as needed
    messages.success(request, f'The job has been {user_selected_job.status.lower()} successfully.')

    return redirect('admin_view_user_job')

def save_notification(worker_username, job_title, start_date, end_date):
    # Create notification message
    message = f"The user {worker_username} job '{job_title}' is approved for the period {start_date} to {end_date}."

    # Save notification to the database
    Notification.objects.create(user=CustomUser.objects.get(username=worker_username), content=message)







# Add this code to your Django views.py file

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

def get_member_users(request):
    search_query = request.GET.get('search', '')
    members = User.objects.filter(username__icontains=search_query, groups__name='member')
    
    # Convert members to JSON format
    member_data = [{'id': member.id, 'username': member.username, 'email': member.email, 'is_active': member.is_active} for member in members]

    return JsonResponse(member_data, safe=False)




from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Notification, UserSelectedJob, JobAccepted

@login_required(login_url='login')
def worker_jobs(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        action = request.POST.get('action')

        if action == 'accept':
            # Get the job instance
            job = UserSelectedJob.objects.get(id=job_id)

            # Check if the job is already accepted by the worker for the specific job
            if JobAccepted.objects.filter(worker=request.user, job_title=job.job.title, applied_by=job.user.username).exists():
                # If the job is already accepted, redirect back to worker jobs page
                return redirect('worker_jobs')

            # Perform actions when job is accepted
            # For example, update the database or send notifications
            # Update the job status or any other relevant action

            # Create a notification for the user
            Notification.objects.create(
                user=request.user,
                content=f"Job '{job.job.title}' has been accepted by worker '{request.user.username}'."
            )

            # Calculate total work based on start and end dates
            total_work = (job.end_date - job.start_date).days

            # Create an instance of AcceptedJob
            JobAccepted.objects.create(
                worker=request.user,
                job_title=job.job.title,
                content=f"Job '{job.job.title}' has been accepted by worker '{request.user.username}'.",
                total_work=total_work,
                applied_by=job.user.username,  # Storing the username of the job applicant
                is_accepted=True
            )

        elif action == 'reject':
            # Get the job instance
            job = UserSelectedJob.objects.get(id=job_id)

            # Perform actions when job is rejected
            # For example, update the database or send notifications
            # Update the job status or any other relevant action

            # Create a notification for the user
            Notification.objects.create(
                user=request.user,
                content=f"Job '{job.job.title}' has been rejected by worker '{request.user.username}'."
            )

        # After processing the form, redirect the user back to the jobs page or any other desired page
        return redirect('worker_jobs')

    else:
        # If it's not a POST request, continue with normal rendering of the jobs page
        # Filter approved jobs excluding those already accepted by the current user
        accepted_job_titles = JobAccepted.objects.filter(worker=request.user, is_accepted=True).values_list('job_title', flat=True)
        approved_jobs = UserSelectedJob.objects.filter(status='Approved').exclude(job__title__in=accepted_job_titles)

        # Get notifications for the user
        notifications = Notification.objects.filter(user=request.user)

        return render(request, 'worker_jobs.html', {'approved_jobs': approved_jobs, 'notifications': notifications})

from django.shortcuts import render, redirect
from .models import Complaint
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def complaints(request):
    if request.method == 'POST':
        # Extract the complaint text and type from the POST request
        complaint_text = request.POST.get('complaint')
        complaint_type = request.POST.get('complaint-type')

        # Check if the complaint contains valid keywords
        valid_keywords = ['complaint', 'issue', 'problem']
        if any(keyword in complaint_text.lower() for keyword in valid_keywords):
            # Create a new Complaint object for the logged-in user with complaint type and save it to the database
            new_complaint = Complaint(user=request.user, complaint_type=complaint_type, complaint=complaint_text)
            new_complaint.save()

            # Redirect to a success page or any other page you want
            return redirect('complaints')  # Assuming you have a URL named 'complaints'
        else:
            # If the complaint does not contain valid keywords, display an error message
            messages.error(request, 'Invalid complaint. Please include relevant details such as "complaint", "issue", or "problem".')
            return redirect('complaints')  # Redirect back to the complaints page
    else:
        # Retrieve complaints submitted by the logged-in user
        user_complaints = Complaint.objects.filter(user=request.user)
        return render(request, 'complaints.html', {'complaints': user_complaints})







from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint

def admin_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'admin_complaints.html', {'complaints': complaints})




from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from .models import Complaint


def admin_response(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        # Process admin response
        # For simplicity, let's assume the response is stored directly in the complaint model
        response_text = request.POST.get('admin_response')
        complaint.admin_response = response_text
        complaint.save()
        return redirect('admin_complaints')
    else:
        return render(request, 'admin_response.html', {'complaint': complaint})



#from django.shortcuts import render, redirect
#from .models import JobAccepted
#def accepted_jobs(request):
#    if request.method == 'POST':
#        job_id = request.POST.get('job_id')
#        worker_id = request.POST.get('worker_id')
#        action = request.POST.get('action')
#
#       if action == 'accept':
#            # Retrieve job details from the database
#            job = Job.objects.get(pk=job_id)
#           worker = CustomUser.objects.get(pk=worker_id)
#            
#            # Create AcceptedJob entry
#            accepted_job = JobAccepted.objects.create(
#                worker=worker,
#                job=job,
#                is_accepted=True,
#                total_working_days=0  # Initialize total_working_days to 0
#            )
#            accepted_job.save()
#       elif action == 'reject':
#            # Implement rejection logic if needed
#           pass
#
#       # Redirect back to the worker jobs page
#        return redirect('worker_jobs')
#    else:
#        approved_jobs = JobAccepted.objects.filter(is_accepted=True)
#        context = {'approved_jobs': approved_jobs}
#       return render(request, 'worker_jobs.html', context)





def view_worker_job(request):
    # Retrieve distinct accepted jobs with additional information for the current worker
    user_id = request.user.id  # Retrieve the user ID
    accepted_jobs = JobAccepted.objects.filter(worker_id=user_id).values(
        'job_title', 'applied_by', 'total_work'
    ).distinct()
    context = {'accepted_jobs': accepted_jobs}
    return render(request, 'view_worker_job.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadedImage

@login_required
def upload_image(request):
    if request.method == 'POST':
        # Assuming you have a CustomUser model and the user is authenticated
        user = request.user
        image_file = request.FILES.get('image')
        # Create and save the UploadedImage instance with the user set
        uploaded_image = UploadedImage.objects.create(user=user, image=image_file)
        # Redirect to the same page or any other page as needed
        return redirect('upload_image')
    
    # Retrieve all uploaded images from the database
    images = UploadedImage.objects.all()
    
    # Pass the images and other necessary data to the template
    return render(request, 'upload_image.html', {'images': images})



@login_required
def delete_image(request, image_id):
    # Retrieve the uploaded image instance
    image = get_object_or_404(UploadedImage, id=image_id)
    # Ensure that the user owns the image before deletion
    if image.user == request.user:
        # Delete the image
        image.delete()
    # Redirect back to the upload_image view
    return redirect('upload_image')


from django.shortcuts import get_object_or_404
from .models import CustomUser, Attendance

def add_attendance(request):
    if request.method == 'GET' and request.user.is_mentor:
        # Retrieve unique job titles and their corresponding applied by usernames
        job_titles = JobAccepted.objects.values_list('job_title', flat=True).distinct()
        applied_by_usernames = JobAccepted.objects.values_list('applied_by', flat=True).distinct()

        # Create a dictionary to store job assignments and attendance records
        job_assignments = {}
        attendance_records = {}

        # Iterate over unique job titles and applied by usernames
        for title in job_titles:
            for username in applied_by_usernames:
                # Get job accepted instances for the current job title and applied by username
                job_accepted_instances = JobAccepted.objects.filter(job_title=title, applied_by=username)

                # Aggregate job assignments and attendance records
                workers = []
                for job_accepted in job_accepted_instances:
                    # Retrieve the CustomUser instance based on the username
                    worker = get_object_or_404(CustomUser, username=job_accepted.worker.username)
                    workers.append(worker)

                job_assignments[(title, username)] = workers
                attendance_records[(title, username)] = Attendance.objects.filter(worker__in=workers)

        # Pass job assignments and attendance records to the template
        context = {
            'job_assignments': job_assignments,
            'attendance_records': attendance_records
        }

        return render(request, 'add_attendance.html', context)
    else:
        return redirect('add_attendance')  # Redirect to a default page if the conditions are not met



from django.shortcuts import render
from collections import defaultdict
from .models import UserSelectedJob, JobAccepted

def member_view_users_jobs(request):
    # Retrieve the job accepted workers ordered by start date
    approved_jobs = UserSelectedJob.objects.filter(status='Approved')
    user_selected_jobs = UserSelectedJob.objects.all().order_by('start_date')

    # Retrieve job accepted workers ordered by starting date and number of workers who accepted the job
    #job_accepted_workers = JobAccepted.objects.all().order_by('start_date', '-total_work')
    
    # Create a nested dictionary to store the total number of workers for each user and job
    total_workers = []

    # Iterate over user selected jobs
    for job in user_selected_jobs:
        # Count the number of workers for the current job and user
        count = JobAccepted.objects.filter(job_title=job.job.title, applied_by=job.user.username).count()
        # Append the tuple to the list
        total_workers.append((job.job.title, count))
    context = {
        'approved_jobs': approved_jobs,
        #'job_accepted_workers': job_accepted_workers,
        'user_selected_jobs': user_selected_jobs,
        'total_workers': total_workers
    }
    return render(request, 'member_view_users_jobs.html', context)



from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import JobAccepted

def start_work(request):
    if request.method == 'POST':
        # Retrieve form data
        job_title = request.POST.get('job_title')
        applied_by_username = request.POST.get('applied_by_username')
        
        # Print job title and applied by username for debugging
        #print("Job Title:", job_title)

        #print("Applied By Username:", applied_by_username)
        
        # Get all JobAccepted instances for the specified job title and applied by username
        job_accepted_instances = JobAccepted.objects.filter(
            job_title=job_title,
            applied_by=applied_by_username
        )
        
        # Update is_work_started field for each instance
        for job_accepted in job_accepted_instances:
            job_accepted.is_work_started = True
            job_accepted.save()
            
        
        # Redirect to a success page or any other desired URL
        return redirect('member_view_users_jobs')
    
    else:
        # Handle GET requests (if needed)
        pass





def view_started_work(request):
    # Retrieve JobAccepted instances where work is started
    started_work = JobAccepted.objects.filter(is_work_started=True)

    context = {
        'started_work': started_work
    }

    return render(request, 'started_work.html', context)