import os
import sys
import compas

print()
print('system')
print('------')
print(sys.version_info)
print()
print('conda')
print('-----')
print(os.getenv('CONDA_DEFAULT_ENV'))
print(os.getenv('CONDA_PREFIX'))
print()
print('COMPAS')
print('-----')
print(compas.__version__)
