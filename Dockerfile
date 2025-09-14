FROM trycua/cua-ubuntu:latest

USER root
RUN apt-get update && \
    apt-get install -y xrdp pulseaudio dbus-x11 && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 3389
CMD ["/usr/sbin/xrdp-sesman", "-n"]