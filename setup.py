import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='pyson_data',
     version='0.0.3',
     scripts=['pyson_data'],
     author="ComputingSquid",
     description="Provides support for storing data in .pyson format",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/ProbablyComputingSquid/PYSON",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )