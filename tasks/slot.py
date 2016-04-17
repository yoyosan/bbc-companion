from library.common import *


@task(alias='i')
def init(slot, branch='master'):
    """
    \033[94mInit a slot with a specific branch. "master" is the default branch.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc slot.i:6 | bbcdc slot.i:6,feat-some-branch\033[0m
    """
    with cd(config.REMOTE_SLOT_DIR + slot):
        with cd(config.REMOTE_MEP_PROJECT_DIR):
            sudo('app/console meps:branch:deploy --author %s %s %s' % (config.REMOTE_USER, branch, slot))

        sudo('git prune')
        sudo('git pull')
        sudo('git checkout %s' % branch)
        sudo('/space/products/comuto3/misc/init-slot2.sh %s prod' % slot)
        slot_url(slot)
        notify('Slot %s initialized.' % slot)


@task(alias='ri')
def reinit(slot):
    """
    \033[94mRe-init a slot.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc slot.ri:6\033[0m
    """
    with cd(config.REMOTE_SLOT_DIR + slot):
        # get the current branch
        with cd(config.REMOTE_MEP_PROJECT_DIR):
            current_branch = sudo('app/console meps:slot:list | grep "%s |" | cut -d" " -f3' % slot)

        # treat the situation when a rebase with master was done
        sudo('git checkout master')
        sudo('git reset --hard HEAD')
        sudo('git pull')
        sudo('git branch -D %s' % current_branch)
        sudo('git checkout %s' % current_branch)
        sudo('/space/products/comuto3/misc/init-slot2.sh %s prod' % slot)

        # update the slot time so that it doesn't get old ;)
        with cd(config.REMOTE_MEP_PROJECT_DIR):
            sudo('app/console meps:slot:update-time %s' % slot)

        slot_url(slot)
        notify('Slot %s reinitialized.' % slot)


@task(alias='cmd')
def cmd(slot, command):
    """
    \033[94mRun a command in a slot's directory.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc slot.cmd:6,"app/console cache:clear"\033[0m
    """
    with cd(config.REMOTE_SLOT_DIR + slot):
        sudo(command)
        notify('Command % run on slot %s.' % (command, slot))


@task(alias='err')
def errors():
    """
    \033[94mTail the contents of "/space/log/php_error.log", on comtools1.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc slot.err\033[0m
    """
    sudo('tail -f /space/log/php_error.log')


@task(alias='ip')
def init_profiling(slot):
    """
    \033[94mInit the profiling env for a slot.\033[0m \033[92mUsage:\033[0m \033[93mbbcdc slot.ip:6\033[0m
    """
    with cd(config.REMOTE_SLOT_DIR + slot):
        # execute(slot_command, slot, 'rm -rf app/cache/profiling/*')
        execute(cmd, slot, 'app/console cache:warmup --env=profiling')


@task
def free(slot=None):
    """
    \033[94mGet a list of free slots or find out whether a slot is free\033[0m \033[92mUsage:\033[0m \033[93mbbcdc slot.free | slot.free:6\033[0m

    :param slot: Slot number to check.
    """
    with cd(config.REMOTE_MEP_PROJECT_DIR):
        if slot is not None:
            sudo('app/console meps:slot:list | grep ' + slot)
        else:
            sudo('app/console meps:slot:list | grep master')


def slot_url(slot):
    repeat_no = 60
    print '#' * repeat_no
    print '# \033[92mSlot URL:\033[0m https://s%s-preprod-fr.maquettes.blablacar.com/' % slot
    print '#' * repeat_no
