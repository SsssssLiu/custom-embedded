DESCRIPTION = "NFS auto-mount service (client and server)"
LICENSE = "MPL-2.0"

SRC_URI += "file://nfs-mount.service"
SRC_URI += "file://nfs-server.service"

inherit cmake systemd pkgconfig

SYSTEMD_SERVICE:${PN} = "nfs-mount.service nfs-server.service"

do_install() {
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/nfs-mount.service ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/nfs-server.service ${D}${systemd_system_unitdir}
}

FILES:${PN} += "${systemd_system_unitdir}/nfs-mount.service"
FILES:${PN} += "${systemd_system_unitdir}/nfs-server.service"