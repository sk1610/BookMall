from django.db import models
from django.utils import timezone

# Create your models here.

class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    price=models.IntegerField(default=0)
    phone = models.CharField(max_length=111, default="")
    currentdate = models.DateField(default=timezone.now)
    currenttime = models.TimeField(default=timezone.now)


class book_table(models.Model):
    book_id = models.AutoField
    book_name = models.CharField(max_length=100)
    book_price = models.IntegerField(default=0)
    book_image = models.ImageField(upload_to='BookKharido/bookimages',default="")
    book_category = models.CharField(max_length=100,default="")
    book_subcategory = models.CharField(max_length=100,default="")
    book_author = models.CharField(max_length=1000,default="")
    book_quantity = models.IntegerField()

    def __str__(self):
        return self.book_name