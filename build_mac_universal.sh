#!/usr/bin/env bash
cd "$(dirname "$0")"

echo ""
echo "====================================================="
echo "  KevinNet - macOS Universal Binary Builder"
echo "  kevinhaji.com | kevin.fullstack.dev@gmail.com"
echo "====================================================="
echo ""

[ "$(uname -s)" != "Darwin" ] && echo "[ERROR] macOS only." && exit 1
[ "$(uname -m)" != "arm64"  ] && echo "[ERROR] Run on Apple Silicon Mac." && exit 1
command -v lipo &>/dev/null   || { echo "[ERROR] xcode-select --install"; exit 1; }

echo "[Check] Rosetta 2..."
arch -x86_64 uname -m > /dev/null 2>&1 || softwareupdate --install-rosetta --agree-to-license
echo "  OK"
echo ""

ARM_PYTHON=""
for c in "/opt/homebrew/opt/python@3.12/bin/python3.12" "/opt/homebrew/opt/python@3.11/bin/python3.11" "/opt/homebrew/bin/python3"; do
    if [ -f "$c" ]; then
        CHK=$(arch -arm64 "$c" -c "import platform; print(platform.machine())" 2>/dev/null || true)
        [ "$CHK" = "arm64" ] && ARM_PYTHON="$c" && break
    fi
done
[ -z "$ARM_PYTHON" ] && ARM_PYTHON=$(which python3)

INTEL_PYTHON=""
for c in "/usr/local/opt/python@3.12/bin/python3.12" "/usr/local/opt/python@3.11/bin/python3.11" "/usr/local/bin/python3"; do
    if [ -f "$c" ]; then
        CHK=$(arch -x86_64 "$c" -c "import platform; print(platform.machine())" 2>/dev/null || true)
        [ "$CHK" = "x86_64" ] && INTEL_PYTHON="$c" && break
    fi
done

if [ -z "$INTEL_PYTHON" ]; then
    echo "  Installing Intel Python..."
    [ ! -f "/usr/local/bin/brew" ] && arch -x86_64 /bin/bash -c \
        "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    arch -x86_64 /usr/local/bin/brew install python@3.12 python-tk@3.12
    INTEL_PYTHON="/usr/local/opt/python@3.12/bin/python3.12"
fi

echo "  ARM:   $ARM_PYTHON"
echo "  Intel: $INTEL_PYTHON"
echo ""

COMMON_ARGS=(--onefile --clean)
[ -f "MasterDnsVPN"     ] && COMMON_ARGS+=(--add-data "MasterDnsVPN:.")     && echo "  Bundling: MasterDnsVPN"
[ -f "MasterDnsVPN.exe" ] && COMMON_ARGS+=(--add-data "MasterDnsVPN.exe:.") && echo "  Bundling: MasterDnsVPN.exe"
echo ""

echo "[1/5] ARM venv + packages..."
"$ARM_PYTHON" -m venv .venv_arm64
.venv_arm64/bin/pip install dnspython pyinstaller pillow --quiet --upgrade && echo "  OK"

echo "[2/5] Intel venv + packages..."
arch -x86_64 "$INTEL_PYTHON" -m venv .venv_x86_64
arch -x86_64 .venv_x86_64/bin/pip install dnspython pyinstaller pillow --quiet --upgrade && echo "  OK"
echo ""

echo "[3/5] Building ARM64..."
.venv_arm64/bin/python -m PyInstaller "${COMMON_ARGS[@]}" --name KevinNet_arm64 kevinnet.py
[ ! -f "dist/KevinNet_arm64" ] && [ -d "dist/KevinNet_arm64.app" ] && \
    cp "dist/KevinNet_arm64.app/Contents/MacOS/KevinNet_arm64" "dist/KevinNet_arm64"
[ ! -f "dist/KevinNet_arm64" ] && echo "[ERROR] ARM build failed." && exit 1
echo "  OK: $(lipo -archs dist/KevinNet_arm64) — $(du -h dist/KevinNet_arm64 | cut -f1)"

echo "[4/5] Building x86_64..."
arch -x86_64 .venv_x86_64/bin/python -m PyInstaller "${COMMON_ARGS[@]}" --name KevinNet_x86_64 kevinnet.py
[ ! -f "dist/KevinNet_x86_64" ] && [ -d "dist/KevinNet_x86_64.app" ] && \
    cp "dist/KevinNet_x86_64.app/Contents/MacOS/KevinNet_x86_64" "dist/KevinNet_x86_64"
[ ! -f "dist/KevinNet_x86_64" ] && echo "[ERROR] Intel build failed." && exit 1
echo "  OK: $(lipo -archs dist/KevinNet_x86_64) — $(du -h dist/KevinNet_x86_64 | cut -f1)"

echo ""
echo "[5/5] Combining Universal Binary..."
lipo -create dist/KevinNet_arm64 dist/KevinNet_x86_64 -output dist/KevinNet
ARCHS=$(lipo -archs dist/KevinNet)
echo "  Architectures: $ARCHS"
if [[ "$ARCHS" != *"arm64"* ]] || [[ "$ARCHS" != *"x86_64"* ]]; then
    echo "  [WARNING] Universal combine may have failed — keeping separate binaries"
else
    rm -f dist/KevinNet_arm64 dist/KevinNet_x86_64
fi

rm -rf build .venv_arm64 .venv_x86_64
rm -rf dist/*.app
rm -f KevinNet_arm64.spec KevinNet_x86_64.spec

echo ""
echo "====================================================="
echo "  SUCCESS: dist/KevinNet"
echo "  Size: $(du -h dist/KevinNet | cut -f1)"
echo "  Runs on ALL Macs (Intel + Apple Silicon)"
echo "====================================================="
open dist/
