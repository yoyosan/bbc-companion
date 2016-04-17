import base64

from library.common import *

env.user = config.REMOTE_USER
env.password = base64.b64decode(config.REMOTE_PASSWORD)
env.sudo_user = config.REMOTE_SUDO_USER
env.colorize_errors = True
env.hosts = config.REMOTE_HOSTS

# import tasks - DO NOT remove this line and THE NEXT!
from tasks import build, command, deploy, gateway, info, service, slot, v3, worker
