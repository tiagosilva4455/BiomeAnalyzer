from setuptools import setup, find_packages

setup(
    name='biomeanalyzer',
    version='0.1.0',
    python_requires='>=3.9',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={'biomeanalyzer': ['data/rrnDB-5.9_pantaxa_stats_NCBI.tsv', 'data/taxonomy.tsv']},
    zip_safe=False,
    install_requires=['numpy', 'pandas', 'scipy', 'tqdm', 'requests'],
    author='',
    author_email='',
    description='BiomeAnalyzer is a Python package for analyzing microbiome data.',
)


