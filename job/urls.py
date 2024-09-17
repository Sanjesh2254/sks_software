from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/',views.login_view, name='login'),
    path("superhome/", views.superhome, name='superhome'),
    path("job_posting/", views.job_posting, name='job_posting'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='Contact'),  
    path('categories/', views.category_create, name='category_create'),
    path('job/delete/<int:job_id>/', views.delete_job_posting, name='delete_job_posting'),
    path('jobs/<int:job_id>/apply/', views.apply, name='apply'),

    path('applylisting/<int:job_id>/', views.applylisting, name='applylisting'),

    path('applylisting/delete/<int:id>/', views.applylisting, name='delete_application'),
    path('applylisting/delete_all/', views.applylisting, name='delete_all_applications'),
    path('export/jobs/excel/', views.export_job_listings_excel, name='export_job_listings_excel'),
    path('register/', views.register, name='register'),
    path('edit/<int:pk>/', views.edit_job_posting, name='edit_job_posting'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    #path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),  # Delete single applicant
    #path('delete_all_applications/', views.delete_all_applications, name='delete_all_applications'),
    #path('jobs/<int:pk>/show/',views.show_job_posting, name='show_job_posting'),
    path('view_applicants/<int:job_id>/',views.view_applicants, name='view_applicants'),
    #path('application-details/<int:job_id>/', views.application_details, name='application_details'),



   

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
