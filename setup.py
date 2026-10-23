from setuptools import find_namespace_packages, setup

setup(
    name="cli-anything-bps",
    version="1.0.0",
    description="Agent-Native CLI Suite & Antigravity Skill for Badan Pusat Statistik (BPS) Indonesia",
    long_description="Deterministic, token-efficient research harness and data availability auditor for BPS Web API.",
    author="CLI-Anything & Antigravity Community",
    python_requires=">=3.10",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "prompt-toolkit>=3.0",
        ],
    },
    package_data={
        "cli_anything.bps": ["*.md", "skills/*.md", "references/*.md"],
    },
    entry_points={
        "console_scripts": [
            "bps=cli_anything.bps.bps_cli:main",
            "cli-anything-bps=cli_anything.bps.bps_cli:main",
        ],
    },
)
