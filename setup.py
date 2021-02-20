from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        readme_file = f.read()
    return readme_file


classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='sparse-matrix-builder',
    version='0.0.5',
    description='This program is intended to build sparse matrices in a more intuitive GUI environment.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/htw1127/matrix_builder',
    author='Taewoo Han',
    author_email='htw1127@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='matrix',
    packages=['builder'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "build-matrix=builder.__main__:main",
        ]
    }
)