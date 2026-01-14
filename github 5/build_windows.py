
# build_windows.py
import PyInstaller.__main__
import os

# Define the app name and main entry point
APP_NAME = "GlobleXGPT"
ENTRY_POINT = "app.py"  # Replace with your main script name
ICON_PATH = "static/img/logo.jpg" # Or a .ico file if you have one

print(f"🚀 Starting Professional Build for {APP_NAME}...")

# 1. Ensure you have the version info file
# 2. Add professional flags:
# --onefile: Packages everything into a single EXE
# --windowed: Prevents a command prompt window from popping up
# --version-file: Adds the company/metadata (CRITICAL FOR TRUST)
# --icon: Adds your branding (CRITICAL FOR IMAGE)
# --uac-admin: Requests admin rights (helps with some system filters)
# --clean: Cleans cache before building

build_args = [
    ENTRY_POINT,
    '--name', APP_NAME,
    '--onefile',
    '--windowed',
    '--clean',
    '--version-file=file_version_info.txt',
    # '--icon=' + ICON_PATH, # Uncomment if ICON_PATH exists and is .ico
    '--add-data=templates;templates',
    '--add-data=static;static',
    '--noconfirm',
]

try:
    PyInstaller.__main__.run(build_args)
    print("\n✅ Build Completed Successfully!")
    print(f"📦 Your App is in the 'dist' folder as {APP_NAME}.exe")
    print("\n💡 NEXT STEP: To completely remove the 'Not Commonly Downloaded' warning:")
    print("1. Submit your compiled EXE to the Microsoft Security Intelligence site for 'Analyst Review'.")
    print("2. URL: https://www.microsoft.com/en-us/wdsi/filesubmission")
    print("3. This manually clears the 'Unknown' status in their database.")
except Exception as e:
    print(f"❌ Build Failed: {e}")
