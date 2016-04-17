from library.common import *


@task(alias='e')
def execute(worker, branch='master'):
    """
    \033[94mExecute a local worker.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc worker.e:mail | bbcdc worker.e:mail,fix-something-branch\033[0m
    """
    with settings(warn_only=True):
        result = local('cd %s' % get_dir('WORKERS', worker))

    if result.failed:
        with lcd(get_dir('WORKERS')):
            local_with_warning('git clone ssh://git@git.priv.blablacar.net:7999/wrk/%s.git' % worker)

    with lcd(get_dir('WORKERS', worker)):
        update_project(True, branch)
        local_with_warning('./console consume %s -vvv --timeout=86400' % worker.replace('-', '_'))


@task(alias='er')
@hosts(config.REMOTE_WORKER_HOSTS)
def execute_remote(worker, queue_suffix='dl', options=''):
    """
    \033[94mExecute a remote production worker to consume a queue.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc worker.er:mail | bbcdc worker.er:mail,dl,"-m\=1 -r"\033[0m
    """
    env.user = 'dev'
    target_dir = config.REMOTE_PRODUCTS_DIR + worker + '-worker/prod/'
    queue_name = worker.replace('-', '_') + '_%s' % queue_suffix
    cmd = 'sudo -u www-data ./console consume "%s" -vvv %s' % (queue_name, options)

    with cd(target_dir):
        run(cmd)


# @task(alias='a')
def add(name=''):
    not_implemented()
