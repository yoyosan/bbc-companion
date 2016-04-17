# Changelog

# 1.2
* New tasks
    * `deploy.pa3` will build and deploy pa3 containers
    * Update configuration to include PA3 hosts and directories

# 1.1.1
* Fixes
    * Fix incorrect condition for env, for `service.pm` task
    * Remove tmux session kill for a non-existent session

# 1.1
* New tasks
    * Display the free slots or check whether a slot is free  
    * Display a slot URL after init or reinit is done
    * Add V3 RabbitMQ reset
    * Add version task
    * **start/stop** private messages daemon for **dev/test**
    * Execute production commands
* Fixes
    * Handle the problems with the V3 task being stuck when mep blocks. You can now
    run the finalize task to send a **Ctrl-C** to the existing deployment session.
* Refactor
    * `boot_in_tmux_session` now became `run_in_tmux_session` and allows to execute
    both local(by using `run_in_local_tmux_session`) and remote commands
    * add `throw_error` to abort the task with an error message
* Add change log

# 1.0

Initial release and e-mail announcement to the tech mailing list.
