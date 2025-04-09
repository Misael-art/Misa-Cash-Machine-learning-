from setuptools import setup, find_packages

setup(
    name="misa_cash",
    version="0.1.0",
    description="Sistema de gerenciamento financeiro com recursos de Machine Learning",
    author="Misael",
    author_email="misael@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "flask-sqlalchemy>=2.5.0",
        "flask-restful>=0.3.9",
        "pytest>=6.0.0",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
            "flake8",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 