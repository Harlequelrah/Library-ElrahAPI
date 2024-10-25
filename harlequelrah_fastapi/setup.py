from setuptools import setup, find_packages

setup(
    name="harlequelrah_fastapi",
    version="0.5.5",
    packages=find_packages(),
    description="Package personnalisé pour faciliter  le développement avec python avec fastapi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Harlequelrah",
    author_email="maximeatsoudegbovi@example.com",
    url="https://github.com/Harlequelrah/Library-harlequelrah_fastapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["fastapi[standard]>=0.112.0", "alembic>=1.13.3","virtualenv>=20.26.6","mysql-connector-python>=9.0.0"],
    entry_points={"console_scripts": ["harlequelrah_fastapi=harlequelrah_fastapi.__main__:main"]},
)
