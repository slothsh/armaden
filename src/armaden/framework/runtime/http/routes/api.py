from armaden.framework.facades import Route
from ..controllers import LifecycleController

# -- Lifecycle Routes ---------------------------------------------------------

Route.get("/health", LifecycleController, 'health')
Route.post("/restart", LifecycleController, 'restart')
Route.post("/shutdown", LifecycleController, 'shutdown')
