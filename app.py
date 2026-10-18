import uuid
from datetime import datetime, timedelta
import boto3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
db = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = db.Table('Visitors')
FMT = '%Y-%m-%d %H:%M:%S'

PAGE = """
<!doctype html><html><head><title>Visitor Management System</title>
<style>
body{font-family:Arial;max-width:900px;margin:30px auto;padding:0 15px}
input,select{padding:8px;margin:4px}
.f input{width:200px}
button{padding:8px 14px;background:#232f3e;color:#fff;border:0}
table{width:100%;border-collapse:collapse;margin-top:8px}
td,th{border:1px solid #ccc;padding:8px;text-align:left}
.box{background:#f4f6f8;padding:10px;margin-top:15px}
h2{margin:25px 0 0}
h4{margin:12px 0 0;color:#555}
</style></head><body>
<h1>Visitor Management System</h1>
<h3>Visitor Check-In</h3>
<form class="f" method="post" action="/checkin">
<input name="name" placeholder="Visitor name" required>
<input name="host" placeholder="Person to meet" required>
<input name="purpose" placeholder="Purpose of visit" required>
<button>Check In</button>
</form>
<div class="box">
<form method="get" action="/">
Month: <input type="month" name="month" value="{{month}}">
Date: <input type="date" name="date" value="{{day}}">
Hour: <select name="hour">
<option value="">All hours</option>
{% for v, l in hours %}
<option value="{{v}}" {% if v==hour %}selected{% endif %}>{{l}}</option>
{% endfor %}
</select>
Sort: <select name="sort">
<option value="new" {% if order=='new' %}selected{% endif %}>Newest first</option>
<option value="old" {% if order=='old' %}selected{% endif %}>Oldest first</option>
</select>
<button>Apply</button>
<a href="/">Reset</a>
</form>
</div>
<p>Showing {{count}} visitor(s)</p>
{% if not groups %}<p>No visitors found.</p>{% endif %}
{% for mlabel, days in groups %}
<h2>{{mlabel}}</h2>
{% for dlabel, rows in days %}
<h4>{{dlabel}}</h4>
<table>
<tr><th>Name</th><th>Meeting</th><th>Purpose</th><th>In</th><th>Out</th></tr>
{% for v in rows %}
<tr><td>{{v.name}}</td><td>{{v.host}}</td><td>{{v.purpose}}</td>
<td>{{v.tin}}</td>
<td>{% if v.tout %}{{v.tout}}{% else %}
<form method="post" action="/checkout/{{v.visitor_id}}">
<button>Check Out</button></form>
{% endif %}</td></tr>
{% endfor %}
</table>
{% endfor %}
{% endfor %}
</body></html>
"""

HOURS = [(f'{h:02d}', datetime(2000, 1, 1, h).strftime('%I %p').lstrip('0'))
         for h in range(24)]

def now():
    t = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return t.strftime(FMT)

def tm(s):
    return datetime.strptime(s, FMT).strftime('%I:%M %p')

def group(items):
    groups = []
    for i in items:
        d = datetime.strptime(i['check_in'], FMT)
        m = d.strftime('%B %Y')
        dl = f"{d:%a}, {d.day} {d:%b %Y}"
        if not groups or groups[-1][0] != m:
            groups.append((m, []))
        days = groups[-1][1]
        if not days or days[-1][0] != dl:
            days.append((dl, []))
        days[-1][1].append(i)
    return groups

@app.route('/')
def home():
    month = request.args.get('month', '')
    day = request.args.get('date', '')
    hour = request.args.get('hour', '')
    order = request.args.get('sort', 'new')
    items = table.scan()['Items']
    if month:
        items = [i for i in items if i['check_in'].startswith(month)]
    if day:
        items = [i for i in items if i['check_in'].startswith(day)]
    if hour:
        items = [i for i in items if i['check_in'][11:13] == hour]
    items.sort(key=lambda x: x['check_in'], reverse=(order == 'new'))
    for i in items:
        i['tin'] = tm(i['check_in'])
        i['tout'] = tm(i['check_out']) if i.get('check_out') else ''
    return render_template_string(
        PAGE, groups=group(items), count=len(items), hours=HOURS,
        month=month, day=day, hour=hour, order=order)

@app.route('/checkin', methods=['POST'])
def checkin():
    f = request.form
    table.put_item(Item={
        'visitor_id': str(uuid.uuid4()),
        'name': f['name'], 'host': f['host'],
        'purpose': f['purpose'], 'check_in': now()})
    return redirect('/')

@app.route('/checkout/<vid>', methods=['POST'])
def checkout(vid):
    table.update_item(
        Key={'visitor_id': vid},
        UpdateExpression='SET check_out = :t',
        ExpressionAttributeValues={':t': now()})
    return redirect('/')

app.run(host='0.0.0.0', port=80)
