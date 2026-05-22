import importlib
import sys

modules = [
    'app.services.extraction_service',
    'app.services.underwriting_service',
    'app.services.deal_service',
    'app.services.auth_service',
    'app.api.deals',
    'app.api.underwriting',
    'app.api.auth',
    'app.main',
]

results = []
for m in modules:
    try:
        importlib.import_module(m)
        results.append((m, 'OK'))
    except Exception as e:
        results.append((m, f'ERROR: {e.__class__.__name__}: {e}'))

for r in results:
    print(f"{r[0]:<40} -> {r[1]}")

# exit non-zero if any error
if any('ERROR' in r[1] for r in results):
    sys.exit(2)
