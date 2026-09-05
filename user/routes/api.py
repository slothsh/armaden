from armaden.framework.facades import RouteFacade
from app.http.controllers.lifecycle_controller import LifecycleController
from app.http.controllers.rcon_controller import RconController

_ = RouteFacade.get('/health', (LifecycleController, 'health'))
_ = RouteFacade.post('/restart', (LifecycleController, 'restart'))
_ = RouteFacade.post('/shutdown', (LifecycleController, 'shutdown'))
_ = RouteFacade.get('/rcon/players', (RconController, 'players'))
_ = RouteFacade.get('/rcon/restart', (RconController, 'restart'))
