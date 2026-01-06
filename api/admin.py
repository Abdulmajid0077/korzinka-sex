from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.humanize.templatetags.humanize import intcomma
from decimal import Decimal
from .models import Investors, Products, Purchases, Sales, Customers, Suppliers, Expenses, ExpenseMachine


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
    
    @admin.display(description="To'langan summa")
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
    list_display = ('supplier', 'product_name', 'quantity_format', 'formatted_price', 'info', 'purchase_date')
    search_fields = ('product_name', 'supplier__name')
    ordering = ('-purchase_date',)

    fieldsets = (
        ("Sotib olish ma’lumotlari", {
            "fields": ("supplier", "product_name", "quantity", "price", "info"),
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
        

@admin.register(Suppliers)
class SupplierAdmin(ModelAdmin):
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
    
@admin.register(Expenses)
class ExpenseAdmin(ModelAdmin):
    list_display = ('expense_type', 'worker_name', 'form_amount', 'expense_date')
    search_fields = ('expense_type', )
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
    filters = ('expense_type',)
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