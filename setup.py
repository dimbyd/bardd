from setuptools import setup

setup(
    name='bardd',
    version='0.2',
    description='Meddalwedd Cynganeddol',
    url='http://github.com/dimbyd/bardd',
    author='dimbyd',
    author_email='dimbyd@cerigos.com',
    license='MIT',
    packages=['bardd'],
    install_requires=['lxml', 'unidecode'],
    entry_points={
        'console_scripts': ['bardd=bardd.main:main'],
    },
    include_package_data=True,
    zip_safe=False,
)
