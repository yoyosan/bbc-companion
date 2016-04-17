import os
import sys

# the local working directory of all BBC projects
DIR_WORK = '~/Work'
# project directories per category
DIR_CATEGORIES = {
    'V3': 'bbc',
    'WORKERS': 'workers',
    'COMMANDS': 'commands',
    'ADMIN': 'admin',
    'MS': 'micro-services',
    'SRVS': 'services'
}

# the remote host/s on which some tasks will be run
REMOTE_HOSTS = ['tools']
REMOTE_WORKER_HOSTS = ['work1']
REMOTE_V3_WORKER_HOSTS = ['workv31']
# pa3 hosts
REMOTE_PA3_HOSTS = ['deploy1']
# batch host
REMOTE_COMMAND_HOSTS = ['batch1']
# preprod and dev
REMOTE_PREPROD_WORKER_HOSTS = ['workpp']
REMOTE_DEV_WORKER_HOSTS = ['workdev1']

# credentials
REMOTE_USER = ''
REMOTE_PASSWORD = ''
REMOTE_SUDO_USER = 'www-data'

# dirs
REMOTE_PRODUCTS_DIR = '/products/'
REMOTE_SATIS_DIR = REMOTE_PRODUCTS_DIR + 'composer-packages/satis/'
REMOTE_SLOT_DIR = REMOTE_PRODUCTS_DIR + 'comuto3/slots/'
REMOTE_MEP_CMD_DIR = '/scripts/meps/'
REMOTE_MEP_PROJECT_DIR = '/products/meps/'
REMOTE_PA3_DIR = '/scripts/deploy-pa3/'

# envs
DEPLOY_ENVS = ['dev', 'preprod']

# notification area
NOTIFICATION_TITLE = 'BBC Developer Companion'
NOTIFICATION_ICON = os.path.dirname(os.path.realpath(__file__)) + '/assets/puss-in-boots-mercy.jpg'
if sys.platform == 'linux2':
    NOTIFICATION_CMD = 'notify-send -t 10000 -i ' + NOTIFICATION_ICON + ' ' + NOTIFICATION_TITLE + '"%s"'
elif sys.platform == 'darwin':
    NOTIFICATION_CMD = 'terminal-notifier -title \'' + NOTIFICATION_TITLE + '\' -message \'%s\' -appIcon ' \
                       + NOTIFICATION_ICON + ' -sound Tink'
