from setuptools import setup, find_packages

setup(
    name='tapestryflow',
    version='0.1.0',
    description='TapestryFlow integrates SnapLog and other flow management tools.',
    author='Tu nombre',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'pillow',
        'python-dotenv',
        'tkinter',
    ],
)
