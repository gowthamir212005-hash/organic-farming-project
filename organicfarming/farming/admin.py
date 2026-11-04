from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render
from django.conf import settings
import os
from urllib.parse import quote
from .models import Order, OrderItem, Product

admin.site.site_header = "Organic Farm Admin"
admin.site.site_title = "Organic Farm Dashboard"
admin.site.index_title = "Organic Farm Management"


def database_design_view(request):
    doc_path = os.path.join(settings.BASE_DIR, 'DATABASE_DESIGN.md')
    content = ''
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        content = 'Could not load documentation: {}'.format(e)
    context = {'doc_content': content}
    return render(request, 'admin/database_design.html', context)


def customer_summary_view(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').all().order_by('name', 'phone', 'created_at')
    customers = {}
    for o in orders:
        email = o.user.email if o.user else ''
        user_id = o.user.id if o.user else None
        key = (user_id, o.name or '', o.phone or '', email)
        if key not in customers:
            if user_id:
                order_link = reverse('admin:farming_order_changelist') + f'?user__id__exact={user_id}'
                user_label = o.user.username
            else:
                order_link = reverse('admin:farming_order_changelist') + f'?q={quote(o.name or "")}'
                user_label = 'Guest'
            customers[key] = {
                'name': o.name or '',
                'phone': o.phone or '',
                'email': email,
                'orders': [],
                'item_groups': {},
                'payment_methods': set(),
                'order_link': order_link,
                'user_label': user_label,
            }
        customers[key]['orders'].append(o)
        customers[key]['payment_methods'].add(o.payment_method)
        for item in o.items.all():
            p_name = item.product.name if item.product else 'Unknown'
            q = int(item.quantity)
            price_str = str(item.price)
            gkey = (p_name, q, price_str)
            grp = customers[key]['item_groups'].setdefault(gkey, {'product': p_name, 'quantity': q, 'price': price_str, 'occurrences': 0, 'total_quantity': 0, 'total_spent': 0.0})
            grp['occurrences'] += 1
            grp['total_quantity'] += q
            grp['total_spent'] += float(q) * float(price_str)

    customer_list = []
    for c in customers.values():
        dates = [o.created_at.strftime('%Y-%m-%d %H:%M') for o in c['orders']]
        items = []
        for grp in c['item_groups'].values():
            items.append({
                'product': grp['product'],
                'quantity': grp['quantity'],
                'price': grp['price'],
                'occurrences': grp['occurrences'],
                'total_quantity': grp['total_quantity'],
                'total_spent': "{:.2f}".format(grp['total_spent']),
            })

        customer_list.append({
            'name': c['name'],
            'phone': c['phone'],
            'email': c['email'],
            'payment_methods': ', '.join(sorted(c['payment_methods'])) if c['payment_methods'] else '',
            'order_count': len(c['orders']),
            'dates': dates,
            'order_link': c['order_link'],
            'user_label': c['user_label'],
            'items': items,
        })

    context = {'customers': customer_list}
    return render(request, 'admin/customer_summary.html', context)


original_get_urls = admin.site.get_urls
def get_urls():
    urls = [
        path('database-design/', admin.site.admin_view(database_design_view), name='database_design'),
        path('customer-summary/', admin.site.admin_view(customer_summary_view), name='customer_summary'),
    ]
    return urls + original_get_urls()
admin.site.get_urls = get_urls


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)
    fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_display',
        'email_display',
        'name',
        'phone',
        'city',
        'payment_method',
        'total_amount',
        'created_at',
    )
    list_filter = ('payment_method', 'created_at', 'city')
    search_fields = ('name', 'phone', 'city', 'pincode', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'total_amount', 'email_display')
    inlines = [OrderItemInline]
    list_select_related = ('user',)
    ordering = ('-created_at',)
    actions = ('delete_selected', 'delete_selected_orders',)
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'name', 'phone', 'address', 'city', 'pincode')
        }),
        ('Order Details', {
            'fields': ('payment_method', 'total_amount', 'created_at')
        }),
    )

    def email_display(self, obj):
        return obj.user.email if obj.user else ''
    email_display.short_description = 'Email'

    def user_display(self, obj):
        return obj.user.username if obj.user else 'Guest'
    user_display.short_description = 'Customer'

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

    def delete_selected_orders(self, request, queryset):
        if not request.user.has_perm('farming.delete_order'):
            self.message_user(request, "You do not have permission to delete orders.", level=messages.ERROR)
            return
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} order(s).", level=messages.SUCCESS)
    delete_selected_orders.short_description = 'Delete selected orders'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')
    search_fields = ('name',)
    ordering = ('name',)
    fields = ('name', 'price', 'image')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__name', 'order__id')
    list_filter = ('product',)
    actions = ('delete_selected', 'delete_selected_orderitems',)

    def delete_selected_orderitems(self, request, queryset):
        if not request.user.has_perm('farming.delete_orderitem'):
            self.message_user(request, "You do not have permission to delete order items.", level=messages.ERROR)
            return
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Successfully deleted {count} order item(s).", level=messages.SUCCESS)
    delete_selected_orderitems.short_description = 'Delete selected order items'


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
