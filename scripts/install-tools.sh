#!/usr/bin/env bash
set -euo pipefail
# Linux cloud toolchain. No credentials, source changes or disabled TLS checks.
if [[ "$(uname -sm)" != 'Linux x86_64' ]]; then
    echo 'Este instalador requiere Linux x86_64; en Windows/macOS instala Rojo 7.6.1.' >&2
    exit 1
fi
tool_root="${MATTERLOOM_TOOLS:-/workspace/tools}"
install_tmp=$(mktemp -d)
trap 'rm -rf "$install_tmp"' EXIT
curl --fail --location --silent --show-error --retry 3 --max-time 120 \
    https://github.com/rojo-rbx/rojo/releases/download/v7.6.1/rojo-7.6.1-linux-x86_64.zip \
    -o "$install_tmp/rojo.zip"
printf '%s  %s\n' a9542a713036897fdbd0173e7a105ea409658333133c949025fcb6f1a7ca909d "$install_tmp/rojo.zip" | sha256sum -c -
curl --fail --location --silent --show-error --retry 3 --max-time 120 \
    https://github.com/luau-lang/luau/releases/download/0.744/luau-ubuntu.zip \
    -o "$install_tmp/luau.zip"
printf '%s  %s\n' 6506f0852c623aaffcb28494aac16c26dc04a269ea0e16cc0aafc8c8ac79f3ec "$install_tmp/luau.zip" | sha256sum -c -
unzip -q "$install_tmp/rojo.zip" -d "$install_tmp/rojo"
unzip -q "$install_tmp/luau.zip" -d "$install_tmp/luau"
mkdir -p "$tool_root/bin" "$tool_root/luau-0.744"
install -m 755 "$install_tmp/rojo/rojo" "$tool_root/bin/rojo"
for binary in luau luau-compile luau-analyze; do
    install -m 755 "$install_tmp/luau/$binary" "$tool_root/luau-0.744/$binary"
done
"$tool_root/bin/rojo" --version
