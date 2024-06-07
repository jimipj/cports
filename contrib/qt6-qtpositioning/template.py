pkgname = "qt6-qtpositioning"
pkgver = "6.7.1"
pkgrel = 0
build_style = "cmake"
make_check_args = ["-E", "(module_includes)"]
hostmakedepends = [
    "cmake",
    "ninja",
    "pkgconf",
]
makedepends = [
    "qt6-qtdeclarative-devel",
]
pkgdesc = "Qt6 Positioning component"
maintainer = "Jami Kettunen <jami.kettunen@protonmail.com>"
license = (
    "LGPL-2.1-only AND LGPL-3.0-only AND GPL-3.0-only WITH Qt-GPL-exception-1.0"
)
url = "https://www.qt.io"
source = f"https://download.qt.io/official_releases/qt/{pkgver[:-2]}/{pkgver}/submodules/qtpositioning-everywhere-src-{pkgver}.tar.xz"
sha256 = "5c2b0d46b8d35126e97c8efe22264b2de7ac1273a5ec38a0314731bb02804f53"
# cross: TODO
options = ["!cross"]


def init_check(self):
    self.make_check_env = {
        "QT_QPA_PLATFORM": "offscreen",
        "QML2_IMPORT_PATH": str(
            self.chroot_cwd / f"{self.make_dir}/lib/qt6/qml"
        ),
    }


def post_install(self):
    self.rm(self.destdir / "usr/tests", recursive=True)


@subpackage("qt6-qtpositioning-devel")
def _devel(self):
    self.depends += [
        f"qt6-qtbase-devel~{pkgver[:-2]}",
        f"qt6-qtdeclarative-devel~{pkgver[:-2]}",
    ]
    return self.default_devel(
        extra=[
            "usr/lib/qt6/metatypes",
            "usr/lib/qt6/mkspecs",
            "usr/lib/qt6/modules",
            "usr/lib/*.prl",
        ]
    )