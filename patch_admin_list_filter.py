from pathlib import Path

path = Path('organicfarming/farming/admin.py')
text = path.read_text(encoding='utf-8')
old = "    list_filter = ('payment_method', 'created_at', 'city')\n"
new = "    list_filter = ('payment_method', 'created_at', 'city', 'user')\n"
if old not in text:
    raise SystemExit('Pattern not found in admin.py')
path.write_text(text.replace(old, new), encoding='utf-8')
print('updated admin.py')
