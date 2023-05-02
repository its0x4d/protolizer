import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protolizer",
    version="1.2.0",
    author='MosyDev',
    author_email='mostafa.uwsgi@gmail.com',
    description='A simple library to serialize and deserialize protobuf messages',
    url='https://github.com/its0x4d/protolizer',
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='protobuf serialization deserialization',
)
