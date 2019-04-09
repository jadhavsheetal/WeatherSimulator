from setuptools import setup
import versioneer

requirements = [
    "pandas==0.24.2",
	"scikit-learn==0.20.3",
	"nltk==3.2.5"
]

setup(
    name='WeatherSimulator',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Generate Fake Weather Data primarily of US/Canadian cities",
    author="Sheetal Jadhav",
    author_email='jadhavsheetal@gmail.com',
    url='https://github.com/jadhavsheetal/WeatherSimulator',
    packages=['weathersimulator'],
    entry_points={
        'console_scripts': [
            'weathersimulator=weathersimulator.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='WeatherSimulator',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
