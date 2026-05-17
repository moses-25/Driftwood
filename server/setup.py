from setuptools import setup, find_packages

setup(
    name="driftwood-cafe-backend",
    version="1.0.0",
    description="Backend API for Driftwood Café - A modern coffee shop management system",
    author="Driftwood Café Team",
    author_email="dev@driftwoodcafe.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Flask==3.0.0",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-Migrate==4.0.5",
        "Flask-CORS==4.0.0",
        "psycopg2-binary==2.9.9",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "gunicorn==21.2.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-flask==1.3.0",
            "black==23.11.0",
            "flake8==6.1.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)