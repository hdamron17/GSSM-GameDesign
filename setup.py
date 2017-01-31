from setuptools import setup

setup(
    name='footsteps',
    version='0.1.dev0',
    author='Hunter Damron',
    packages=['footsteps', ],
    description="A simple ASCII art game for my game design class",
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'footsteps = footsteps.__main__:wrapped_main'
        ]
    },
)

### run ```python3 setup.py sdist bdist_wheel --universal``` and ```twine upload dist/*``` to upload to pypi
