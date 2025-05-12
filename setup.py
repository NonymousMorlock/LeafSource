from setuptools import setup, find_packages

setup(
    name="library-cli",
    version="0.1.0",
    author="Your Name",
    description="A simple command‐line library management tool",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "passlib[bcrypt]==1.7.4",
        "bcrypt==3.2.2",
        "SQLAlchemy==2.0.40",
        "typer==0.15.3",
        "click==8.0.4",
    ],
    entry_points={
        "console_scripts": [
            # now `library` will be your CLI entry point
            "library = leafsource.cli.main:app",
        ],
    },
)
