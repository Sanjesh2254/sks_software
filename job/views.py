# Built in packages
import openpyxl
import os
import logging

# Django sub modules
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages


from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse


# google package
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Models
from .models import JobPosting, Application, Category
from .models import Application,UserProfile

# forms

from .forms import JobPostingForm, ApplyForm, CategoryForm
from .forms import UserProfileForm
from .forms import JobPostingForm
from .forms import RegistrationForm

# openpyxl
from openpyxl.styles import Font
from openpyxl.worksheet.hyperlink import Hyperlink
import pandas as pd






# ------------------------------------------- index page --------------------------------------------------------
def index(request):
    return render(request, 'job/index.html')


# -------------------------------------------login page---------------------------------------------------------


def login_view(request):
    if request.user.is_authenticated:
        return redirect('superhome')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('superhome')  # Redirect to a success page or home
    else:
        form = AuthenticationForm()
    return render(request, 'job/login.html', {'form': form})





#-----------------------------------Register page ----------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in after registration
            return redirect('superhome')  # Redirect to home or another page after registration
    else:
        form = RegistrationForm()
    
    return render(request, 'job/register.html', {'form': form})


#-------------------------------------Home page-------------------------------------------------------


@login_required
def superhome(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    if query:
        # Use Q objects to filter with OR condition
        job_postings = JobPosting.objects.filter(
            Q(category__name__icontains=query) | Q(title__icontains=query)
        )
    else:
        job_postings = JobPosting.objects.all()
    
    context = {
        'job_postings': job_postings,
        'applicants': {job.pk: job.applicants.all() for job in job_postings}  # Dictionary of job IDs and their applicants
    }
    return render(request, 'job/superhome.html', context)









#--------------------------------About page(user)------------------------------------------------------------

def about(request):
    return render(request, 'job/about.html')

#------------------------------Contact page(user)------------------------------------------------------

def contact(request):
    return render(request, 'job/contact.html')

#-----------------------------------category create(admin)-------------------------------------------

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_create')  # Redirect to the same page or another page
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'job/category_form.html', {'form': form, 'categories': categories})

#----------------------------------category list(admin)----------------------------------------

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'job/category_form.html', {'categories': categories})

#----------------------------------Job Posting(admin)-------------------------------------------------------

@login_required
def job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_posting')  # Redirect to the same page or another page
    else:
        form = JobPostingForm()
    return render(request, 'job/job_posting.html', {'form': form})

#------------------------------------------Apply listing------------------------------------------------------------

@login_required


def applylisting(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)
    
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        if application_id:
            application = get_object_or_404(Application, id=application_id)
            application.delete()
        else:
            # Handle other POST actions
            Application.objects.filter(job_posting=job).delete()  # Only delete applications for this job
        return redirect('applylisting', job_id=job_id)
    
    applications = Application.objects.filter(job_posting=job)
    context = {'job': job, 'applications': applications}
    return render(request, 'job/applylistings.html', context)





    
#--------------------------------------------edit_application----------------------------------------------
@login_required
def edit_job_posting(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)

    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_posting)
        if form.is_valid():
            form.save()
            return redirect('superhome')  # Redirect to the list page after save
    else:
        form = JobPostingForm(instance=job_posting)

    return render(request, 'job/edit_job_posting.html', {'form': form})


    
#--------------------------------------------delete_job_posting(admin)---------------------------------------------

@login_required
def delete_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)
    if request.method == 'POST':
        job_posting.delete()
        return redirect('superhome')
    return render(request, 'job/delete_confirm.html', {'job_posting': job_posting})  # Assuming you have a confirmation template

#----------------------------------------------Job Apply page(user)----------------------------------

SERVICE_ACCOUNT_FILE = r'C:\Users\rsanj\Downloads\projectsks-9fd9104d328b.json'  # Replace with the actual path

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_gdrive(file_path, file_name, folder_id):
    try:
        # Authenticate using the service account
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        # Define file metadata
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        # Media file upload instance
        media = MediaFileUpload(file_path, mimetype='application/pdf')  # Adjust MIME type if needed

        # Create a file on Google Drive
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Generate the file's Google Drive link
        return f"https://drive.google.com/file/d/{file.get('id')}/view"
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None








logger = logging.getLogger(__name__)
 




@login_required
  # Make sure this function is correctly implemented



 # Assuming this function exists in a utils module

 # Make sure to import your utility function

