from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.humanize.templatetags.humanize import intcomma
from decimal import Decimal
from .models import Investors, Products, Purchases, Sales, Customers, Suppliers, Expenses, ExpenseMachine, PaymentDebt, MonthlyReport
from .models import SProducts, SSupplier, SCustomers, SPurchases,  SSales, SExpenseMachine, SExpenses, SPaymentDebt, SMonthlyReport
from .models import SalCustomers, SalSuppliers, SalProducts, SalPurchases, SalSales, SalPaymentDebts, SalExpenses, SalMonthlyReports
from .models import User

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'phone', 'is_staff', 'is_admin', 'korzinka', 'seriyo', 'salfetka')
    unfoldable_fieldsets = [
        ("General", {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone")}),
        ("Module Permissions", {
            "fields": ("korzinka", "seriyo", "salfetka"),
            "classes": ("collapse",),  # yopiq boshlanadi
        }),
        ("Advanced Permissions", {
            "fields": ("is_active", "is_staff", "is_admin", "groups", "user_permissions"),
            "classes": ("collapse",),
        }),
    ]



@admin.register(Investors)
class InvestorAdmin(ModelAdmin):
    list_display = ('name', 'age', 'phone', 'formatted_invest', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

    fieldsets = (
        ("Investor ma’lumotlari", {
            "fields": ("name", "age", "phone", "invest", "currency"),
        }),
    )

    @admin.display(description="Sarmoya ")
    def formatted_invest(self, obj):
        amount = obj.invest or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        if obj.currency == 'UZS':
            return f"{amount_str} so‘m"
        return f"${amount_str}"
    
@admin.register(Products)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'quantity_format', 'formatted_price')
    search_fields = ('name',)

    fieldsets = (
        ("Mahsulot ma’lumotlari", {
            "fields": ("name", "quantity", "price"),
        }),
    )
    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} dona"
    
    @admin.display(description="Narxi")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"

@admin.register(Sales)
class SaleAdmin(ModelAdmin):
    list_display = ('customer', 'product', 'quantity_format', 'formatted_price', 'is_debt', 'info', 'sale_date')
    search_fields = ('product__name', 'customer__name')
    ordering = ('-sale_date',)

    fieldsets = (
        ("Sotuv ma’lumotlari", {
            "fields": ("customer", "product", "quantity", "price", "is_debt", "info"),
        }),
    )

    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} dona"

    @admin.display(description="To'langan summa")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
        
    
@admin.register(Purchases)
class PurchaseAdmin(ModelAdmin):
    list_display = ('supplier', 'product_name', 'quantity_format', 'formatted_price', 'is_debt', 'info', 'purchase_date')
    search_fields = ('product_name', 'supplier__name')
    ordering = ('-purchase_date',)

    fieldsets = (
        ("Sotib olish ma’lumotlari", {
            "fields": ("supplier", "product_name", "quantity", "price", "is_debt", "info"),
        }),
    )

    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} kg"
    
    @admin.display(description="To'langan summa")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(Customers)
class CustomerAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'form_debt', 'info')
    search_fields = ('name',)

    fieldsets = (
        ("Mijoz ma’lumotlari", {
            "fields": ("name", "phone", "debt", "info"),
        }),
    )

    @admin.display(description="Qarz miqdori")
    def form_debt(self, obj):
        amount = obj.debt or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
        

@admin.register(Suppliers)
class SupplierAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'form_debt', 'info')
    search_fields = ('name',)

    fieldsets = (
        ("Yetkazib beruvchi ma’lumotlari", {
            "fields": ("name", "phone", "debt", "info"),
        }),
    )
    
    @admin.display(description="Qarz miqdori")
    def form_debt(self, obj):
        amount = obj.debt or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(Expenses)
class ExpenseAdmin(ModelAdmin):
    list_display = ('expense_type', 'worker_name', 'form_amount', 'expense_date')
    list_filter = ('expense_type',)
    ordering = ('-expense_date',)
    fieldsets = (
        ("Harajat ", {
            "fields": ("worker_name", "expense_type", "amount"),
        }),
    )
    @admin.display(description="Harajat miqdori")
    def form_amount(self, obj):
        amount = obj.amount or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(ExpenseMachine)
