
from django.urls import path
from . import views

urlpatterns = [
    # User Authentication URLs (Tourist)
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # General Content URLs
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),


    # Guide Specific URLs (Guide Authentication, Guide Dashboard)
    path('guides/register/', views.guide, name='guide'),  
    path('guides/login/', views.guide_login, name='guide_login'),  
    path('guides/<int:guide_id>/dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('guides/logout/', views.guide_logout, name='guide_logout'),
    path('guides/message/<int:message_id>/reply/', views.guide_message_reply, name='guide_message_reply'),
    

    # News Section URLs (List and Detail)
    path('news/', views.news, name='news'),
    path('news/<int:guide_id>/', views.guide_details, name='guide_details'),

    # Dashboard URLs (User Bookings)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('dashboard/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('dashboard/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

    # Booking URLs
    path('contact_guide/<int:guide_id>/', views.contact_guide, name='contact_guide'),
    path('mark-messages-as-read/', views.mark_messages_as_read, name='mark_messages_as_read'),

]