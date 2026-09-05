from armaden.framework.facades import RouteFacade
from app.http.controllers.lifecycle_controller import LifecycleController

_ = RouteFacade.get('/health', (LifecycleController, 'health'))
_ = RouteFacade.post('/restart', (LifecycleController, 'restart'))
_ = RouteFacade.post('/shutdown', (LifecycleController, 'shutdown'))