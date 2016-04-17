from library.common import *


@task(alias='e')
def execute(cmd, extra_cmd=''):
    """
    \033[94mExecute a local command.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc command.e:indexer-contact | bbcdc command.e:indexer-contact,"check:indexation"\033[0m
    """
    with settings(warn_only=True):
        result = local('cd %s' % get_dir('COMMANDS', cmd))

    if result.failed:
        with lcd(get_dir('COMMANDS')):
            local_with_warning('git clone ssh://git@git.priv.blablacar.net:7999/cmd/%s.git' % cmd)

    with lcd(get_dir('COMMANDS', cmd)):
        update_project()
        local('./console %s' % extra_cmd)


@task(alias='mse')
@hosts(config.REMOTE_COMMAND_HOSTS)
def member_search_export(id, file):
    """
    \033[94mRuns the member search export command for an ES filter id.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc command.mse:1,/tmp/ids.csv\033[0m
    """
    env.user = 'dev'
    target_dir = config.REMOTE_PRODUCTS_DIR + 'comuto3/prod/'
    with cd(target_dir):
        run('sudo -u www-data ./app/console blablacar:member-search:export --env=prod --no-debug %s %s' % (id, file))
        local('scp %s@%s:%s .' % (env.user, config.REMOTE_COMMAND_HOSTS[0], file))
        notify('Export %s done for id %s.' % (file, id))


@task(alias='er')
@hosts(config.REMOTE_COMMAND_HOSTS)
def execute_remote(cmd, options='-h'):
    """
    \033[94mExecute a remote production command to consume a queue.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc worker.er:total-ftp | bbcdc worker.er:total-ftp,"-h"\033[0m
    """
    env.user = 'dev'
    target_dir = config.REMOTE_PRODUCTS_DIR + cmd + '-command/prod/'
    cmd = 'sudo -u www-data ./console -vvv %s' % options

    with cd(target_dir):
        run(cmd)
