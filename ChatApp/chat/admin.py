from django.contrib import admin

# Register your models here.
from .models import User,Ticket,Staff,Message

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Staff)
admin.site.register(Message)

