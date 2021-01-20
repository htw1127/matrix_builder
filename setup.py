from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='sparse_matrix_builder',
    version='0.0.1',
    description='This program is intended to build sparse matrices in a more intuitive GUI environment.',
    url='',
    author='Taewoo Han',
    author_email='htw1127@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='matrix',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'tk']
)