"""pyiqoapi is a python wrapper for IQOption's API."""
from setuptools import setup, find_packages

version = '0.2.0'

setup(name='pyiqoapi',
      version=version,
      description="pyiqoapi is a python wrapper for IQOption's API.",
      long_description="""\
""",
      classifiers=[
          # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Intended Audience :: Financial and Insurance Industry'
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='IQOption binary option wrapper REST API',
      author='angelocarbone',
      author_email='api@magmati.co',
      url='http://pyiqoapi.magmati.co/',
      license='MIT',
      packages=find_packages(exclude=['examples', 'tests']),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests',
          'websocket-client'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
