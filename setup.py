from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="elrahapi",
    version="1.0.4",
    packages=find_packages(),
    description="Framework de développement d'API basé FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Harlequelrah",
    author_email="maximeatsoudegbovi@example.com",
    url="https://github.com/Harlequelrah/Library-ElrahAPI",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi[standard]>=0.112.0",
        "alembic>=1.13.3",
        "argon2-cffi>=23.1.0",
        "python-dotenv>=1.0.1",
        "python-jose[cryptography]>=3.3.0",
        "black>=24.10.0",
        "sqlalchemy>=2.0.38",
        "sqlalchemy-utils>=0.41.2"
    ],
    entry_points={"console_scripts": ["elrahapi=elrahapi.__main__:main"]},
)
