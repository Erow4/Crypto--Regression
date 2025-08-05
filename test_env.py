# File Description: This files just tests the new virtual environment

try:
    import numpy
    import pandas
    import requests

    print("✅ All libraries imported successfully!\n")
    print(f"numpy version   : {numpy.__version__}")
    print(f"pandas version  : {pandas.__version__}")
    print(f"requests version: {requests.__version__}")

except ImportError as e:
    print(f"❌ Import failed: {e}")
