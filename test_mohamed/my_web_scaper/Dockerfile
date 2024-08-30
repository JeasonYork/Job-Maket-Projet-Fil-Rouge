FROM python:3.12-bookworm

# Install necessary packages
RUN pip install playwright==1.44.0 && \
                           playwright install --with-deps

# Install additional Python libraries
                           RUN pip install selectolax logging validator fake-useragent httpx aiofiles pandas

# Create directories for data and logs
                           RUN mkdir -p /app/data /app/logs

# Set the working directory
                           WORKDIR /app

# Copy your scripts into the container
                           COPY scraper.py skills.py /app/

# Make sure your scripts are executable
                           RUN chmod +x /app/scraper.py /app/skills.py
