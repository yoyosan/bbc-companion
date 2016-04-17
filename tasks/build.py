from library.common import *


@task
def satis():
    """
    \033[94mUpdate the composer repository with satis.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc build.satis\033[0m
    """
    with cd(config.REMOTE_SATIS_DIR):
        sudo('./bin/satis build packages/comuto3.json www/')
        notify('SATIS done.')


# @task
def test():
    run_in_tmux_session('test-bbcdc', 'ping google.com', '/space/products')
