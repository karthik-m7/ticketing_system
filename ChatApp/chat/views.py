from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import User, Ticket, Staff


def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if name and email and number:
            user_obj, _ = User.objects.get_or_create(
                name=name,
                email=email,
                number=number,
                defaults={'created_at': timezone.now()}  # Only set created_at if new user
            )

        if title and description:
            ticket_obj, _ = Ticket.objects.get_or_create(
                user=user_obj,
                title=title,
                description=description,
                image=image,
                defaults={'created_at': timezone.now()}
            )

            # Success Message
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
        'current_user_type': 'staff' if staff_id else 'user'
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







