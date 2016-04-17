from fabric import colors
from fabric.api import *
from fabric.contrib.console import confirm

import config

VERSION = '1.2'


def update_project(with_composer=True, branch=None):
    if branch is not None:
        local_with_warning('git checkout %s' % branch)

    local_with_warning('git pull')

    if with_composer:
        local_with_warning('composer install')


def local_with_warning(command):
    """
    Run a local command but confirm to continue when an error occurs.

    :param command:
    """
    with settings(warn_only=True):
        result = local(command)
    if result.failed:
        notify("Fail : %s" % command)
    if result.failed and not confirm("Continue anyway?"):
        abort("Abort after fail")


def notify(message):
    local(config.NOTIFICATION_CMD % message)


def get_dir(category, project=''):
    return config.DIR_WORK + config.DIR_CATEGORIES.get(category) + '/' + project


def run_in_tmux_session(session_name, command, directory, target='run'):
    allowed_targets = ['local', 'run']
    if target not in allowed_targets:
        throw_error('Target should be %s' % allowed_targets)

    cd_command = 'cd ' + directory

    with settings(warn_only=True):
        result = call_target(target,
                             'tmux list-sessions -F \'#S|#{session_activity_string}\' | grep "%s"' % session_name)

    if result.failed:
        call_target(target, 'tmux new-session -d -s "%s"' % session_name)

    call_target(target, 'tmux send -t "%s" clear ENTER' % session_name)
    call_target(target, 'tmux send -t "%s" "%s" ENTER' % (session_name, cd_command))
    call_target(target, 'tmux send -t "%s" "%s" ENTER' % (session_name, command))
    call_target(target, 'tmux attach-session -t "%s"' % session_name)


def run_in_local_tmux_session(session_name, command, directory):
    run_in_tmux_session(session_name, command, directory, 'local')


def not_implemented():
    print
    print colors.yellow('\tThis task is not yet implemented!\n\tHelp this tool grow by implementing it ;)')
    print


def throw_error(msg):
    abort(colors.white(msg, True))


def call_target(target, arg):
    return globals()[target](arg)