class ExpenseMachineAdmin(ModelAdmin):
    list_display = ('expense_type', 'form_amount', 'info', 'expense_date')
    list_filter = ('expense_type',)
    ordering = ('-expense_date',)
    fieldsets = (
        ("Stanog harajatlari ", {
            "fields": ("expense_type", "amount", "info"),
        }),
    )
    @admin.display(description="Harajat miqdori")
    def form_amount(self, obj):
        amount = obj.amount or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(PaymentDebt)
class PaymentDebtAdmin(ModelAdmin):
    list_display = ('customer', 'supplier', 'payment_type', 'form_amount', 'info', 'payment_date')
    list_filter = ('payment_type',)
    ordering = ('-payment_date',)
    fieldsets = (
        ("To'lov va qarz undirish ", {
            "fields": ("customer", "supplier", "payment_type", "amount", "info"),
        }), 
    )

    @admin.display(description="To'langan summa")
    def form_amount(self, obj):
        amount = obj.amount or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    

@admin.register(SProducts)
class SProductAdmin(ModelAdmin):
    list_display = ('name', 'quantity_format', 'formatted_price')
    search_fields = ('name',)

    fieldsets = (
        ("Mahsulot ma’lumotlari", {
            "fields": ("name", "quantity", "price"),
        }),
    )
    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} kg"
    
    @admin.display(description="Narxi")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SSupplier)
class SSupplierAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'form_debt')
    search_fields = ('name',)

    fieldsets = (
        ("Yetkazib beruvchi ma’lumotlari", {
            "fields": ("name", "phone", "debt"),
        }),
    )
    
    @admin.display(description="Qarz miqdori")
    def form_debt(self, obj):
        amount = obj.debt or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SCustomers)
class SCustomerAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'form_debt')
    search_fields = ('name',)

    fieldsets = (
        ("Mijoz ma’lumotlari", {
            "fields": ("name", "phone", "debt"),
        }),
    )
    @admin.display(description="Qarz miqdori")
    def form_debt(self, obj):
        amount = obj.debt or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"

@admin.register(SPurchases)
class SPurchaseAdmin(ModelAdmin):
    list_display = ('supplier', 'product', 'quantity_format', 'formatted_price', 'is_debt', 'info', 'purchase_date')
    search_fields = ('product__name', 'supplier__name')
    ordering = ('-purchase_date',)

    fieldsets = (
        ("Sotib olish ma’lumotlari", {
            "fields": ("supplier", "product", "quantity", "price", "is_debt", "info"),
        }),
    )

    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} kg"
    
    @admin.display(description="To'langan summa")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SSales)
class SSaleAdmin(ModelAdmin):
    list_display = ('customer', 'product', 'quantity_format', 'formatted_price', 'is_debt', 'info', 'sale_date')
    search_fields = ('product__name', 'customer__name')
    ordering = ('-sale_date',)

    fieldsets = (
        ("Sotuv ma’lumotlari", {
            "fields": ("customer", "product", "quantity", "price", "is_debt", "info"),
        }),
    )

    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} kg"
    
    @admin.display(description="Narxi")
    def formatted_price(self, obj): 
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SExpenseMachine)
class SExpenseMachineAdmin(ModelAdmin):
    list_display = ('name', 'form_amount', 'info', 'expense_date')
    list_filter = ('name',)
    ordering = ('-expense_date',)
    fieldsets = (
        ("Stanog harajatlari ", {
            "fields": ("name", "cost", "info"),
        }),
    )
    @admin.display(description="Harajat miqdori")
    def form_amount(self, obj):
        amount = obj.cost or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"

@admin.register(SExpenses)
class SExpenseAdmin(ModelAdmin):
    list_display = ('expense', 'worker', 'form_amount', "info", 'expense_date')
    list_filter = ('expense',)
    ordering = ('-expense_date',)
    fieldsets = (
        ("Harajat ", {
            "fields": ("worker", "expense", "cost", "info"),
        }),
    )
    @admin.display(description="Harajat miqdori")
    def form_amount(self, obj):
        amount = obj.cost or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SPaymentDebt)
