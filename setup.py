from setuptools import setup, find_packages

setup(
    name="palo-scm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "pandas",
        "python-dotenv"
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'run-app=app.main:main',  # This allows you to run `run-app` from the terminal to execute your app
        ],
    },
)
