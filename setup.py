import importlib.util
from pathlib import Path
from setuptools import setup, find_packages

pwd = Path(__file__).parent
spec = importlib.util.spec_from_file_location(
    'eips_exposed',
    Path().cwd().joinpath('eips_exposed/__init__.py')
)
assert spec is not None
eips_exposed_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eips_exposed_init)

# Get the long description from the README file
with open(pwd.joinpath('README.md'), encoding='utf-8') as f:
    long_description = f.read()


def requirements_to_list(filename):
    return [dep for dep in open(pwd.joinpath(filename)).read().split('\n') if (
        dep and not dep.startswith('#')
    )]


setup(
    name='eips_exposed',
    version=eips_exposed_init.__version__,
    description='Solidity development tools for creating Ethereum smart contracts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikeshultz/eips.exposed',
    author=eips_exposed_init.__author__,
    author_email=eips_exposed_init.__email__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ethereum development eip improvement proposal',
    packages=find_packages(exclude=['docs', 'tests', 'scripts', 'build']),
    install_requires=requirements_to_list('requirements.txt'),
    extras_require={
        'dev': requirements_to_list('requirements.dev.txt'),
    },
    entry_points={
        'console_scripts': [
            'ee-processor=eips_exposed.processor.main:main',
            'ee-server=eips_exposed.server.main:main',
        ],
    },
    package_data={
        '': [
            'README.md',
            'LICENSE',
        ],
    },
)
