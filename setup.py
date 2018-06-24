import setuptools

setuptools.setup(
    name='pycommon',
    version='0.0.1',
    author='Christopher Brown',
    author_email='io@henrian.com',
    description='General purpose Python programming modules',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chbrown/pycommon',
    license='MIT',
    packages=setuptools.find_packages(),
)
