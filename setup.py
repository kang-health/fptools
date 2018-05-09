from setuptools import setup

setup(
    name='fptools',
    version='0.2.2',
    description='Functional programming tools for Python',
    url='https://github.com/kang-health/fptools',
    author='Iddan Aaronsohn',
    author_email='iddan@khealth.ai',
    packages=['fptools'],
    install_requires=[
        'cardinality',
    ],
    platforms="any",
)
