from setuptools import find_packages, setup

setup(
    name="original_metaplex_python",
    version="0.0.1-alpha",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.9.3",
        "aiosignal>=1.3.1",
        "anchorpy-core>=0.1.3",
        "anyio>=4.3.0",
        "async-timeout>=4.0.3",
        "attrs>=23.2.0",
        "solana>=0.30.2",
        "anchorpy>=0.18.0",
        "construct>=2.10.68",
        "borsh-construct>=0.1.0",
        "construct-typing>=0.5.6",
        "ed25519>=1.5",
        "jsonrpcclient>=4.0.3",
        "pynacl>=1.5.0",
        "requests>=2.31.0",
        "types-requests>=2.31.0.20240218",
    ],
)
