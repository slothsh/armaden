from armaden.framework.facades import Route
from ..controllers import LifecycleController

Route.get('/health', [LifecycleController, 'health'])
Route.post('/restart', [LifecycleController, 'restart'])
Route.post('/shutdown', [LifecycleController, 'shutdown'])
