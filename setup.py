from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='oref',
    version='0.1.0',
    url='https://github.com/emrothenberg/oref',
    description="Unofficial API for the Israeli Home Front Command",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='emrothenberg',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='oref, homefront, home front, pikud, haoref, rockets, missiles, tzeva adom, emergency, api, idf, israel, israeli, alerts, red alert, sirens, civil defense, air raid, public safety, realtime, defense, national alert, region alerts, security',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.31',
    ]
)
