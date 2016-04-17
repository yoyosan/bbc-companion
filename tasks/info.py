from library.common import *


@task(alias="v")
def version():
    """
    \033[94mDisplay version.\033[0m \033[0m \033[92mUsage:\033[0m \033[93mbbcdc info.version|v\033[0m
    """
    print('\033[92mVersion:\033[0m ' + VERSION)
