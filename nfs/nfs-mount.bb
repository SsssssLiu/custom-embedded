DESCRIPTION = "NFS auto-mount service (client and server)"
LICENSE = "CLOSED"

SRC_URI += "file://nfs-mount-client.service"
SRC_URI += "file://nfs-mount-server.service"

inherit systemd pkgconfig

SYSTEMD_SERVICE:${PN} = "nfs-mount-client.service nfs-mount-server.service"

do_install() {
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/nfs-mount-client.service ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/nfs-mount-server.service ${D}${systemd_system_unitdir}
}

FILES:${PN} += "${systemd_system_unitdir}/nfs-mount-client.service"
FILES:${PN} += "${systemd_system_unitdir}/nfs-mount-server.service"