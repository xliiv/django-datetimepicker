from setuptools import setup


setup(
    name='django-bootstrap3-datetimepicker',
    packages=['bootstrap3_datetime',],
    package_data={'bootstrap3_datetime': ['static/bootstrap3_datetime/css/*.css', 
                                          'static/bootstrap3_datetime/js/*.js',
                                          'static/bootstrap3_datetime/js/locales/*.js',]},
    include_package_data=True,
    version='2.3.1',
    description='Bootstrap3 compatible datetimepicker for Django projects.',
    long_description=open('README.rst').read(),
    author='Pablo Escodebar',
    author_email='escodebar@gmail.com',
    url='https://github.com/escodebar/django-bootstrap3-datetimepicker.git',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
