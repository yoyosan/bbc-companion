from library.common import *


@task
def fixtures(extra_cmd=''):
    """
    \033[94mReset V3 fixtures.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.fixtures:reset | bbcdc v3.fixtures:reset\033[0m
    """
    with lcd(get_dir('ADMIN', 'fixtures')):
        update_project()
        local_with_warning("./fixtures %s" % extra_cmd)


@task(alias='es')
def elastic_search():
    """
    \033[94mReset ES definitions and add river.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.es\033[0m
    """
    with lcd(get_dir('ADMIN', 'elasticsearch')):
        update_project(False)
        local_with_warning("./reset.sh")
        local_with_warning("./river.sh")
        notify('Elastic search RESET done.')


@task()
def rbmq():
    """
    \033[94mReset RabbitMQ queues and exchanges.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.rbmq\033[0m
    """
    with lcd(get_dir('ADMIN', 'rabbit-mq')):
        update_project()
        local_with_warning("./bin/create_local.sh")
        notify('RabbitMQ RESET done.')


@task(alias='wu')
def warm_up(env='dev'):
    """
    \033[94mWarm up a specific env. "dev" is the default.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.wu | bbcdc v3.wu:test\033[0m
    """
    with lcd(get_dir('V3')):
        local("./app/console cac:war --env=%s" % env)
        notify('Warmup done for "%s".' % env)


@task
def reset(env='dev'):
    """
    \033[94mDo a V3 reset for a specific env. "dev" is the default.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.reset | bbcdc v3.reset:test\033[0m
    """
    with lcd(get_dir('V3')):
        local("git status -sb")
        local_with_warning("composer install")
        local_with_warning("./reset.sh %s" % env)
        execute(warm_up, env=env)
        local("./assets-install.sh")
        execute(elastic_search)
        notify("Reset Done")


@task(alias='rb')
def run_behat():
    """
    \033[94mStart the behat containers.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.rb\033[0m
    """
    with settings(warn_only=True):
        local('sudo docker stop sehub sechrome')
        local('sudo docker rm sehub sechrome')

    local('sudo docker run -d --name sehub -h sehub -p 4444:4444 docker-registry.priv.blablacar.net/sehub')
    local('sudo docker run -d --name sechrome -h sechrome -e VNC=true --link sehub:hub' +
          ' -p 5900:5900 docker-registry.priv.blablacar.net/sechrome')


@task(alias='w')
def worker():
    """
    \033[94mStart the global worker for V3.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc v3.w\033[0m
    """
    with lcd(get_dir('V3')):
        local_with_warning('./app/console swarrot:consume:default global -vvv -t 86400 -m 100000')
