import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='battleships-pkg-klar',
    version='1.0.2',
    author='Jake Klar',
    author_email='jk733@exeter.ac.uk',
    description='The classic Battleship game implemented in Python. Singleplayer and multiplayer as well as option GUI version',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/imferolla/battleships',
    packages=setuptools.find_packages(),
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)