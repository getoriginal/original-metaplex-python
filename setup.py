from setuptools import find_packages, setup

setup(
    name="original_metaplex_python",
    version="0.0.1-alpha",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
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
    ],
)
