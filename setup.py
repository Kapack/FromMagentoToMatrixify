from distutils.core import setup
from setuptools import find_packages

setup(
  name="FromMagentoToMatrixy",  
  version="1.0.0",
  description="Converts Magento export sheet to Matrixify Import sheet",
  author="Kasper Kloster",
  author_email='kasper@wepack.se',
  python_requires='>=3, <4', 
  # package_dir = {'' : 'src'}, 
  install_requires=[
    'slugify==0.0.1',
    'python-slugify==6.1.2',
    'pandas >= 1.5.1',
  ],

  entry_points={
        'console_scripts': [
            'cli = FromMagentoToMatrixify.src.main:Main',
        ]
    }
)
