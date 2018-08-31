import os
from distutils.core import setup


PROJECT_DIR = os.path.dirname(__file__)

if PROJECT_DIR:
    os.chdir(PROJECT_DIR)

setup(
    name='boop',
    version='0.1.0',
    description='Image Manipulation and Generation',
    long_description=open(os.path.join(PROJECT_DIR, "README.md")).read(),
    author='Sarah Lynch',
    author_email='sarahlynch@fastmail.com',
    packages=['boop'],
    install_requires=open(os.path.join(PROJECT_DIR, "requirements.txt")).read(),
)
