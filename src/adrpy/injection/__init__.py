from injector import Inject as Inject_Injector
from injector import Injector

from adrpy.injection.modules import configure_modules

injector = Injector((configure_modules,))

Inject = Inject_Injector
