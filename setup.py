from setuptools import find_packages, setup

install_requires = [
    "aiohttp>=3.9.3,<4.0",
    "aiosignal>=1.3.1,<2.0",
    "anchorpy-core>=0.2.0,<0.3.0",
    "anyio>=4.3.0,<5.0",
    "async-timeout>=4.0.3,<5.0",
    "attrs>=23.2.0,<24.0",
    "solana>=0.32.0,<0.33.0",
    "anchorpy>=0.19.1,<0.20.0",
    "construct>=2.10.68,<3.0",
    "borsh-construct>=0.1.0,<0.2.0",
    "construct-typing>=0.5.6,<0.6.0",
    "ed25519>=1.5,<2.0",
    "jsonrpcclient>=4.0.3,<5.0",
    "pynacl>=1.5.0,<2.0",
    "requests>=2.31.0,<3.0",
    "types-requests>=2.31.0.20240218,<3.0",
]

tests_require = ["pytest", "pytest-asyncio<=0.21.1", "python-dotenv"]
ci_require = [
    "black",
    "flake8",
    "flake8-isort",
    "flake8-bugbear",
    "pytest-cov",
    "mypy",
    "types-requests",
]

with open("README.md", "r") as f:
    long_description = f.read()

about: dict = {}

with open("original_metaplex_python/__pkg__.py") as fp:
    exec(fp.read(), about)

setup(
    name="original_metaplex_python",
    version=about["__version__"],
    author=about["__maintainer__"],
    author_email=about["__email__"],
    url="https://github.com/getoriginal/original-metaplex-python",
    description="Python port of Metaplex JS SDK - https://github.com/metaplex-foundation/js",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["*tests*"]),
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"test": tests_require, "ci": ci_require},
    include_package_data=True,
    python_requires=">=3.7",
)
