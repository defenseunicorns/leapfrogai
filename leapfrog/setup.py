from setuptools import setup, find_packages

setup(
    name='leapfrog',    # This is the name of your PyPI-package.
    version='0.1',               # Update the version number for new releases.
    packages=find_packages(),    # This finds all packages (and sub-packages) in the current directory.
    install_requires=[           # Add your project dependencies here.
        # 'requests',
        # 'numpy',
    ],
    author='Tom Runyon and Gerred Dillon',
    author_email='ai@defenseunicorns.com',
    description='A brief description of your project',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',  # This is important if your README is in markdown
    url='https://github.com/defenseunicorns/leapfrogai',  # Link to the github or other repository
)