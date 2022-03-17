from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erptn/__init__.py
from erptn import __version__ as version

setup(
	name="erptn",
	version=version,
	description="adaption of erpnext in the tunisian market fellowing the tunisian standards, laws and needs",
	author="amf",
	author_email="ahmed.fourati97@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
