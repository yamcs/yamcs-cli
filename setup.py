import io

import setuptools

with io.open("README.md", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="yamcs-cli",
    version="1.4.3",
    description="Yamcs Command-Line Tools",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/yamcs/yamcs-cli",
    author="Space Applications Services",
    author_email="yamcs@spaceapplications.com",
    license="LGPL",
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["yamcs = yamcs.cli.__main__:main"]},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    platforms="Posix; MacOS X; Windows",
    install_requires=["yamcs-client>=1.7.0"],
    extras_require={"kerberos": ["yamcs-client-kerberos>=1.2.0"]},
    include_package_data=True,
    zip_safe=False,
)
