# use catkin to run

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch package.xml values
setup_args = generate_distutils_setup(
    packages=['turtle_handlers'],
    package_dir={'':'src'},
)

setup(**setup_args)
