from armaden.framework.facades import Route
from app.http.controllers.lifecycle_controller import LifecycleController

Route.get('/health', [LifecycleController, 'health'])
Route.post('/restart', [LifecycleController, 'restart'])
Route.post('/shutdown', [LifecycleController, 'shutdown'])