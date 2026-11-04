from pathlib import Path

admin_path = Path('organicfarming/farming/admin.py')
template_path = Path('organicfarming/templates/admin/customer_summary.html')
admin_text = admin_path.read_text(encoding='utf-8')

old = "    list_display = (\n        'id',\n        'user_display',\n        'name',\n        'phone',\n        'city',\n        'payment_method',\n        'total_amount',\n        'created_at',\n    )\n    list_filter = ('payment_method', 'created_at', 'city')\n    search_fields = ('name', 'phone', 'city', 'pincode', 'user__username', 'user__email')\n    readonly_fields = ('created_at', 'total_amount')\n"
new = "    list_display = (\n        'id',\n        'user_display',\n        'email_display',\n        'name',\n        'phone',\n        'city',\n        'payment_method',\n        'total_amount',\n        'created_at',\n    )\n    list_filter = ('payment_method', 'created_at', 'city')\n    search_fields = ('name', 'phone', 'city', 'pincode', 'user__username', 'user__email')\n    readonly_fields = ('created_at', 'total_amount', 'email_display')\n"
if old not in admin_text:
    raise SystemExit('Could not find OrderAdmin block to patch')
admin_text = admin_text.replace(old, new, 1)

old = "    def user_display(self, obj):\n        return obj.user.username if obj.user else 'Guest'\n    user_display.short_description = 'Customer'\n"
new = "    def email_display(self, obj):\n        return obj.user.email if obj.user else ''\n    email_display.short_description = 'Email'\n\n    def user_display(self, obj):\n        return obj.user.username if obj.user else 'Guest'\n    user_display.short_description = 'Customer'\n"
if old not in admin_text:
    raise SystemExit('Could not find user_display block to patch')
admin_text = admin_text.replace(old, new, 1)
admin_path.write_text(admin_text, encoding='utf-8')

template_text = template_path.read_text(encoding='utf-8')
old = "        <th style=\"text-align:left; padding:8px;\">Email</th>\n        <th style=\"text-align:left; padding:8px;\">Order Count</th>\n        <th style=\"text-align:left; padding:8px;\">Order Dates</th>\n"
new = "        <th style=\"text-align:left; padding:8px;\">Email</th>\n        <th style=\"text-align:left; padding:8px;\">Payment Mode</th>\n        <th style=\"text-align:left; padding:8px;\">Order Count</th>\n        <th style=\"text-align:left; padding:8px;\">Order Dates</th>\n"
if old not in template_text:
    raise SystemExit('Could not find template header block to patch')
template_text = template_text.replace(old, new, 1)

old = "        <td style=\"padding:8px; vertical-align:top;\">{{ c.email }}</td>\n        <td style=\"padding:8px; vertical-align:top;\">{{ c.order_count }}</td>\n        <td style=\"padding:8px; vertical-align:top;\"><a href=\"{{ c.order_link }}\" style=\"color:#1e4bb8;\">View orders</a></td>\n"
new = "        <td style=\"padding:8px; vertical-align:top;\">{{ c.email }}</td>\n        <td style=\"padding:8px; vertical-align:top;\">{{ c.payment_methods }}</td>\n        <td style=\"padding:8px; vertical-align:top;\">{{ c.order_count }}</td>\n        <td style=\"padding:8px; vertical-align:top;\"><a href=\"{{ c.order_link }}\" style=\"color:#1e4bb8;\">View orders</a></td>\n"
if old not in template_text:
    raise SystemExit('Could not find template row block to patch')
template_text = template_text.replace(old, new, 1)
template_path.write_text(template_text, encoding='utf-8')
print('patched update_payment_email')
