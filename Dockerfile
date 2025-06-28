# Use the official Ubuntu 24.04 LTS (Noble Numbat) as the base image.
FROM ubuntu:24.04

# Set environment variables for non-interactive installation.
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Set the working directory.
WORKDIR /app

# Pre-accept the Microsoft Fonts EULA to ensure a smooth installation.
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

# Install system dependencies.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-is-python3 \
    libcairo2-dev \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    pkg-config \
    imagemagick \
    fonts-dejavu-core \
    fonts-liberation \
    ttf-mscorefonts-installer \
    fontconfig \
    xfonts-utils && \
    # Rebuild the system's font cache.
    fc-cache -f -v && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy our custom, more permissive ImageMagick policy file.
COPY custom-policy.xml .

# This robustly copies the policy to the correct location for IMv6 and/or IMv7,
# ensuring the policy is applied whether 'convert' or 'magick' is called.
RUN if [ -d /etc/ImageMagick-7 ]; then cp custom-policy.xml /etc/ImageMagick-7/policy.xml; fi && \
    if [ -d /etc/ImageMagick-6 ]; then cp custom-policy.xml /etc/ImageMagick-6/policy.xml; fi

# Set the environment variable for MoviePy.
ENV IMAGEMAGICK_BINARY="/usr/bin/convert"

# Copy and install Python dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Set the default entrypoint to an interactive shell.
CMD ["bash"]