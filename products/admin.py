from django.contrib import admin
from products.models.category import Category
from products.models.product import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    row_number = 0

    list_display = ('row_product', 'category', 'name', 'price', 'off', 'description', 'stock')

    def row_product(self, obj):
        count = Product.objects.all().count()
        if self.row_number < count:
            self.row_number += 1
        else:
            self.row_number = 1

        return self.row_number


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    row_number = 0
    list_display = ('row_category', 'name',)

    def row_category(self, obj):
        count = Category.objects.all().count()
        if self.row_number < count:
            self.row_number += 1
        else:
            self.row_number = 1

        return self.row_number
