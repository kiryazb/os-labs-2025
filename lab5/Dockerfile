FROM i386/debian:bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends nasm qemu-system-x86 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY boot.asm /src/boot.asm

RUN nasm -f bin boot.asm -o boot.bin

CMD ["qemu-system-i386", \
     "-drive", "format=raw,file=boot.bin", \
     "-display", "curses", "-serial", "none", "-monitor", "none", "-no-reboot"]
