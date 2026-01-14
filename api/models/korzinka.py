from django.db import models
from django.db import transaction
from django.db.models import F

class Investors(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    age = models.IntegerField(verbose_name="Yosh")
    invest = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Sarmoya miqdori")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    currency = models.CharField(max_length=3, choices=[('UZS', 'UZS'), ('USD', 'USD')], default='UZS', verbose_name="Valyuta")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investorlar"

class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

class Suppliers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarz")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Yetkazib beruvchi"
        verbose_name_plural = "Yetkazib beruvchilar"
    
class Customers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarz")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Xaridor"
        verbose_name_plural = "Xaridorlar"
    
class Purchases(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi")
    product_name = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    is_debt = models.BooleanField(default=False, verbose_name="Qarzdorlik")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan sana")

    def __str__(self):
        return f"{self.product_name} from {self.supplier.name}"
    
    class Meta:
        verbose_name = "Xarid"
        verbose_name_plural = "Xaridlar"
    
    @transaction.atomic
    def save(self, *args, **kwargs):

            if self.pk:
                old = Purchases.objects.select_for_update().get(pk=self.pk)

                if old.is_debt and old.supplier:
                    old.supplier.debt = F('debt') - old.price
                    old.supplier.save(update_fields=['debt'])

            if self.is_debt and self.supplier:
                self.supplier.debt = F('debt') + self.price
                self.supplier.save(update_fields=['debt'])

            super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):

            if self.is_debt and self.supplier:
                self.supplier.debt = F('debt') - self.price
                self.supplier.save(update_fields=['debt'])

            super().delete(*args, **kwargs)
    
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
    
    class Meta:
        verbose_name = "Sotuv"
        verbose_name_plural = "Sotuvlar"
    
    @transaction.atomic
    def save(self, *args, **kwargs):

            if self.pk:
                # UPDATE holati
                old = Sales.objects.select_for_update().get(pk=self.pk)

                # 1️⃣ Eski qarzni qaytarish (eski customer’dan)
                if old.is_debt and old.customer:
                    old.customer.debt -= old.price
                    old.customer.save()

            # 2️⃣ Yangi qarzni qo‘shish (yangi customer’ga)
            if self.is_debt and self.customer:
                self.customer.debt += self.price
                self.customer.save()

            super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):

            if self.is_debt and self.customer:
                self.customer.debt -= self.price
                self.customer.save()

            super().delete(*args, **kwargs)

    
class Expenses(models.Model):
    CHOICES = [
        ('Oylik', 'Oylik'),
        ('Oziq-ovqat', 'Oziq-ovqat'),
        ('Soliq', 'Soliq'),
        ('Arenda ', 'Arenda'),
        ('Elektr', 'Elektr'),
        ('Internet', 'Internet'),
    ]
    worker_name = models.CharField(max_length=100, default="-", verbose_name="Xodim ismi")
    expense_type = models.CharField(max_length=20, choices=CHOICES, verbose_name="Harajat turi")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Summasi")
    expense_date = models.DateTimeField(auto_now_add=True, verbose_name="Harajat sanasi")

    class Meta:
        verbose_name = "Harajat"
        verbose_name_plural = "Harajatlar"

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

    class Meta:
        verbose_name = "Stanoq Harajati"
        verbose_name_plural = "Stanoq Harajatlari"
        
class PaymentDebt(models.Model):
    payment_choice = [
        ('Qarz undirish', 'Qarz undirish'),
        ('Qarzni to\'lash', 'Qarzni to\'lash'),
    ]
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Xaridor", null=True, blank=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi", null=True, blank=True)
    payment_type = models.CharField(max_length=50, choices=payment_choice, verbose_name="To'lov turi")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="To'langan summa")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="To'lov sanasi")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    class Meta:
        verbose_name = "Qarz To'lovi"
        verbose_name_plural = "Qarz To'lovlari"

    def __str__(self):
        return f"Payment from {self.customer.name}"
    
    def save(self, *args, **kwargs):
        is_update = self.pk is not None

        old = None
        if is_update:
            old = self.__class__.objects.get(pk=self.pk)

        # ==== CUSTOMER ====
        if self.customer:
            if is_update and old.customer == self.customer:
                # eski ta'sirni qaytarish
                if old.payment_type == 'Qarz undirish':
                    self.customer.debt += old.amount

            if self.payment_type == 'Qarz undirish':
                self.customer.debt -= self.amount

            self.customer.save()

        # ==== SUPPLIER ====
        if self.supplier:
            if is_update and old.supplier == self.supplier:
                if old.payment_type == "Qarzni to'lash":
                    self.supplier.debt += old.amount

            if self.payment_type == "Qarzni to'lash":
                self.supplier.debt -= self.amount

            self.supplier.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.customer:
            if self.payment_type == 'Qarz undirish':
                self.customer.debt += self.amount
            self.customer.save()

        if self.supplier:
            if self.payment_type == "Qarzni to'lash":
                self.supplier.debt += self.amount
            self.supplier.save()

        super().delete(*args, **kwargs)

from django.db import models, transaction
from django.db.models import Sum
from decimal import Decimal

class MonthlyReport(models.Model):
    choise_month = [
        ('Yanvar', 'Yanvar'),
        ('Fevral', 'Fevral'),
        ('Mart', 'Mart'),
        ('Aprel', 'Aprel'),
        ('May', 'May'),
        ('Iyun', 'Iyun'),
        ('Iyul', 'Iyul'),
        ('Avgust', 'Avgust'),
        ('Sentabr', 'Sentabr'),
        ('Oktabr', 'Oktabr'),
        ('Noyabr', 'Noyabr'),
        ('Dekabr', 'Dekabr'),
    ]

    month = models.CharField(max_length=20, choices=choise_month, verbose_name="Hisobot")
    from_date = models.DateTimeField(verbose_name="Boshlanish sanasi")
    to_date = models.DateTimeField(verbose_name="Tugash sanasi")

    # 📊 HISOBOT NATIJALARI
    total_purchases = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami xaridlar")
    total_sales = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami sotuvlar")
    total_expenses = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami xarajatlar")
    total_expense_machine = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami stanog xarajatlari")
    total_supplier_debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarzlarimiz")
    total_customer_debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Haqlarimiz")
    net_profit = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Sof foyda")

    class Meta:
        verbose_name = "Oylik Hisobot"
        verbose_name_plural = "Oylik Hisobotlar"

    @transaction.atomic
    def save(self, *args, **kwargs):
        ZERO = Decimal('0')

        self.total_sales = (
            Sales.objects
            .filter(sale_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('price'))
            ['total'] or ZERO
        )

        self.total_purchases = (
            Purchases.objects
            .filter(purchase_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('price'))
            ['total'] or ZERO
        )

        self.total_expenses = (
            Expenses.objects
            .filter(expense_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('amount'))
            ['total'] or ZERO
        )

        self.total_expense_machine = (
            ExpenseMachine.objects
            .filter(expense_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('amount'))
            ['total'] or ZERO
        )

        self.total_supplier_debt = (
            Suppliers.objects.aggregate(total=Sum('debt'))['total'] or ZERO
        )

        self.total_customer_debt = (
            Customers.objects.aggregate(total=Sum('debt'))['total'] or ZERO
        )

        self.net_profit = (
            self.total_sales
            - self.total_purchases
            - self.total_expenses
            - self.total_expense_machine
        )

        super().save(*args, **kwargs)


    
