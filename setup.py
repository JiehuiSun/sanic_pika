# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name="sanic_pika",
    version="0.1.0",
    author="huihui",
    author_email="sunjiehuimail@foxmail.com",
    description="sanic pika",
    long_description="sanic asyncio pika rabbitMQ",
    long_description_content_type="text/markdown",
    url="https://github.com/JiehuiSun/sanic_pika",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO"
    ],
    install_requires=[
        "sanic>=21.12.1"
        "apika>=0.1.2"
    ],
    python_requires=">=3.8"

)
