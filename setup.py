from setuptools import setup, find_packages

setup(
    name="palo-scm",
    version="0.1.0",
    packages=find_packages(include=['scm', 'app', 'app.processors']),
    install_requires=[
        "httpx",
        "pandas",
        "python-dotenv"
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-app=app.main:main',  # Ensure this points to the correct module
        ],
    },
)
