from setuptools import setup
def fread(fname,lines=False,bytes=False):
    with open(fname,'rb' if bytes else 'r') as f:
        res = f.readlines() if lines else f.read()
    return res
setup(
   name='chb-mit',
   version='0.1.0',
   author='Doug Koch, Misha Klopukh',
   author_email='misha@mpcrlab.com',
   packages=['chbdata'],
   url='https://github.com/dougkoch/chb-mit',
   license='LICENSE.txt',
   description='CHB-MIT scalp EEG dataset helpers',
   long_description=fread('README.md'),
   install_requires=fread('requirements.txt',lines=True),
)