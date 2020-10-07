from __future__ import print_function

import sys
import compas

from compas_bootstrapper import ENVIRONMENT_NAME, PYTHON_DIRECTORY, INSTALLED_PACKAGES

print()
print('system')
print('------')
print(sys.version_info)
print()
print('conda')
print('-----')
print(ENVIRONMENT_NAME)
print(PYTHON_DIRECTORY)
print()
print('COMPAS')
print('-----')
print(INSTALLED_PACKAGES)
print(compas.__version__)
