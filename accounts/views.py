from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import GuideForm, BookingForm, ReplyForm, AvailabilityForm
from travello.models import Guide , Destination, Contact, Booking, Message
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from django.contrib import messages
def login(request):
     if request.method == "POST":
         username = request.POST["username"]
         password = request.POST["password"]

         user = authenticate(username=username, password=password)
         if user is not None:
             auth_login(request, user)

             try:
                 guide = Guide.objects.get(username=request.user.username)
             except Guide.DoesNotExist:
                 unread_messages = Message.objects.filter(recipient__username=request.user.username, read=False)
                 if unread_messages:
                    message_data = []
                    for message in unread_messages:
                        message_data.append({
                            'guide_name': message.sender.first_name,
                            'content': message.content,
                            'message_id': message.id
                            })
                    request.session['unread_messages'] = message_data
                 else:
                     if 'unread_messages' in request.session:
                       del request.session['unread_messages']
                 reply_messages = Message.objects.filter(recipient__username=request.user.username, read=False).exclude(sender__username=request.user.username)
                 if reply_messages:
                    reply_message_data = []
                    for message in reply_messages:
                        reply_message_data.append(
                             {
                                'guide_name': message.sender.first_name,
                                'content': message.content,
                                'message_id' : message.id
                            }
                        )
                    request.session['reply_message'] = reply_message_data
                 else:
                    if 'reply_message' in request.session:
                        del request.session['reply_message']

             return redirect(reverse("dashboard"))
         else:
             messages.error(request, "invalid credentials...")
    
     # Clear messages including the session messages
     storage = messages.get_messages(request)
     for _ in storage:
          pass
     return render(request, "login.html")

def register(request):
 if request.method == "POST":
     first_name = request.POST["first_name"]
     last_name = request.POST["last_name"]
     username = request.POST["username"]
     email = request.POST["email"]
     password1 = request.POST["password1"]
     password2 = request.POST["password2"]

     if password1 == password2:
         if User.objects.filter(username=username).exists():
             messages.info(request, "username taken...")
             test = User.objects.all()
             print(test)
             return redirect("register")
         elif User.objects.filter(email=email).exists():
             messages.info(request, "email taken...")
             return redirect("register")
         else:
             user = User.objects.create_user(
                 username=username,
                 password=password1,
                 email=email,
                 first_name=first_name,
                 last_name=last_name,
             )
             user.save()
             messages.info(request, "User Created...")
             return redirect("dashboard")
     else:
         messages.info(request, "Password Not Matched...")
         return redirect("dashboard")
     return redirect("/")
 else:
     return render(request, "register.html")


def logout(request):
    auth_logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

def contact(request):
 if request.method == 'POST':
     name = request.POST.get('name')
     email = request.POST.get('email')
     subject = request.POST.get('subject')
     message = request.POST.get('message')

    
     Contact.objects.create(
         name=name,
         email=email,
         subject=subject,
         message=message,
     )

     messages.success(request, 'Your message has been sent successfully!')

   
     return redirect('contact') 

 return render(request, 'contact.html')  

def about(request):
 return render(request, "about.html")
from django.shortcuts import render, get_object_or_404
from travello.models import Booking, Message
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user_bookings = Booking.objects.filter(user=request.user)
    unread_messages = request.session.get('unread_messages', [])
    reply_message = request.session.get('reply_message', [])

    if unread_messages or reply_message:
        if 'reply_message' in request.session:
           del request.session['reply_message']
        if 'unread_messages' in request.session:
           del request.session['unread_messages']
        return render(request, 'dashboard.html', {'user_bookings': user_bookings, 'unread_messages': unread_messages, 'reply_message': reply_message})
        
    return render(request, 'dashboard.html', {'user_bookings': user_bookings})
def news(request):
 guides = Guide.objects.all()
 return render(request, "news.html", {"guides":guides})


def destinations(request):
    destinations = Destination.objects.all()
    for destination in destinations:
        if destination.list_items:
            destination.list_items = [item.strip() for item in destination.list_items.split(",")]
    return render(request, 'destinations.html', {'destinations': destinations})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def mark_messages_as_read(request):
    if request.method == 'POST' and request.user.is_authenticated:
        messages = Message.objects.filter(recipient__username = request.user.username, read=False)
        for message in messages:
            message.read = True
            message.save()
        return JsonResponse({'status':'success'})
    return JsonResponse({'status': 'error'}, status = 400)

def guide(request):
    if request.method == "POST":
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.save()
            request.session['guide_id'] = guide.id
            return redirect(reverse("guide_dashboard",kwargs={'guide_id':guide.id}))
    else:
        form = GuideForm()
    return render(request, "guideregistration.html", {"form": form})

from datetime import datetime, timedelta
from calendar import monthrange


