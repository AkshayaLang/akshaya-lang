from setuptools import setup, find_packages

setup(
    name="akshayalang",
    version="1.0.0",
    description="AkshayaLang — a sovereign symbolic programming language",
    author="D.V.S. Siva Chandra Raju",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "aks = akshayalang.repl:start_repl"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)