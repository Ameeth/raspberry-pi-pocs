from setuptools import setup

setup(
    name='home',
    packages=['home'],
    include_package_data=True,
    install_requires=[
        'flask', 'flask-bootstrap','flask-nav'
        ,'RPi.GPIO','py-irsend'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