def guide_details(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    today = datetime.today()
    availabilities = guide.availabilities.all()
    cal_data = []
    for i in range(0, 2):
        month_date = today.replace(month=today.month + i)
        year = month_date.year
        month = month_date.month

        num_days = monthrange(year, month)[1]
        first_day_of_month = datetime(year, month, 1).weekday()
        days = []
        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            is_available = False
            for availability in availabilities:
              if availability.start_date.date() <= date.date() <= availability.end_date.date():
                  is_available = True
                  break
            days.append({
                    'date': date,
                    'day': day,
                    'is_available': is_available,
                })
        
        # Calculate range in view
        first_day_range = list(range(first_day_of_month))

        cal_data.append(
            {
                "month_name": month_date.strftime("%B %Y"),
                "first_day_range": first_day_range,
                "days": days,
            }
        )

    return render(request, "guide_details.html", {"guide": guide, 'calendar_data': cal_data})


@login_required
def contact_guide(request, guide_id):
    guide = get_object_or_404(Guide, pk=guide_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            message_content = request.POST.get('message')
            booking = Booking(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                preferred_date=form.cleaned_data['preferred_date'],
                party_size=form.cleaned_data['party_size'],
                message=message_content,
                accept_terms=form.cleaned_data['accept_terms'],
                accept_marketing_emails=form.cleaned_data['accept_marketing_emails'],
                guide=guide,
                user=request.user
            )
            booking.save()
            # Retrieve the user associated with the guide
            try:
                 recipient_user = User.objects.get(username = guide.username)
            except User.DoesNotExist:
                messages.error(request, "The user associated with the guide does not exist")
                return redirect(reverse('index'))
            Message.objects.create(
                sender=request.user,
                recipient=recipient_user,  # Use the User instance of the guide
                content=message_content,
                booking=booking
            )
            message = "Thank you for contacting " + guide.first_name + " " + guide.last_name + ". We will reach out to you soon."
            messages.success(request, message)
            return redirect(reverse('index'))
    else:
        form = BookingForm()
    return render(request, 'message.html', {'form': form, 'guide':guide})

@login_required
def edit_booking(request, booking_id):
    try:
      booking = get_object_or_404(Booking, pk=booking_id)
    except Booking.DoesNotExist:
     messages.error(request, "Booking Not found.")
     return redirect(reverse("dashboard"))
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking) 
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect(reverse('dashboard'))
    else:
        form = BookingForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


@login_required
def delete_booking(request, booking_id):
 booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
 if request.method == 'POST':
     booking.delete()
     messages.success(request, "Booking deleted successfully.")
     return redirect(reverse('dashboard'))
 return render(request, 'delete_booking.html', {'booking': booking})

@login_required
def reject_booking(request, booking_id):
    # Get the booking
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Get the guide associated with the logged-in user
    try:
        guide = Guide.objects.get(username=request.user.username)
    except Guide.DoesNotExist:
        messages.error(request, "You are not authorized to reject this booking.")
        return redirect(reverse('guide_dashboard', kwargs={'guide_id': request.user.id}))
    
    # Verify this booking belongs to this guide
    if booking.guide != guide:
        messages.error(request, "You are not authorized to reject this booking.")
        return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id}))
    
    if request.method == 'POST':
        # Update the booking status to rejected
        booking.status = 'rejected'
        booking.save()
        
        messages.success(request, "Booking has been rejected successfully.")
        return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id}))
    
    context = {
        'booking': booking,
        'guide_id': guide.id  # Add guide_id to context
    }
    return render(request, 'reject_booking.html', context)


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.urls import reverse
from travello.models import Guide
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def guide_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            guide = Guide.objects.get(username=username)

            if check_password(password, guide.password):  # Correct password
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': guide.email,
                        'first_name': guide.first_name,
                        'last_name': guide.last_name
                    }
                )
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    request.session['guide_id'] = guide.id
                    storage = messages.get_messages(request)
                    for _ in storage:
                         pass
                    return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id})) # Redirect here
            else:
                messages.error(request, 'Invalid credentials.')

        except Guide.DoesNotExist:
            messages.error(request, 'Guide not found.')

    return render(request, 'login.html')
def guide_dashboard(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    try:
        user = User.objects.get(username=guide.username)
    except User.DoesNotExist:
        messages.error(request, "The user associated with the guide does not exist")
        return redirect(reverse('index'))

    bookings = Booking.objects.filter(guide=guide).order_by('-booking_date')
    
    # Fetch messages where the recipient is the guide's user account
    all_booking_messages = []
    for booking in bookings:
        booking_messages = Message.objects.filter(booking=booking, recipient = user).order_by('-timestamp')
        all_booking_messages.extend(booking_messages)
    
    availabilities = guide.availabilities.all()

    if request.method == "POST":
         form = AvailabilityForm(request.POST)
         if form.is_valid():
            
             if availabilities:
                 availability = availabilities.first()
                 availability.start_date = form.cleaned_data['start_date']
                 availability.end_date = form.cleaned_data['end_date']
                 availability.save()
             else:
                  availability = form.save(commit=False)
                  availability.guide = guide
                  availability.save()

             return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id}))

    else:
        form = AvailabilityForm()

    return render(request, 'guide_dashboard.html', {'guide': guide, 'messages': all_booking_messages,
                                                     'bookings': bookings, "form":form,
                                                     'availabilities': availabilities})
@login_required
def guide_message_reply(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    try:
        guide = Guide.objects.get(username=request.user.username)
    except Guide.DoesNotExist:
        messages.error(request, "You are not logged in or your session has expired. Please login again.")
        return redirect(reverse("guide_login"))
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data['reply']

            # Get the User related to the guide
            user = User.objects.get(username=guide.username)

            if isinstance(message.sender, User):
                recipient_user = message.sender
            elif isinstance(message.sender, Guide):
                try:
                   recipient_user = User.objects.get(username=message.sender.username)
                except User.DoesNotExist:
                     messages.error(request, "The user that sent the message does not have a user profile")
                     return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id}))
            else:
                messages.error(request, "An unexpected error has occurred please contact the support team")
                return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id}))


            #Update the booking status to confirmed
            booking = message.booking
            if booking.status == 'pending':
                  booking.status = 'confirmed'
                  booking.save()


            Message.objects.create(
                sender=user,
                recipient=recipient_user,
                content=reply_text,
                booking=message.booking
            )
            request.session['reply_message'] = {
                'guide_name': guide.first_name,
                'content': reply_text,
                'message_id': message.id,
            }

            return redirect(reverse('guide_dashboard', kwargs={'guide_id': guide.id}))
    else:
        form = ReplyForm()
    return render(request, 'reply.html', {'form': form, 'message': message, 'guide':guide})



def guide_logout(request):
    auth_logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    return redirect('login')