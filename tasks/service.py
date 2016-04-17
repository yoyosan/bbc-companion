from library.common import *


@task(alias='pm')
def priv_msgs(action='start', env='dev'):
    """
    \033[94mStart/Stop the private messages service.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc service.pm:start|stop,dev|test\033[0m
    """
    allowed_envs = ['dev', 'test']
    if env not in allowed_envs:
        throw_error('Invalid environment! Choose one of the following: %s' % allowed_envs)

    session_name = 'priv-msgs-' + env
    flag = '-d'
    if env == 'test':
        flag = '-t'

    if action == 'stop':
        local('tmux send-keys -t "%s" "%s"' % (session_name, 'C-c'))
    else:
        cmd = 'java -jar private-messages.jar %s ' % flag
        run_in_local_tmux_session(session_name, cmd, get_dir('SRVS', 'private-messages'))
