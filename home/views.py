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
                    return redirect('dashmember')
                # Pass the user's first name to the template
               # return render(request, 'login.html', {'username': user.username})
                else:
                    return redirect('admindashboard')
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})

    response = render(request,"login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response





def member(request):
    member_users = CustomUser.objects.filter(user_type='Member')
    member_count=member_users.count()
    context = {
                'member_users': member_users,
                'member_count':member_count,
             }
    return render(request,'member.html',context)


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



@login_required(login_url='login')
def admindashboard(request):
    users = CustomUser.objects.exclude(is_superuser=True)
    return render(request, 'admindashboard.html')







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

        return redirect('admindashboard')

    except Http404:
        # Handle the case where the user with the provided ID does not exist
        messages.error(request, "User not found.")
        return redirect('admindashboard')


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
    return redirect('admindashboard')
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
@login_required
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


@login_required
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


@login_required
def edit_application(request, job_card_id):
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



@login_required
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





@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Get updated data from the form
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # Update the user's profile with the new data
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('myprofile')

    return render(request, 'edit_user_profile.html', {'user': request.user})



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






def member_view_worker_list(request):
    worker_users = CustomUser.objects.filter(user_type='worker')
    worker_count=worker_users.count()
    context = {
                'worker_users': worker_users,
                'worker_count':worker_count,
             }
    return render(request, 'member_view_worker_list.html',context)


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

@login_required
def select_user_job(request):
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

@login_required
def add_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        Job.objects.create(title=job_title)
        # You can add additional logic or redirect to another page
        return redirect('add_job')
    return render(request, 'add_job.html')

def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        new_job_title = request.POST.get('new_job_title')

        # Validate if new_job_title is not empty
        if not new_job_title:
            messages.error(request, 'New job title cannot be empty.')
            return redirect('add_job')

        # Validate if the new job title already exists
        if Job.objects.exclude(id=job_id).filter(title=new_job_title).exists():
            messages.error(request, 'Job with the same title already exists.')
            return redirect('add_job')

        # If validation passes, update the job title
        job.title = new_job_title
        job.save()
        messages.success(request, f'Job "{new_job_title}" updated successfully.')

    return redirect('add_job')

def delete_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job_title = job.title
    job.delete()
    messages.success(request, f'Job "{job_title}" deleted successfully.')

    return redirect('add_job')




from django.shortcuts import render, get_object_or_404
from .models import UserSelectedJob

@login_required
def view_select_user_job(request):
    if not request.user.is_authenticated:
        # Handle unauthenticated user (redirect to login page, show an error message, etc.)
        return redirect('login')  
    user = request.user 
    #user_profile = CustomUser.objects.get(username=request.user.username)
    selected_works = UserSelectedJob.objects.filter(user=user)

    context = {
        'user': request.user,
        'selected_works': selected_works,
    }


    return render(request, 'edit_select_user_job.html', context)



@login_required
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


