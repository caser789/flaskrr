from setuptools import setup

setup(
        name='flaskr',
        packages=['flaskr'],
        include_package_data=True,
        install_requires=['flask', 'pyyaml'],
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        )