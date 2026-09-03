from armaden.framework.runtime.kernel import bootstrap_http
from returns.pipeline import is_successful

result = bootstrap_http()
if not is_successful(result):
    raise SystemExit(1)
