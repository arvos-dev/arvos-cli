from setuptools import setup, find_packages


with open("readme.rst", "r") as f:
    readme = f.read()

setup(
    name="arvos",
    version="1.0.3",
    description="Arvos Command Line Helper",
    long_description=readme,
    author='Ayoub ED-DAFALI',
    author_email='ayoub.eddafali@elastisys.com',
    packages=find_packages('src'),
    package_dir={'':'src'},
    setup_requires=[],
    install_requires=["docker", "mako"],
    entry_points={
        'console_scripts': ['arvos=arvos.cli:main'],
    }
)


