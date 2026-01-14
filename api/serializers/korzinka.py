from models import Investors, Products, Suppliers, Customers, Purchases, Sales, Expenses, ExpenseMachine
from rest_framework import serializers

class InvestorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investors
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'

class ExpenseMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseMachine
        fields = '__all__'