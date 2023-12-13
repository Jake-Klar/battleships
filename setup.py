from setuptools import setup, find_packages

setup(
    name='Battleships',
    version='1.0.0',
    description='The classic Battleship game implemented in Python. Singleplayer and multiplayer as well as option GUI version',
    author='Jake Klar',
    license='MIT',
    url='https://github.com/imferolla/battleships',
    packages=find_packages(),
    install_requires=[
        'Flask'
    ]
)