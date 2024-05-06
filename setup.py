import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# TODO: fix this
setuptools.setup(
     # this line doesn't work as intended
     #scripts=['src/pyson_data'],
     author="josh-co-dev",
     description="Provides support for storing data in .pyson format",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/OmegaGodzilla66/PYSON",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
