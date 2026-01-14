from django.db import models
from django.db import transaction
from django.db.models import F, Sum
from decimal import Decimal

class SalCustomers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarz")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    class Meta: 
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"

    def __str__(self):
        return self.name
    
class SalSuppliers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Telefon raqam")
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarz")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    class Meta: 
        verbose_name = "Yetkazib beruvchi"
        verbose_name_plural = "Yetkazib beruvchilar"

    def __str__(self):
        return self.name
    

class SalProducts(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")

    class Meta: 
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return self.name
    
class SalPurchases(models.Model):
    supplier = models.ForeignKey(SalSuppliers, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi")
    product = models.CharField(max_length=100, verbose_name="Mahsulot nomi")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    is_debt = models.BooleanField(default=False, verbose_name="Qarzdorlik")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan sana")

    class Meta: 
        verbose_name = "Xarid"
        verbose_name_plural = "Xaridlar"

    def __str__(self):
        return f"{self.product} purchased on {self.purchase_date}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
            if self.pk:
                old = SalPurchases.objects.select_for_update().get(pk=self.pk)

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

class SalSales(models.Model):
    customer = models.ForeignKey(SalCustomers, on_delete=models.CASCADE, verbose_name="Mijoz")
    product = models.ForeignKey(SalProducts, on_delete=models.CASCADE, verbose_name="Mahsulot nomi")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    is_debt = models.BooleanField(default=False, verbose_name="Qarzdorlik")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotilgan sana")

    class Meta: 
        verbose_name = "Sotuv"
        verbose_name_plural = "Sotuvlar"

    def __str__(self):
        return f"{self.product.name} sold to {self.customer.name}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
            if self.pk:
                old = SalSales.objects.select_for_update().get(pk=self.pk)

                if old.is_debt and old.customer:
                    old.customer.debt = F('debt') - old.price
                    old.customer.save(update_fields=['debt'])

            if self.is_debt and self.customer:
                self.customer.debt = F('debt') + self.price
                self.customer.save(update_fields=['debt'])

            super().save(*args, **kwargs)
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
            if self.is_debt and self.customer:
                self.customer.debt = F('debt') - self.price
                self.customer.save(update_fields=['debt'])

            super().delete(*args, **kwargs)

class SalExpenses(models.Model):
    expense_choice = [
         ('Ishchi oyligi', "Ishchi oyligi"),
         ('Texnika ta\'mirlash', "Texnika ta'mirlash"),
         ('Oziq-ovqat', "Oziq-ovqat"),
         ('Elektr energiyasi', "Elektr energiyasi"),
         ('Soliq', "Soliq"),
         ('internet', "Internet"),
         ('Arenda', "Arenda"),
     ]
    name = models.CharField(max_length=100, choices=expense_choice, verbose_name="Xarajat turi")
    worker = models.CharField(max_length=100, verbose_name="Xodim ismi", default="Noma'lum")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Xarajat miqdori")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    expense_date = models.DateTimeField(auto_now_add=True, verbose_name="Xarajat sanasi")

    class Meta: 
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"

    def __str__(self):
        return self.name
    
class SalPaymentDebts(models.Model):
    type_choice = [
         ('Qarz undirish', "Qarz undirish"),
        ('Qarz to\'lash', "Qarz to'lash"),
     ]
    payment_type = models.CharField(max_length=50, choices=type_choice, verbose_name="To'lov turi")
    supplier = models.ForeignKey(SalSuppliers, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi", null=True, blank=True)
    customer = models.ForeignKey(SalCustomers, on_delete=models.CASCADE, verbose_name="Mijoz", null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="To'langan summa")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="To'lov sanasi")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    class Meta: 
        verbose_name = "Qarz To'lovi"
        verbose_name_plural = "Qarz To'lovlari"

    def __str__(self):
        return f"Payment of {self.amount_paid} by "
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk:
            old = SalPaymentDebts.objects.select_for_update().get(pk=self.pk)

            # 🔁 OLD holatni to‘liq BEKOR qilish
            if old.payment_type == 'Qarz undirish' and old.customer:
                old.customer.debt = F('debt') + old.amount_paid
                old.customer.save(update_fields=['debt'])

            elif old.payment_type == "Qarz to'lash" and old.supplier:
                old.supplier.debt = F('debt') + old.amount_paid
                old.supplier.save(update_fields=['debt'])

        # ➕ NEW holatni qo‘llash
        if self.payment_type == 'Qarz undirish' and self.customer:
            self.customer.debt = F('debt') - self.amount_paid
            self.customer.save(update_fields=['debt'])

        elif self.payment_type == "Qarz to'lash" and self.supplier:
            self.supplier.debt = F('debt') - self.amount_paid
            self.supplier.save(update_fields=['debt'])

        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):

        # DELETE → old holatni qaytarish
        if self.payment_type == 'Qarz undirish' and self.customer:
            self.customer.debt = F('debt') + self.amount_paid
            self.customer.save(update_fields=['debt'])

        elif self.payment_type == "Qarz to'lash" and self.supplier:
            self.supplier.debt = F('debt') + self.amount_paid
            self.supplier.save(update_fields=['debt'])

        super().delete(*args, **kwargs)

class SalMonthlyReports(models.Model):
    months = [
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
    month = models.CharField(max_length=20, choices=months, verbose_name="Hisobot")
    from_date = models.DateTimeField(verbose_name="Boshlanish sanasi")
    to_date = models.DateTimeField(verbose_name="Tugash sanasi")

    total_purchases = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami xaridlar")
    total_sales = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami sotuvlar")
    total_expenses = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami xarajatlar")
    total_customer_debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Haqlarimiz")
    total_supplier_debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarzlarimiz")
    net_profit = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Sof foyda")

    class Meta:
        verbose_name = "Oylik Hisobot"
        verbose_name_plural = "Oylik Hisobotlar"

    @transaction.atomic
    def save(self, *args, **kwargs):
        ZERO = Decimal('0')

        self.total_sales = (
            SalSales.objects
            .filter(sale_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum(F('price') * F('quantity')))['total'] or ZERO
        )

        self.total_purchases = (
            SalPurchases.objects
            .filter(purchase_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum(F('price') * F('quantity')))['total'] or ZERO
        )

        self.total_expenses = (
            SalExpenses.objects
            .filter(expense_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('amount'))['total'] or ZERO
        )

        self.total_supplier_debt = (
            SalSuppliers.objects.aggregate(total=Sum('debt'))['total'] or ZERO
        )

        self.total_customer_debt = (
            SalCustomers.objects.aggregate(total=Sum('debt'))['total'] or ZERO
        )

        self.net_profit = (
            self.total_sales
            - self.total_purchases
            - self.total_expenses
        )

        super().save(*args, **kwargs)

