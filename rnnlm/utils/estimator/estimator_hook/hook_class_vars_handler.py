from rnnlm.utils.global_var_manager import GlobalVarManager
from rnnlm.utils.estimator import estimator_hook
import inspect
import importlib
import os
import logging.config


import yaml

from rnnlm import config as rnnlm_config

logging.config.dictConfig(yaml.load(open(rnnlm_config.LOGGING_CONF_PATH, 'r')))
logger = logging.getLogger('rnnlm.utils.estimator.estimator_hook.hook_class_vars_handler')


class HookClassVarsHandler:

    def __init__(self):
        hooks_dir = 'rnnlm/utils/estimator/estimator_hook'
        files = os.listdir(hooks_dir)
        callable_classes = list()
        logger.info('loading hooks from {}'.format(hooks_dir))
        for f in files:
            if not f.startswith('_') and f != os.path.basename(__file__):
                f = f.replace('.py', '')
                train_hook = importlib.import_module(name="." + f, package=estimator_hook.__name__)
                class_name = inspect.getmembers(train_hook, inspect.isclass)[0][0]
                callable_class = getattr(train_hook, class_name)
                callable_classes.append(callable_class)
        self.gvm = None
        logger.debug('found hook classes {}'.format(callable_classes))
        self.load(callable_classes)

    def load(self, callable_classes):
        d = dict()
        for cl in callable_classes:
            attributes = inspect.getmembers(cl, lambda x: not (inspect.isroutine(x)))
            for a in attributes:
                if not (a[0].startswith('_') or a[0].endswith('_')):
                    unique_name = cl.__name__ + "." + a[0]
                    value = a[1]
                    d[unique_name] = value
        logger.debug('hook classes vars: {}'.format(d))
        self.gvm = GlobalVarManager(d)

    def add(self, class_name, var_name, var_initial_value):
        unique_name = class_name + "." + var_name
        self.gvm.add({unique_name: var_initial_value})

    def remove(self, class_name, var_name):
        unique_name = class_name + "." + var_name
        self.gvm.remove([unique_name])

    def reset(self, class_name, var_name):
        unique_name = class_name + "." + var_name
        self.gvm.reset_one(unique_name)

    def reset_all(self):
        logger.debug('resetting hook classes vars to their initial values')
        self.gvm.reset_all()
