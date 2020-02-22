from setuptools import setup
import versioneer

requirements = [
    'sortedcontainers',
    'pandas',
    'numpy'
]

setup(
    name='staircase',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Modelling of quantitative state changes as step functions",
    license="MIT",
    author="Riley Clement",
    author_email='venaturum@gmail.com',
    url='https://github.com/venaturum/staircase',
    packages=['staircase'],
    
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