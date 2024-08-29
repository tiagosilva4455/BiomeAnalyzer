from setuptools import setup, find_packages

setup(
    name='biomeanalyzer',
    version='0.0.4',
    python_requires='>=3.9',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={'biomeanalyzer': ['data/rrnDB-5.8_pantaxa_stats_NCBI.tsv', 'data/taxonomy.tsv']},
    zip_safe=False,
    install_requires=['numpy', 'pandas', 'scipy'],
    author='',
    author_email='',
    description='BiomeAnalyzer is a Python package for analyzing microbiome data.',
)
