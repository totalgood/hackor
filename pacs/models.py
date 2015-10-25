from django.conf import settings
from utils import models
from utils import LongCharField

host = settings.DATABASES['default']['HOST'].lower()
dbname = settings.DATABASES['default']['NAME'].lower()

# use a recent localhost mirror of the RDS db created by Daniel
if host in ('localhost', '127.0.0.1', '192.168.0.0') and dbname == 'btc':
    from models_localrds import *
elif '.rds.' in host or host.endswith('amazonaws.com'):
    from models_rds import *
elif 'localhost' in host or '127.0.0.1' in host or '192.168.' in host:
    from models_local import *
