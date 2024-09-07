from setuptools import setup

APP = ["activity_improver.py"]  # Replace with your script name
DATA_FILES = []  # Add any additional data files if needed
OPTIONS = {
    "argv_emulation": True,  # Necessary for compatibility with some macOS features
    "packages": [],  # List any additional packages your app needs
    "plist": {
        "CFBundleName": "ActivityTracker",  # Application name
        "CFBundleDisplayName": "Activity Tracker",  # Display name
        "CFBundleVersion": "1.0.0",  # Version number
        "CFBundleIdentifier": "com.sukanta.activitytracker",  # Bundle identifier
        "NSHighResolutionCapable": True,  # Enable high-resolution support
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
