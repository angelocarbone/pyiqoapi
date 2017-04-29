# pyiqoapi

_pyiqoapi_ is a python wrapper for IQOption's API.

# Install

Using pip:

    $ pip install git+https://github.com/angelocarbone/pyiqoapi.git

_pyiqoapi_ depends to some packages, which will be installed automatically.

# Usage

Include the _pyiqoapi_ module and create an _pyiqoapi_ instance with your account credentials.

	import pyiqoapi

	api = pyiqoapi.PyiqoAPI(username="yourusername", password="yoursecret")
	api.connect()