def apply(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)  # Fetch the job

    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            form_instance = form.save(commit=False)  # Save form but don't commit yet
            form_instance.job_posting = job  # Link the job to the application
            form_instance.save()  # Now save the form

            # Handle file upload
            uploaded_file = request.FILES.get('resume')
            if uploaded_file:
                file_name = uploaded_file.name

                # Ensure the 'temp' directory exists
                temp_dir = 'temp'
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                file_path = os.path.join(temp_dir, file_name)

                # Save the uploaded file temporarily
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Google Drive folder ID where you want to store the files
                folder_id = '1-9qff7gR8UtbO3JEeqATS82pr8GkdUdz'  # Replace with your actual folder ID

                # Upload to Google Drive
                gdrive_link = upload_to_gdrive(file_path, file_name, folder_id)

                if gdrive_link:
                    # Update the application instance with the Google Drive link
                    form_instance.resume_link = gdrive_link
                    form_instance.save()

                    # Delete the temporary file
                    os.remove(file_path)

            # Prepare email details
            subject = 'New Job Application Submitted'
            message = f"""
            A {job.title} job application has been submitted.

            Applicant Name: {form_instance.applicant_name}
            Address: {form_instance.address}
            Email: {form_instance.email}
            Phone Number: {form_instance.phone_number}
            Age: {form_instance.age}
            Gender: {form_instance.gender}
            Skills: {form_instance.skills}
            Education: {form_instance.education}
            Experience: {form_instance.experience}
            Resume Link: {form_instance.resume_link}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [form_instance.email]  # Use recipient email from the form

            try:
                # Send email
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Your application has been successfully submitted!')
            except Exception as e:
                # Handle email sending errors
                messages.error(request, 'There was an error sending the notification email. Please try again later.')
                print(f"Error sending email: {e}")

            # Redirect to a success page or any other page
            return redirect(f'{reverse("superhome")}?success=true') # Replace 'superhome' with your success URL name

    else:
        # Pre-fill the form with user's profile data
        user_profile = UserProfile.objects.get(user=request.user)
        initial_data = {
            'applicant_name': user_profile.full_name,
            'address': user_profile.address,
            'email': user_profile.email,
            'phone_number': user_profile.phone_number,
            'age': user_profile.age,
            'gender': user_profile.gender,
            'skills': user_profile.skills,
            'education': user_profile.education,
            'experience': user_profile.experience,
        }
        form = ApplyForm(initial=initial_data)

    return render(request, 'job/apply.html', {'form': form, 'job': job})












#----------------------------------------export_job_listings_excel------------------------------------------
@login_required
def export_job_listings_excel(request):
    # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Job Listings'

    # Write the headers to the Excel file
    headers = ['Applicant Name', 'Address', 'Email', 'Phone Number', 'Age', 'Gender', 'Skills', 'Education', 'Experience', 'Resume Link']
    sheet.append(headers)

    # Apply bold style to headers
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    # Get the search query if any
    query = request.GET.get('q', '')
    if query:
        applications = Application.objects.filter(applicant_name__icontains=query)
    else:
        applications = Application.objects.all()

    # Write application data to Excel
    for application in applications:
        row = [
            application.applicant_name,
            application.address,
            application.email,
            application.phone_number,
            application.age,
            application.gender,
            application.skills,
            application.education,
            application.experience
        ]
        if application.resume_link:
            # Add resume link as a clickable hyperlink
            row.append(f'=HYPERLINK("{application.resume_link}", "Download Resume")')
        else:
            row.append('No Resume')

        sheet.append(row)

    # Create the HttpResponse object with the appropriate Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="job_listings.xlsx"'

    # Save the workbook to the response
    workbook.save(response)

    return response



#----------------------------------------------------Upload Excel File and Send Interview Invites---------------

@login_required
def upload_excel(request):
    if request.method == 'POST':
        # Extract interview date and time from the POST request
        interview_date = request.POST.get('date', 'Not specified')
        interview_time = request.POST.get('time', 'Not specified')

        # Extract the uploaded file
        excel_file = request.FILES.get('file')
        if not excel_file:
            return HttpResponse("No file uploaded.", status=400)

        # Read the Excel file
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return HttpResponse(f"Error reading the Excel file: {e}", status=400)

        # Ensure there's a column named 'email' and 'name'
        if 'email' not in df.columns or 'name' not in df.columns:
            return HttpResponse("No 'email' or 'name' column found in the Excel sheet.", status=400)

        # Send emails
        for index, row in df.iterrows():
            email = row['email']
            name = row['name']  # Extract 'name' from the row
            email_body = f"""Dear {name},

We are pleased to inform you that you have been shortlisted for an interview with our company.

You have an interview scheduled on {interview_date} at {interview_time}.
Please reply to this email to confirm your availability.

Best regards,
SkS Software"""

            try:
                email_message = EmailMessage(
                    subject="Interview Invitation",
                    body=email_body,
                    from_email='skssoftwaretech@gmail.com',  # Replace with your email
                    to=[email]
                )
                email_message.send()
            except Exception as e:
                return HttpResponse(f"Error sending email to {email}: {e}", status=500)

        return HttpResponse("Emails sent successfully.")

    return render(request, 'job/upload.html')

#------------------------------------------------user profile--------------------------

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'job/user_profile.html', {'form': form})

@login_required
def profile_update(request):
     if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Adjust the redirect URL as needed
     else:
        form = UserProfileForm(instance=request.user)
    
     return render(request, 'job/user_update.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import JobPosting, Application

def job_list(request):
    job_postings = JobPosting.objects.all()
    show_applicants = False
    applicants = []
    job_id = request.POST.get('job_id')

    if job_id and request.method == 'POST':
        job = get_object_or_404(JobPosting, id=job_id)
        applicants = Application.objects.filter(job_posting=job)
        show_applicants = True
    
    context = {
        'job_postings': job_postings,
        'show_applicants': show_applicants,
        'applicants': applicants,
    }
    
    return render(request, 'job/show_applicants.html', context)

def view_applicants(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    applicants = Application.objects.filter(job_posting=job)
    
    context = {
        'job': job,
        'applicants': applicants,
        'show_applicants': True,
    }
    
    return render(request, 'job/show_applicants.html', context)

