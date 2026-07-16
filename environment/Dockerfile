FROM python:3.9-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/pylint-dev/pylint.git /app \
    && cd /app \
    && git checkout 0a4204fd7555cfedd43f43017c94d24ef48244a5


RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install \
        "astroid==2.11.4" \
        "typing-extensions~=4.2" \
        "pytest~=7.1" \
        "pytest-timeout~=2.1" \
        "GitPython>3" \
        "dill>=0.2" \
        "platformdirs>=2.2.0" \
        "isort>=4.2.5,<6" \
        "mccabe>=0.6,<0.8" \
        "tomli>=1.1.0" \
        "tomlkit>=0.10.1" \
    && python -m pip install -e .

WORKDIR /app
