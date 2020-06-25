import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mongo Tasks",
    version="0.1.2",
    author="Pedro Havay",
    author_email="pedrohavay@protonmail.com",
    description="A Python Project to manage tasks queue using MongoDB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrohavay/mongo-tasks",
    packages=setuptools.find_packages(),
    install_requires=[
        "pymongo==3.10.1",
        "python-dotenv==0.13.0"
    ]
)
