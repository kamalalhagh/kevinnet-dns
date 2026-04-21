#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo ""
echo "====================================================="
echo "  KevinNet DNS Config - Linux Build"
echo "  kevinhaji.com | kevin.fullstack.dev@gmail.com"
echo "====================================================="
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "  Platform: $OS / $ARCH"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "[ERROR] python3 not found."
    echo "  sudo apt install python3 python3-pip python3-venv python3-tk"
    exit 1
fi

if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "[ERROR] tkinter not found."
    echo "  sudo apt install python3-tk"
    exit 1
fi

echo "[1/3] Installing packages..."
python3 -m pip install dnspython pyinstaller pillow --quiet --upgrade
echo "  OK"

ADD_DATA=""
[ -f "MasterDnsVPN"     ] && ADD_DATA="$ADD_DATA --add-data MasterDnsVPN:."     && echo "  Bundling: MasterDnsVPN"
[ -f "MasterDnsVPN.exe" ] && ADD_DATA="$ADD_DATA --add-data MasterDnsVPN.exe:." && echo "  Bundling: MasterDnsVPN.exe"
echo ""

echo "[2/3] Building binary..."
python3 -m PyInstaller \
    --onefile --windowed \
    --name "KevinNet" \
    --clean \
    $ADD_DATA \
    "kevinnet.py"

echo ""
echo "[3/3] Cleanup..."
rm -rf build KevinNet.spec

echo ""
echo "====================================================="
echo "  SUCCESS: dist/KevinNet"
echo "  Platform: $OS / $ARCH"
echo "====================================================="
