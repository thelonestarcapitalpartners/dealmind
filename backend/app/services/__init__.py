"""Service package exports. Keep optional imports guarded so tests can run without optional deps."""
try:
	from app.services import auth_service
except Exception:
	auth_service = None
try:
	from app.services import calculator
except Exception:
	calculator = None

try:
	from app.services import deal_service
except Exception:
	deal_service = None

try:
	from app.services import underwriting_service
except Exception:
	underwriting_service = None

try:
	from app.services import extraction_service
except Exception:
	extraction_service = None
