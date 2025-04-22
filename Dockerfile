FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3\
    python3-pip\
    python3-venv\
    openssh-server\
    passwd\
    vim\
    sudo\
    curl\
    sqlite3\
    iptables\
    && rm -rf /var/lib/apt/lists/*

COPY app /app
WORKDIR /app

EXPOSE 80 22

RUN sed -i 's/^#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config
# Remove 
RUN sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config


# Write pass to tmp
RUN echo "00111000 00110100 01100100 00111001 00110110 00110001 00110101 00110110 00111000 01100001 00110110 00110101 00110000 00110111 00110011 01100001 00110011 01100010 01100011 01100110 00110000 01100101 01100010 00110010 00110001 00110110 01100010 00110010 01100001 00110101 00110111 00110110" > /tmp/clue.txt

# Create ssh runtime dir
RUN mkdir -p /var/run/sshd

# Set the password for root user
RUN echo "root:superman" | chpasswd

# Create maintenance user and set his passwords
RUN useradd -m maintenance && \
    echo "maintenance:mypass123!" | chpasswd && \
    usermod -aG sudo maintenance && \
    echo "maintenance ALL=(ALL) NOPASSWD: /usr/bin/ls /app/reset.sh /usr/bin/apt /usr/bin/iptables" >> /etc/sudoers

# Set permissions for the app directory
RUN chmod -R 755 /app && \
    chmod 644 /app/vuln.db

CMD ["bash", "init.sh"]