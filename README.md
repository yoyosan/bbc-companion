# Coding Night #2: BBC Developer Companion

# Introduction

Note: Inspired by pyfab-dev, by Matthieu Morlon.

This tool was created to:

* shorten the time to run regular tasks
* no need to remember all the steps to do a regular task
* one command to consume a queue, without adding it into supervisor

Specification page [here](https://docs.google.com/document/d/1yS6B4VyTa_oBstPAPnMksTYIBbHGK8wreJaVcH2PI9g/edit).

Please feel free to improve it via PRs.

# Installation

## Linux

### Dependencies

If you don't have **pip** installed, please start by installing it:

```
sudo aptitude install python-pip
```

After you're done, install the libraries needed by the project:

```
sudo pip install -r requirements.txt
```

## Mac OS X 10.8+

### Dependencies

If you don't have **pip** installed, please go ahead and install it:

```
sudo easy_install pip
```

After you're done, install the libraries needed by the project:

```
cd ~/Work/bbc-dev-companion
sudo pip install -r requirements.txt
```

Now, we need a nice tool to send notifications when stuff is completed. Go ahead and install [terminal-notifier](https://github.com/julienXX/terminal-notifier):

```
brew install terminal-notifier
```

## Configuration

Start by configuring the application:

```
cp config.sample.py config.py
vim config.py
```

All *workers* sit in the **workers** directory, all *admin related tools* in the **admin** folder, etc.

The configuration is very flexible and it allows you to have any name for your directories, as long as you respect the purpose of the category.

Now, let's start configuring them one by one:

* **DIR_WORK** - this is the directory where you have all of your Blablacar projects
* **DIR_CATEGORIES** - the folders where your projects reside. When you see categories think of the ones used in stash ;)   
* **REMOTE_USER** - the remote user that should be used when connection to comtools1. E.g.: anonymouse

## Alias FTW

Then, create an alias in your `~/.bashrc` or `~/.zshrc` file:
 
```
alias bbcdc='fab -f ~/Work/bbc-dev-companion/fabfile.py'
```

# Usage

Get a list of tasks that you can use:

```
bbcdc --list
```

To run a specific task:

```
bbcdc <task_name>
```

# List of tasks

**Note**: If you are in the project's folder you can use `fab` to run the tasks. Otherwise, you need to use the `bbcdc` alias.

## Build tasks
* `bbcdc build.satis` Update the composer repository using satis. 

## V3 tasks
* `bbcdc v3.fixtures` Apply the most recent fixtures to the V3 database.
* `bbcdc v3.fixtures:-h` Give an extra command/arguments to the fixtures binary. 
* `bbcdc v3.warm_up|wu` Warm up the v3 cache for the **dev** env
* `bbcdc v3.warm_up|wu:test` Warm up the v3 cache for the **test** env
* `bbcdc v3.elasticsearch|es` Reset the elastic search mappings.
* `bbcdc v3.reset` Run a reset for v3, for the **dev** env
* `bbcdc v3.reset:test` Run a reset for v3, for the **test** env
* `bbcdc v3.run_behat|rb` Init the behat containers in order to run Behat tests.
* `bbcdsc v3.worker|w` Start the *global worker* for V3.

## Worker tasks

### Locally running a worker
* `bbcdc worker.execute|e:segmentation` One command to consume queue using a worker. What it does: checkouts the **segmentation** worker, if it doesn't exist. If it does, run a `git pull`, `composer install` and a `consume` on the related queue. Timeout is set to one day.
* `bbcdc worker.execute|e:segmentation,"branch_name"` Checkout the given branch and run the worker for it.

### Remotely running a worker
* `bbcdc worker.execute_remote|er:user-id-check` Remotely consume a worker's *dl* queue **from production**.
* `bbcdc worker.execute_remote|er:user-id-check,retry_3` Remotely consume a worker's *retry_3* queue.
* `bbcdc worker.execute_remote|er:user-id-check,"dl","-m\=1 -r"` Extra options for the consume command. In this example, consume one message and return it to the queue if an error occurred.

## Command tasks

### Locally running a command
* `bbcdc command.execute|e:indexer-contact` One command to run a bbc command. Same behaviour as for the worker. It will display the available commands.  
* `bbcdc command.execute|e:indexer-contact,check:indexation` Run a specific sub command for the given command.

### Remote running
* `bbcdc command.mse:1,/tmp/ids.csv` Runs the member search export command for an ES filter id.
* `bbcdc command.execute_remote|er:total-ftp,'-h'` Run a given production command. Use the second argument, (-h in the example), to call sub commands.
 
## Service tasks

* `bbcdc service.pm:start|stop,dev|test` Control the **start** or **stop** of the private messages service, for the **dev** or **test** environments.

## Slot tasks 
* `bbcdc slot.init|i:6` Init a slot on comtools1(reserved via the mep web page), by running: `git fetch`, checking out a branch(master, if not specified) and initializing the slot.
* `bbcdc slot.init|i:6,"branch_name"` Init a slot using a given branch name.
* `bbcdc slot.init_profiling|ip:22` Initialize the profiling environment for a  given slot.
* `bbcdc slot.reinit|ri:6` Re-initialize a slot.
* `bbcdc slot.cmd:6,"composer install"` Run a given command on a specific slot.
* `bbcdc slot.errors|err` Run `tail -f` on the `php_errors.log` file on comtools1.
* `bbcdc slot.free` Get a list of free(pointed to the master branch) slots
* `bbcdc slot.free:41` Check whether a slot is free.

## Deploy tasks

**Note**: Use Ctrl + B, D to detach from the tmux session so that it's not re-created every time.

### V3
* `bbcdc deploy.v3` Deploy or finalize V3.
* `bbcdc deploy.fac` Force the  flushing of the *admin.js* and *admin.css* files in order for the UI changes pushed in production, for the Admin panel, to go live.
* `bbcdc deploy.pa3` Build and deploy PA3 containers for V3.

### Workers
* `bbcdc deploy.worker|w:user-id-check` Deploy a worker on the **dev** env.
* `bbcdc deploy.worker|w:user-id-check,preprod` Deploy a worker on the **preprod** env.
* `bbcdc deploy.worker|w:user-id-check,preprod,some_branch` Deploy a worker on the **preprod** env, using a given branch.
* `bbcdc deploy.worker_envs|we:user-id-check` Deploy a worker on all environments(dev, preprod).
* `bbcdc deploy.worker_envs|we:user-id-check,some_branch` Deploy a worker on all environments(dev, preprod), using a given branch.

### Commands
* `bbcdc deploy.command|c:user-update-linkedin-information` Deploy a command on the **dev** env.
* `bbcdc deploy.command|c:user-update-linkedin-information,preprod` Deploy a command on the **preprod** env.
* `bbcdc deploy.command_envs|ce:user-update-linkedin-information` Deploy a command on all environments(dev, preprod).

# Tasks left to do

* Add a command that generates the configuration for a project in misc and copies the new configuration files in the correct folder.
* 1st stage: Autocomplete for all projects that exist in the corresponding category folders(workers, commands, admin, micro-services) so that you can easily run a worker without manually typing its name.
* 2nd stage: Autocomplete for all projects that exist in the corresponding categories on stash(workers, commands, admin, micro-services) so that you can easily run a worker without manually typing its name.
* 3rd stage: Autocomplete for all branches of the current project(worker, command, etc.).
* Create a new project using the skeleton projects
    * gateway-dev project - add it to satis, bamboo(?)
    * worker/ command - add it to the misc folder, bamboo(?)
* Be able to tell in what projects the gateway and/or gateway-dev-* repo is used.

# Contributing

* Your suggestions are more than welcome for new tasks, new ways of improving the code etc.
* Please use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as a style guide. 

# Things to avoid

* Do not name a task **run** since it will be ran as the default one every time you intend to execute a command from a task file
* `v3.run_behat|rb` doesn't work on Mac OS X right now.