class SPaymentDebtAdmin(ModelAdmin):
    list_display = ('customer', 'supplier', 'payment_type', 'form_amount', 'info', 'payment_date')
    list_filter = ('payment_type',)
    ordering = ('-payment_date',)
    fieldsets = (
        ("To'lov va qarz undirish ", {
            "fields": ("customer", "supplier", "payment_type", "amount", "info"),
        }), 
    )

    @admin.display(description="To'langan summa")
    def form_amount(self, obj):
        amount = obj.amount or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalProducts)
class SalProductAdmin(ModelAdmin):
    list_display = ('name', 'quantity_format', 'formatted_price')
    search_fields = ('name',)

    fieldsets = (
        ("Mahsulot ma’lumotlari", {
            "fields": ("name", "quantity", "price"),
        }),
    )
    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} pochka"
    
    @admin.display(description="Narxi")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        # Decimal bo‘lib qoladi, faqat ko‘rinishda .00 olib tashlanadi
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalSuppliers)   
class SalSupplierAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'form_debt')
    search_fields = ('name',)

    fieldsets = (
        ("Yetkazib beruvchi ma’lumotlari", {
            "fields": ("name", "phone", "debt"),
        }),
    )
    
    @admin.display(description="Qarz miqdori")
    def form_debt(self, obj):
        amount = obj.debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalCustomers)
class SalCustomerAdmin(ModelAdmin):
    list_display = ('name', 'phone', 'form_debt')
    search_fields = ('name',)

    fieldsets = (
        ("Mijoz ma’lumotlari", {
            "fields": ("name", "phone", "debt"),
        }),
    )
    @admin.display(description="Qarz miqdori")
    def form_debt(self, obj):
        amount = obj.debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalPurchases)
class SalPurchaseAdmin(ModelAdmin):
    list_display = ('supplier', 'product', 'quantity_format', 'formatted_price', 'is_debt', 'info', 'purchase_date')
    search_fields = ('product', 'supplier__name')
    ordering = ('-purchase_date',)

    fieldsets = (
        ("Sotib olish ma’lumotlari", {
            "fields": ("supplier", "product", "quantity", "price", "is_debt", "info"),
        }),
    )

    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} kg"
    
    @admin.display(description="To'langan summa")
    def formatted_price(self, obj):
        amount = obj.price or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalSales)
class SalSaleAdmin(ModelAdmin):
    list_display = ('customer', 'product', 'quantity_format', 'formatted_price', 'is_debt', 'info', 'sale_date')
    search_fields = ('product', 'customer__name')
    ordering = ('-sale_date',)

    fieldsets = (
        ("Sotuv ma’lumotlari", {
            "fields": ("customer", "product", "quantity", "price", "is_debt", "info"),
        }),
    )

    @admin.display(description="Mahsulot miqdori")
    def quantity_format(self, obj):
        amount = obj.quantity or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        
        return f"{amount_str} pochka"
    
    @admin.display(description="Narxi")
    def formatted_price(self, obj): 
        amount = obj.price or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalExpenses)
class SalExpenseAdmin(ModelAdmin):
    list_display = ('name', 'worker', 'form_amount', "info", 'expense_date')
    list_filter = ('name',)
    ordering = ('-expense_date',)
    fieldsets = (
        ("Harajat ", {
            "fields": ("worker", "name", "amount", "info"),
        }),
    )
    @admin.display(description="Harajat miqdori")
    def form_amount(self, obj):
        amount = obj.amount or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalPaymentDebts)
class SalPaymentDebtAdmin(ModelAdmin):
    list_display = ('customer', 'supplier', 'payment_type', 'form_amount', 'info', 'payment_date')
    list_filter = ('payment_type',)
    ordering = ('-payment_date',)
    fieldsets = (
        ("To'lov va qarz undirish ", {
            "fields": ("customer", "supplier", "payment_type", "amount_paid", "info"),
        }), 
    )

    @admin.display(description="To'langan summa")
    def form_amount(self, obj):
        amount = obj.amount_paid or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(SalMonthlyReports)
