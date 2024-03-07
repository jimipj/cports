pkgname = "sbcl"
pkgver = "2.4.4"
pkgrel = 0
archs = ["aarch64", "ppc", "ppc64le", "riscv64", "x86_64"]
configure_args = [
    "--prefix=/usr",
    "--with-sb-core-compression",
    "--with-sb-dynamic-core",
    "--with-sb-linkable-runtime",
    "--with-sb-test",
    "--with-sb-unicode",
]
hostmakedepends = [
    "ecl",
    "ecl-devel",
    "gc-devel",
    "gmake",
    "gmp-devel",
    "libatomic_ops-devel",
    "libffi-devel",
    "linux-headers",
    "texinfo",
]
makedepends = ["zstd-devel"]
checkdepends = ["strace"]
pkgdesc = "Steel Bank Common Lisp"
maintainer = "Paul A. Patience <paul@apatience.com>"
license = "custom:sbcl"
url = "https://www.sbcl.org"
source = f"$(SOURCEFORGE_SITE)/{pkgname}/{pkgname}-{pkgver}-source.tar.bz2"
sha256 = "8a932627b3f1d8e9618f1cdc225edcb002456804697e2c87d140683764a106d5"
# tests are unreliable
options = ["!cross", "!lto", "!check"]
# GNUMAKE disregarded in tests
exec_wrappers = [("/usr/bin/gmake", "make")]


def init_configure(self):
    match self.profile().arch:
        # only available on a few archs
        # --fancy implies threads
        case "aarch64" | "riscv64" | "x86_64":
            self.configure_args += ["--fancy", "--with-sb-thread"]


def do_build(self):
    self.do("sh", "make.sh", "ecl", *self.configure_args)
    self.do("gmake", "info", wrksrc="doc/manual")


def do_check(self):
    self.do("sh", "run-tests.sh", wrksrc="tests")


def do_install(self):
    self.do(
        "sh",
        "install.sh",
        env={"INSTALL_ROOT": str(self.chroot_destdir / "usr")},
    )

    self.install_license("COPYING")
    self.rm(self.destdir / "usr/share/doc/sbcl/COPYING")
