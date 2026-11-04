from pathlib import Path

admin_path = Path('organicfarming/farming/admin.py')
template_path = Path('organicfarming/templates/admin/customer_summary.html')
admin_text = admin_path.read_text(encoding='utf-8')

old1 = "        'id',\n        'user_display',\n        'name',\n        'phone',\n        'city',\n        'payment_method',\n        'total_amount',\n        'created_at',\n    )\n    list_filter = ('payment_method', 'created_at', 'city')\n    search_fields = ('name', 'phone', 'city', 'pincode', 'user__username', 'user__email')\n    readonly_fields = ('created_at', 'total_amount')\n    inlines = [OrderItemInline]\n    list_select_related = ('user',)\n    ordering = ('-created_at',)\n"
new1 = "        'id',\n        'user_display',\n        'email_display',\n        'name',\n        'phone',\n        'city',\n        'payment_method',\n        'total_amount',\n        'created_at',\n    )\n    list_filter = ('payment_method', 'created_at', 'city')\n    search_fields = ('name', 'phone', 'city', 'pincode', 'user__username', 'user__email')\n    readonly_fields = ('created_at', 'total_amount', 'email_display')\n    inlines = [OrderItemInline]\n    list_select_related = ('user',)\n    ordering = ('-created_at',)\n"
if old1 not in admin_text:
    raise SystemExit('Could not find OrderAdmin list_display block')
admin_text = admin_text.replace(old1, new1, 1)

old2 = "        customer_list.append({\n            'name': c['name'],\n            'phone': c['phone'],\n            'email': c['email'],\n            'order_count': len(c['orders']),\n            'dates': dates,\n            'order_link': c['order_link'],\n            'user_label': c['user_label'],\n            'items': items,\n        })\n"
new2 = "        customer_list.append({\n            'name': c['name'],\n            'phone': c['phone'],\n            'email': c['email'],\n            'payment_methods': ', '.join(sorted(c['payment_methods'])) if c['payment_methods'] else '',\n            'order_count': len(c['orders']),\n            'dates': dates,\n            'order_link': c['order_link'],\n            'user_label': c['user_label'],\n            'items': items,\n        })\n"
if old2 not in admin_text:
    raise SystemExit('Could not find customer_list append block')
admin_text = admin_text.replace(old2, new2, 1)

old3 = "    def user_display(self, obj):\n        return obj.user.username if obj.user else 'Guest'\n    user_display.short_description = 'Customer'\n"
new3 = "    def email_display(self, obj):\n        return obj.user.email if obj.user else ''\n    email_display.short_description = 'Email'\n\n    def user_display(self, obj):\n        return obj.user.username if obj.user else 'Guest'\n    user_display.short_description = 'Customer'\n"
if old3 not in admin_text:
    raise SystemExit('Could not find user_display block')
admin_text = admin_text.replace(old3, new3, 1)

admin_path.write_text(admin_text, encoding='utf-8')

template_text = template_path.read_text(encoding='utf-8')
old4 = "        <th style=\"text-align:left; padding:8px;\">Email</th>\n        <th style=\"text-align:left; padding:8px;\">Order Count</th>\n        <th style=\"text-align:left; padding:8px;\">Order Dates</th>\n"
new4 = "        <th style=\"text-align:left; padding:8px;\">Email</th>\n        <th style=\"text-align:left; padding:8px;\">Payment Mode</th>\n        <th style=\"text-align:left; padding:8px;\">Order Count</th>\n        <th style=\"text-align:left; padding:8px;\">Order Dates</th>\n"
if old4 not in template_text:
    raise SystemExit('Could not find template header block')
template_text = template_text.replace(old4, new4, 1)

old5 = "        <td style=\"padding:8px; vertical-align:top;\">{{ c.email }}</td>\n        <td style=\"padding:8px; vertical-align:top;\">{{ c.order_count }}</td>\n        <td style=\"padding:8px; vertical-align:top;\"><a href=\"{{ c.order_link }}\" style=\"color:#1e4bb8;\">View orders</a></td>\n"
new5 = "        <td style=\"padding:8px; vertical-align:top;\">{{ c.email }}</td>\n        <td style=\"padding:8px; vertical-align:top;\">{{ c.payment_methods }}</td>\n        <td style=\"padding:8px; vertical-align:top;\">{{ c.order_count }}</td>\n        <td style=\"padding:8px; vertical-align:top;\"><a href=\"{{ c.order_link }}\" style=\"color:#1e4bb8;\">View orders</a></td>\n"
if old5 not in template_text:
    raise SystemExit('Could not find template row block')
template_text = template_text.replace(old5, new5, 1)

template_path.write_text(template_text, encoding='utf-8')
print('patched')
