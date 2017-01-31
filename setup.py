from setuptools import setup

#Find last version string which is not empty
versions = open('versions.txt').read().split('\n')
for ver in reversed(versions):
	if ver != '':
		latest_version = ver
		break

setup(
    name='footsteps',
    version=latest_version,
    author='Hunter Damron',
    author_email="hdamron1594@yahoo.com",
    url="https://github.com/hdamron17/Footsteps",
    packages=['footsteps', ],
    description="A simple ASCII art game for my game design class",
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'footsteps = footsteps.__main__:wrapped_main'
        ]
    },
)

### run ```python3 setup.py sdist bdist_wheel --universal``` and ```twine upload dist/*``` to upload to pypi
