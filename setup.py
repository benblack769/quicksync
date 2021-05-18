import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quicksync",
    version="0.1",
    author="Benjamin Black",
    author_email="benblack769@gmail.com",
    description="A data synchronization tool designed for remote desktop work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benblack769/quicksync",
    keywords=["Remote Desktop", "rsync"],
    packages=["quicksync"],
    install_requires=["pyyaml"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/backward_sync', 'bin/forward_sync'],
    include_package_data=True,
)
