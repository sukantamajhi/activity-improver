import subprocess
import sys
import os


def build():
    # Define the name of your script and executable
    script_name = "activity_improver.py"
    output_name = "ActivityImproverApp"

    # PyInstaller command
    command = [
        "pyinstaller",
        "--onefile",  # Bundle everything into a single file
        "--windowed",  # No console window (use for GUI apps)
        "--name",
        output_name,  # Name of the executable
        script_name,  # Main Python script
    ]

    # Run the PyInstaller command
    subprocess.run(command, check=True)


if __name__ == "__main__":
    build()
