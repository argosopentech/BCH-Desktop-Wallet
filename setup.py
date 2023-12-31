from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="BCHDesktopWallet",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bch-desktop-wallet = bchdesktopwallet.wallet:main",
        ],
    },
)
