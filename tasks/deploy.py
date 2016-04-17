import time

from library.common import *


@task(alias='w')
def worker(worker, env='dev', branch='stable'):
    """
    \033[94mDeploy a worker to a specific environment and/or branch.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.w:mail | bbcdc deploy.w:mail,preprod,fix-something-branch\033[0m
    """
    cmd = 'sudo ./mep-worker.sh %s %s %s' % (worker, env, branch)
    run_in_tmux_session('worker-deploy', cmd, config.REMOTE_MEP_CMD_DIR)
    notify('Worker "%s" deployed on "%s" environment with "%s" branch.' % (worker, env, branch))


@task(alias='we')
def worker_envs(workert, branch='stable'):
    """
    \033[94mDeploy a worker on dev and preprod and/or for a specific branch.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.we:mail | bbcdc deploy.we:mail,fix-something-branch\033[0m
    """
    for env in config.DEPLOY_ENVS:
        execute(worker, workert, env, branch)


@task(alias='c')
def command(command, env='dev'):
    """
    \033[94mDeploy a command to a specific environment.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.c:axes | bbcdc deploy.c:axes,preprod\033[0m
    """
    cmd = 'sudo ./mep-command.sh %s %s' % (command, env)
    run_in_tmux_session('command-deploy', cmd, config.REMOTE_MEP_CMD_DIR)
    notify('Command "%s" deployed on "%s" environment.' % (command, env))


@task(alias='ce')
def command_envs(command):
    """
    \033[94mDeploy a command to dev and preprod.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.ce:axes\033[0m
    """
    for env in config.DEPLOY_ENVS:
        execute(command, command, env)


@task
def v3():
    """
    \033[94mDeploy V3. It will ask whether it's a finalyze.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.v3\033[0m
    """
    session_name = 'deploy_v3'
    if confirm(colors.green('Is this a finalize?', bold=True)):
        cmd = 'sudo ./finalyze_mepv3.sh'

        # abort the existing process of deployment
        run('tmux send-keys -t "%s" "%s"' % (session_name, 'C-c'))
        run_in_tmux_session(session_name, cmd, config.REMOTE_MEP_CMD_DIR)
        notify('Finished FINALIZE!')
    else:
        cmd = 'sudo ./mep-v3.sh'

        if confirm(colors.red('Is SYNC allowed?', bold=True)):
            run_in_tmux_session(session_name, cmd, config.REMOTE_MEP_CMD_DIR)
            notify('Finished SYNC!')
        else:
            throw_error('You need a break!')


@task()
@hosts(config.REMOTE_PA3_HOSTS)
def pa3():
    """
    \033[94mBuild and deploy PA3 containers.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.pa3\033[0m
    """
    env.user = 'dev'
    session_name = 'pa3_build_mpalade'
    cmd = 'sudo ./deploy-v3.sh'
    run_in_tmux_session(session_name, cmd, config.REMOTE_PA3_DIR)


@task(alias='fac')
def flush_admin_cache():
    """
    \033[94mFlush the admin panel cache.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc deploy.fac\033[0m
    """
    with settings(hide('stdout')):
        for i in xrange(6):
            print 'Retry #%s' % (i + 1)
            local('curl -Is "https://static.blablacar.com/v-1/assets/build/js/admin.js" --header ' +
                  '"Cache-Control: no-cache"')
            local('curl -Is "https://static.blablacar.com/v-1/assets/build/css/admin/admin.css" --header ' +
                  '"Cache-Control: no-cache"')
            time.sleep(0.5)
