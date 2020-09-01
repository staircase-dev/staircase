from setuptools import setup
import versioneer

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
requirements = [
    'sortedcontainers>=2,<=2.2.2',
    'pandas>=0.24',
    'numpy>=1.16.0',
    'matplotlib>3.0.0'
]

setup(
    name='staircase',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Modelling of quantitative state changes as step functions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    author="Riley Clement",
    author_email='venaturum@gmail.com',
    url='https://github.com/venaturum/staircase',
    packages=['staircase', 'staircase.docstrings'],
    python_requires='>=3.6',
    install_requires=requirements,
    keywords=['Staircase',
			'Step Functions',
			'Data Analysis',
			'Intervals',
			'Simulation'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
