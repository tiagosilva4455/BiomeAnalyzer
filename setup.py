from setuptools import setup, find_packages

setup(
    name='biomeanalyzer',
    version='0.0.1',
    python_requires='>=3.9',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=['numpy', 'pandas'],
    author='',
    author_email='',
    description='BiomeAnalyzer is a Python package for analyzing microbiome data.',
)