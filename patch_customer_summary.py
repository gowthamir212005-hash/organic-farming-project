from pathlib import Path

path = Path('organicfarming/templates/admin/customer_summary.html')
text = path.read_text(encoding='utf-8')
old = '        <td style="padding:8px; vertical-align:top;">{{ c.order_count }}</td>\n        <td style="padding:8px; vertical-align:top;">\n          {% for d in c.dates %}\n'
new = '        <td style="padding:8px; vertical-align:top;">{{ c.order_count }}</td>\n        <td style="padding:8px; vertical-align:top;"><a href="{{ c.order_link }}" style="color:#1e4bb8;">View orders</a></td>\n        <td style="padding:8px; vertical-align:top;">\n          {% for d in c.dates %}\n'
if old not in text:
    raise SystemExit('Pattern not found')
path.write_text(text.replace(old, new), encoding='utf-8')
print('updated')