class SalMonthlyReportAdmin(ModelAdmin):
    list_display = ("month",  'ftotal_sales', 'ftotal_purchases', 'ftotal_expenses', 'ftotal_supplier_debt', 'ftotal_customer_debt', 'fnet_profit')
    ordering = ('-from_date',)
    readonly_fields = ('total_purchases', 'total_sales', 'total_expenses',  'total_supplier_debt', 'total_customer_debt', 'net_profit')
    fieldsets = (
        ("Oylik hisobotlar", {
            "fields": ("month", "from_date", "to_date", "total_purchases", "total_sales", "total_expenses", "total_supplier_debt", "total_customer_debt", "net_profit"),
        }),
    )

    @admin.display(description="Jami xaridlar")
    def ftotal_purchases(self, obj):
        amount = obj.total_purchases or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Jami sotuvlar")
    def ftotal_sales(self, obj):
        amount = obj.total_sales or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Jami xarajatlar")
    def ftotal_expenses(self, obj):
        amount = obj.total_expenses or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Qarzlarimiz")
    def ftotal_supplier_debt(self, obj):
        amount = obj.total_supplier_debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Haqlarimiz")
    def ftotal_customer_debt(self, obj):
        amount = obj.total_customer_debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Sof foyda")
    def fnet_profit(self, obj):
        amount = obj.net_profit or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
@admin.register(MonthlyReport)
class MonthlyReportAdmin(ModelAdmin):
    list_display = ("month", 'ftotal_purchases', 'ftotal_sales', 'ftotal_expenses', 'ftotal_expense_machine', 'ftotal_supplier_debt', 'ftotal_customer_debt', 'fnet_profit')
    ordering = ('-from_date',)
    readonly_fields = ('total_purchases', 'total_sales', 'total_expenses', 'total_expense_machine', 'total_supplier_debt', 'total_customer_debt', 'net_profit')
    fieldsets = (
        ("Oylik hisobotlar", {
            "fields": ("month", "from_date", "to_date", "total_purchases", "total_sales", "total_expenses", "total_expense_machine", "total_supplier_debt", "total_customer_debt", "net_profit"),
        }),
    )

    @admin.display(description="Jami xaridlar")
    def ftotal_purchases(self, obj):
        amount = obj.total_purchases or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Jami sotuvlar")
    def ftotal_sales(self, obj):
        amount = obj.total_sales or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Jami xarajatlar")
    def ftotal_expenses(self, obj):
        amount = obj.total_expenses or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Stanog xarajatlari")
    def ftotal_expense_machine(self, obj):
        amount = obj.total_expense_machine or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Qarzlarimiz")
    def ftotal_supplier_debt(self, obj):
        amount = obj.total_supplier_debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Haqlarimiz")
    def ftotal_customer_debt(self, obj):
        amount = obj.total_customer_debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Sof foyda")
    def fnet_profit(self, obj):
        amount = obj.net_profit or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    

@admin.register(SMonthlyReport)
class SMonthlyReportAdmin(ModelAdmin):
    list_display = ("month", 'ftotal_purchases', 'ftotal_sales', 'ftotal_expenses', 'ftotal_supplier_debt', 'ftotal_customer_debt', 'fnet_profit')
    ordering = ('-from_date',)
    readonly_fields = ('total_purchases', 'total_sales', 'total_expenses',  'total_supplier_debt', 'total_customer_debt', 'net_profit')
    fieldsets = (
        ("Oylik hisobotlar", {
            "fields": ("month", "from_date", "to_date", "total_purchases", "total_sales", "total_expenses", "total_supplier_debt", "total_customer_debt", "net_profit"),
        }),
    )

    @admin.display(description="Jami xaridlar")
    def ftotal_purchases(self, obj):
        amount = obj.total_purchases or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Jami sotuvlar")
    def ftotal_sales(self, obj):
        amount = obj.total_sales or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Jami xarajatlar")
    def ftotal_expenses(self, obj):
        amount = obj.total_expenses or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Qarzlarimiz")
    def ftotal_supplier_debt(self, obj):
        amount = obj.total_supplier_debt or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"
    
    @admin.display(description="Haqlarimiz")
    def ftotal_customer_debt(self, obj):
        amount = obj.total_customer_debt or Decimal('0')
        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())
        return f"{amount_str} so‘m"
    
    @admin.display(description="Sof foyda")
    def fnet_profit(self, obj):
        amount = obj.net_profit or Decimal('0')

        if amount == amount.to_integral_value():
            amount_str = intcomma(amount.quantize(Decimal('1')))
        else:
            amount_str = intcomma(amount.normalize())

        return f"{amount_str} so‘m"