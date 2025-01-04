from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image_link = models.URLField(max_length=500, null=True, blank=True, help_text="Link to the book's cover image")
    status =models.BooleanField(default=False, help_text="0=default, 1=hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    isbn = models.CharField(max_length=13, unique=True, null=False, blank=False, help_text="Unique ISBN of the book")
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    publish_year = models.PositiveIntegerField(null=False, blank=False)
    publisher = models.CharField(max_length=255, null=False, blank=False)
    image_link = models.URLField(max_length=500, null=True, blank=True, help_text="Link to the book's cover image")
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, help_text="Rating out of 10.00")
    description = models.TextField(max_length=1000, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    status =models.BooleanField(default=False, help_text="0=default, 1=hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    price = models.FloatField(null=False, blank=False)
    
    
    def __str__(self):
        return self.title
    
    def update_average_rating(self):
        """Cập nhật rating trung bình dựa trên đánh giá của người dùng."""
        avg_rating = self.reviews.aggregate(average=Avg('rating'))['average']
        self.rating = avg_rating if avg_rating is not None else 0
        self.save()

class UserRating(models.Model):
    id_user = models.IntegerField(null=False, blank=False, help_text="ID of the user")
    isbn = models.ForeignKey(Product, to_field='isbn', on_delete=models.CASCADE)  # Tham chiếu qua `isbn`
    user_rating = models.PositiveIntegerField(null=False, blank=False, help_text="Rating given by the user (0-10)")

    def __str__(self):
        return f"User {self.user_id} - {self.book.title} - {self.rating}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatuses = (
        ('Pending','Pending'),
        ('Shipping', 'Shipping'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    
    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)
    
    
    
    