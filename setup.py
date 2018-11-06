from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name         = 'lifester',
    version      = '1.2.0',
    author       = 'Sophie Au',
    author_email = 'some.person@web.de',
    license      = 'MIT',
    description  = 'Every minute of your life. On the command line.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords     = ['command-line-tool', 'productivity'],
    url          = 'https://github.com/sophieau/lifester',

    packages     = ['lifester'],
    zip_safe     = False,
    entry_points = {
        'console_scripts': ['lifester=lifester.__main__:main'],
    },
    python_requires  = '>=3.6',
    install_requires = [
        'tabulate >= 0.8.2',
    ]
)
