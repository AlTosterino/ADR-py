from adrpy.injection.modules import RepositoryModules, ServiceModules
from adrpy.injection.settings import configure_settings
from injector import Inject as Inject_Injector
from injector import Injector

injector = Injector((configure_settings, RepositoryModules(), ServiceModules()))

Inject = Inject_Injector
