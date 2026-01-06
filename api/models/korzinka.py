from django.db import models

class Investors(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    age = models.IntegerField(verbose_name="Yosh")
    invest = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Sarmoya miqdori")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')], default='UZS', verbose_name="Valyuta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")

    def __str__(self):
        return self.name
    
class Suppliers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarz")

    def __str__(self):
        return self.name
    
class Customers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarz")

    def __str__(self):
        return self.name
    
class Purchases(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi")
    product_name = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan sana")

    def __str__(self):
        return f"{self.product_name} from {self.supplier.name}"
    
class Sales(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Xaridor")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='sales', verbose_name="Mahsulot")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    is_debt = models.BooleanField(default=False, verbose_name="Qarzdorlik")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotilgan sana")

    def __str__(self):
        return f"{self.product.name} to {self.customer.name}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            # UPDATE holati
            old = Sales.objects.get(pk=self.pk)

            # Eski qarzni qaytarib tashlaymiz
            if old.is_debt:
                old.customer.debt -= old.price
                old.customer.save()

        # Yangi qarzni qo‘shamiz
        if self.is_debt:
            self.customer.debt += self.price
            self.customer.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_debt:
            self.customer.debt -= self.price
            self.customer.save()

        super().delete(*args, **kwargs)

    
class Expenses(models.Model):
    CHOICES = [
        ('Oylik', 'Oylik'),
        ('Oziq-ovqat', 'Oziq-ovqat'),
        ('Soliq', 'Soliq'),
        ('Elektr', 'Elektr'),
        ('Internet', 'Internet'),
    ]
    worker_name = models.CharField(max_length=100, default="-", verbose_name="Xodim ismi")
    expense_type = models.CharField(max_length=20, choices=CHOICES, verbose_name="Harajat turi")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Summasi")
    expense_date = models.DateTimeField(auto_now_add=True, verbose_name="Harajat sanasi")

class ExpenseMachine(models.Model):
    CHOICES_TYPE = [
        ('Usta Haqqi', 'Usta Haqqi'),
        ('Kran', 'Kran'),
        ('Qolip Sotib Olish', 'Qolip Sotib Olish'),
    ]
    info = models.TextField(null=True, blank=True, verbose_name="Ma'lumot")
    expense_type = models.CharField(max_length=50, choices=CHOICES_TYPE, verbose_name="Harajat turi")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Summasi")
    expense_date = models.DateTimeField(auto_now_add=True, verbose_name="Harajat sanasi")
        
