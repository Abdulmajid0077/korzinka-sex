from django.db import models
from django.db import transaction
from django.db.models import F, Sum
from decimal import Decimal

class SProducts(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")

    def __str__(self):
        return self.name

class SSupplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    debt = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Qarz", default=0)
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    def __str__(self):
        return self.name

class SPurchases(models.Model):
    supplier = models.ForeignKey(SSupplier, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi")
    product = models.ForeignKey(SProducts, on_delete=models.CASCADE, verbose_name="Mahsulot nomi")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    is_debt = models.BooleanField(default=False, verbose_name="Qarzdorlik")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan sana")

    def __str__(self):
        return f"{self.product.name} from {self.supplier.name}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):

            if self.pk:
                old = SPurchases.objects.select_for_update().get(pk=self.pk)

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

class SCustomers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    debt = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Qarz miqdori", default=0)
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    def __str__(self):
        return self.name

class SSales(models.Model):
    customer = models.ForeignKey(SCustomers, on_delete=models.CASCADE, verbose_name="Xaridor")
    product = models.ForeignKey(SProducts, on_delete=models.CASCADE, related_name='s_sales', verbose_name="Mahsulot")
    quantity = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Narxi")
    is_debt = models.BooleanField(default=False, verbose_name="Qarzdorlik")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotilgan sana")

    def __str__(self):
        return f"{self.product.name} sale"
    
    @transaction.atomic
    def save(self, *args, **kwargs):

            if self.pk:
                old = SSales.objects.select_for_update().get(pk=self.pk)

                if old.is_debt and old.customer:
                    old.customer.debt -= old.price
                    old.customer.save()

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

    
class SExpenseMachine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Mashina nomi")
    cost = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Harajat miqdori")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    expense_date = models.DateTimeField(auto_now_add=True, verbose_name="Harajat sanasi")

    def __str__(self):
        return self.name
    
class SExpenses(models.Model):
    expense_choice = [
        ('Ishchi oyligi', 'Ishchi oyligi'),
        ('Elektr energiyasi', 'Elektr energiyasi'),
        ('Arenda', 'Arenda'),
        ('Suv to\'lovi', 'Suv to\'lovi'),
        ('soliq', 'Soliq'),
        ('boshqa', 'Boshqa'),
    ]
    expense = models.CharField(max_length=50, choices=expense_choice, verbose_name="Harajat turi")
    worker = models.CharField(max_length=100, verbose_name="Xodim ismi", default="-")
    cost = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="Harajat miqdori")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")
    expense_date = models.DateTimeField(auto_now_add=True, verbose_name="Harajat sanasi")

    def __str__(self):
        return self.worker
    
class SPaymentDebt(models.Model):
    payment_choice = [
        ('Qarz undirish', 'Qarz undirish'),
        ('Qarzni to\'lash', 'Qarzni to\'lash'),
    ]
    customer = models.ForeignKey(SCustomers, on_delete=models.CASCADE, verbose_name="Xaridor", null=True, blank=True)
    supplier = models.ForeignKey(SSupplier, on_delete=models.CASCADE, verbose_name="Yetkazib beruvchi", null=True, blank=True)
    payment_type = models.CharField(max_length=50, choices=payment_choice, verbose_name="To'lov turi")
    amount = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="To'langan summa")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="To'lov sanasi")
    info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumot")

    def __str__(self):
        return f"Payment from "
    
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

class SMonthlyReport(models.Model):
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
    total_expense_machine = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Jami stanog xarajatlari")
    total_customer_debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Haqlarimiz")
    total_supplier_debt = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Qarzlarimiz")   
    net_profit = models.DecimalField(max_digits=25, decimal_places=2, default=0, verbose_name="Sof foyda")

    @transaction.atomic
    def save(self, *args, **kwargs):
        ZERO = Decimal('0')

        self.total_sales = (
            SSales.objects
            .filter(sale_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('price'))['total'] or ZERO
        )

        self.total_purchases = (
            SPurchases.objects
            .filter(purchase_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('price'))['total'] or ZERO
        )

        self.total_expenses = (
            SExpenses.objects
            .filter(expense_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('cost'))['total'] or ZERO
        )

        self.total_expense_machine = (
            SExpenseMachine.objects
            .filter(expense_date__range=(self.from_date, self.to_date))
            .aggregate(total=Sum('cost'))['total'] or ZERO
        )

        self.total_customer_debt = (
            SCustomers.objects.aggregate(total=Sum('debt'))['total'] or ZERO
        )

        self.total_supplier_debt = (
            SSupplier.objects.aggregate(total=Sum('debt'))['total'] or ZERO
        )

        self.net_profit = (
            self.total_sales - self.total_purchases - self.total_expenses - self.total_expense_machine 
        )

        super().save(*args, **kwargs)

