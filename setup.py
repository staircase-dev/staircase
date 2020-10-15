from setuptools import setup
import versioneer

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
requirements = [
    'sortedcontainers>=2,<3',
    'pandas>=0.24,<2',
    'numpy>=1.16.0,<2',
    'matplotlib>3.0.0,<4'
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
    keywords=[
        'Staircase',
        'Step Functions',
        'Mathematics', 
        'Data Analysis',
        'Analysis',
        'Data Structures',
        'Time Signal',
        'Simulation Output',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
