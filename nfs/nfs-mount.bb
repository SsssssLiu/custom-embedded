DESCRIPTION = "NFS auto-mount service (client and server)"
LICENSE = "CLOSED"

SRC_URI += "file://nfs-client.service"
SRC_URI += "file://nfs-server.service"

inherit cmake systemd pkgconfig

SYSTEMD_SERVICE:${PN} = "nfs-client.service nfs-server.service"

do_install() {
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/nfs-client.service ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/nfs-server.service ${D}${systemd_system_unitdir}
}

FILES:${PN} += "${systemd_system_unitdir}/nfs-client.service"
FILES:${PN} += "${systemd_system_unitdir}/nfs-server.service"