from .base import *

DEBUG = False

secrets = json.load(open(os.path.join(SECRETS_DIR, 'deploy.json')))
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

# No Use RDS & S3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Log
LOG_DIR = os.path.join(ROOT_DIR, '.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s (%(asctime)s)\n>>> %(message)s',
        },
    },
    'handlers': {
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'idea_error.log'),
            'formatter': 'default'
        },
        'console_info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_error', 'console_info'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# -- Code For AWS ELB Health Check -- #
# Reference
# - https://lhy.kr/elb-healthcheck-for-django
# - https://hashedin.com/blog/5-gotchas-with-elastic-beanstalk-and-django/
def is_ec2_linux():
    """
    Detect if we are running on an EC2 Linux Instance
    See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """
    Get the private IP Address of the machine if running on an EC2 linux server
    """
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)

# -- ----------------------------- -- #
