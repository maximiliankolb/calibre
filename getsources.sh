#!/bin/sh -e

# Usage: ./getsources.sh [version]
#     (this produces calibre-[version]-nofonts.tar.xz)
if [ -n "$1" ]; then
    version="$1"
else
    version="$(awk '/^Version:/{print $2}' *.spec)"
fi

fname="calibre-${version}-nofonts.tar.xz"
if [ -e "$fname" ]; then
    echo "$fname already exists, not downloading"
    exit 0
fi

echo "Downloading version ${version}"
[ -x /bin/pxz ] && xz=pxz || xz=xz

curl -sSL http://code.calibre-ebook.com/dist/src | \
    xzcat | \
    tar --delete --wildcards -f - '*/fonts/liberation/*' | \
    $xz -9v > "$fname"

echo "$fname is ready"
