FROM gcc:13-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge
COPY challenge/password-please.c .
RUN gcc -O0 -fno-stack-protector -no-pie -o chall password-please.c

EXPOSE 5000
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:/challenge/chall,stderr"]
