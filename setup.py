import setuptools

setuptools.setup(
    name="pylamost",
    version="0.1.0",
    py_modules=["pylamost"],
    install_requires=[
        'requests',
        'astropy',
        'numpy',
        'scipy',
        'matplotlib',
    ],
)
