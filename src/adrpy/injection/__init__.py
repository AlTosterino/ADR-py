from adrpy.injection.modules import configure_modules
from injector import Inject as Inject_Injector
from injector import Injector

injector = Injector((configure_modules,))

Inject = Inject_Injector
