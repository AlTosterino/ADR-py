from adrpy.injection.modules import configure_modules
from adrpy.injection.settings import configure_settings
from injector import Inject as Inject_Injector
from injector import Injector

injector = Injector((configure_modules, configure_settings))

Inject = Inject_Injector
