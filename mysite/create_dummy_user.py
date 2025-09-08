from django.contrib.auth.models import User

if not User.objects.filter(username='demo').exists():
    User.objects.create_superuser('demo', 'demo@example.com', 'demo1234')
    print('Dummy superuser created: demo/demo1234')
else:
    print('Dummy user already exists.')