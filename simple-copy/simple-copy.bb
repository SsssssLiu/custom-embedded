DESCRIPTION = "Simply copy samplefile to image"
LICENSE = "CLOSED"

SRC_URI = "file://samplefile"

# don't need compile/configure
do_configure[noexec] = "1"
do_compile[noexec] = "1"

do_install() {
    # dest: /home/root/
    cp -r --no-preserve=ownership ${WORKDIR}/samplefile ${D}/home/root/
    chmod 777  ${D}/home/root/samplefile
}

FILES:${PN} = "/home/root/samplefile"
INSANE_SKIP:${PN} += "installed-vs-shipped dev-so file-rdeps"
