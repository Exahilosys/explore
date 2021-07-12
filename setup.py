import setuptools

with open('README.rst') as file:

    readme = file.read()

name = 'explore'

version = '1.0.0'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Scoring and best match picking.',
    long_description = readme
)
