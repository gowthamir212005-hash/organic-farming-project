from pathlib import Path
path = Path('organicfarming/farming/admin.py')
text = path.read_text(encoding='utf-8')
old = "        ('Customer Information', {\n            'fields': ('user', 'name', 'phone', 'address', 'city', 'pincode')\n        }),\n"
new = "        ('Customer Information', {\n            'fields': ('user', 'name', 'email_display', 'phone', 'address', 'city', 'pincode')\n        }),\n"
if old not in text:
    raise SystemExit('Could not find customer information fieldset block')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
print('updated fieldset')
