from distutils.core import setup
from setuptools import find_packages


setup(name='barracks',
      version='1.0',
      description='web admin framework barracks',
      author="Xiang Shu",
      author_email="xshu@bainainfo.com",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      install_requires=[])
