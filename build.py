import subprocess
import sys


def build_application():
    # Define the name of the main Python script for your application
    main_script = (
        "main.py"  # Replace with the name of your main script if it's different
    )

    # Define the name of the output executable
    output_name = "activity_improver"

    # Define additional options for PyInstaller
    pyinstaller_options = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--noconsole",  # Hide the console window (for GUI applications)
        "--icon=handshake.ico",  # Specify the icon file for the executable
        f"--name={output_name}",  # Specify the name of the output executable
        main_script,  # The main Python script to package
    ]

    # Execute PyInstaller command
    subprocess.run(pyinstaller_options, check=True)


if __name__ == "__main__":
    build_application()
