from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import User, Ticket, Staff


from django.shortcuts import render
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from .models import User, Ticket  # adjust import as needed

def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        user_obj = None
        ticket_obj = None

        if name and email and number:
            user_obj, _ = User.objects.get_or_create(
                name=name,
                email=email,
                number=number,
                defaults={'created_at': timezone.now()}
            )

        if user_obj and title and description:
            ticket_obj, _ = Ticket.objects.get_or_create(
                user=user_obj,
                title=title,
                description=description,
                image=image,
                defaults={'created_at': timezone.now()}
            )


            # Build ticket detail URL
            ticket_url = request.build_absolute_uri(reverse('ticket_details', args=[ticket_obj.pk]))


            # Send email
            subject = "🎫 Ticket Created Successfully"
            message = f"""
                Hi {user_obj.name},
                
                Your ticket has been created successfully.
                
                📌 Title: {ticket_obj.title}
                📝 Description: {ticket_obj.description}
                
                You can view your ticket here:
                {ticket_url}
                
                Thanks,
                Support Team
                """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_obj.email])

            # Success message
            messages.success(request, f"{user_obj.name}, your ticket '{ticket_obj.title}' has been created successfully!")

        return render(request, 'index.html', {'user': user_obj, 'ticket': ticket_obj})

    return render(request, 'index.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Message
from django.utils import timezone

def ticket_details(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        image = request.FILES.get('image')

        # Detect sender: Staff or User
        staff_id = request.session.get('staff_id')
        if staff_id:
            staff = Staff.objects.get(id=staff_id)
            sender_name = staff.name
            sender_type = 'staff'
        else:
            sender_name = ticket.user.name
            sender_type = 'user'

        if message_text and sender_name:
            Message.objects.create(
                ticket=ticket,
                sender_name=sender_name,
                sender_type=sender_type,
                message=message_text,
                image=image,
                datetime=timezone.now()
            )
            return redirect('ticket_details', id=ticket.id)

    # Send sender type & name to template
    staff_id = request.session.get('staff_id')
    context = {
        'ticket': ticket,
        'current_user_name': ticket.staff.name if staff_id else ticket.user.name,
        'current_user_type': 'staff' if staff_id else 'user',
        'is_staff': bool(staff_id),
    }
    return render(request, 'ticket_details.html', context)





def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        number = request.POST.get('number')

        try:
            staff = Staff.objects.get(email=email, number=number)
            request.session['staff_id'] = staff.id  # Save session
            return redirect('staff_dashboard')
        except Staff.DoesNotExist:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'staff_login.html')

def staff_dashboard(request):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('staff_login')

    staff = get_object_or_404(Staff, id=staff_id)
    tickets = Ticket.objects.all().order_by('-created_at')
    total_tickets = tickets.count()
    resolved_count = tickets.filter(status='RESOLVED').count()
    assigned_to_me = tickets.filter(staff=staff).count()

    return render(request, 'staff_dashboard.html', {
        'staff': staff,
        'tickets': tickets,
        'total_tickets': total_tickets,
        'resolved_count': resolved_count,
        'assigned_to_me': assigned_to_me,
    })


def assign_ticket(request, ticket_id):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('staff_login')

    ticket = get_object_or_404(Ticket, id=ticket_id)
    staff = get_object_or_404(Staff, id=staff_id)

    ticket.staff = staff
    ticket.status = 'IN_PROGRESS'
    ticket.save()

    return redirect('staff_dashboard')


from django.shortcuts import render, redirect
from .models import Staff
from django.contrib import messages

def staff_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        designation = request.POST.get('designation')

        if name and email and number and designation:
            Staff.objects.create(
                name=name,
                email=email,
                number=number,
                designation=designation
            )
            messages.success(request, 'Staff created successfully.')
            return redirect('staff_dashboard')

    return render(request, 'staff_create.html')


from django.http import JsonResponse
import json





@csrf_exempt
def update_ticket_status(request, ticket_id):
    if request.method == 'POST' and request.session.get('staff_id'):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status in dict(Ticket.STATUS_CHOICES).keys():
            ticket.status = new_status
            ticket.save()
            return JsonResponse({
                "success": True,
                "status_display": ticket.get_status_display()
            })

    return JsonResponse({"success": False}, status=400)





