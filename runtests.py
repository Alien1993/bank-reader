import os
import sys
import pytest

# add here your folders to the PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "django-bank-reader"))

sys.exit(pytest.main())
