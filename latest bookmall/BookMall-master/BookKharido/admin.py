from django.contrib import admin

# Register your models here.
from BookKharido.models import book_table
from .models import Orders

admin.site.register(book_table)
admin.site.register(Orders)