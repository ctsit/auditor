from setuptools import setup

setup(name='auditor',
      version='1.2.0',
      description='Makes sure your CSV data is complian.',
      url='http://github.com/pfwhite/auditor',
      author='Patrick White',
      author_email='pfwhite9@gmail.com',
      license='Apache2.0',
      packages=['auditor'],
      entry_points={
          'console_scripts': [
              'auditor = auditor.__main__:main',
          ],
      },
      install_requires=[
          'docopt==0.6.2',
          'pyyaml==3.12',
          'python-dateutil==2.6.1'],
      zip_safe=False)
