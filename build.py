import subprocess
import sys
import platform


def build_application():
    # Define the name of the main Python script for your application
    main_script = (
        "main.py"  # Replace with the name of your main script if it's different
    )

    # Define the name of the output executable
    output_name = "activity_improver"

    # Determine the appropriate icon file based on the operating system
    os_system = platform.system()
    if os_system == "Darwin":  # macOS
        icon_file = "handshake.icns"
        pyinstaller_options = [
            "pyinstaller",
            "--onefile",  # Create a single executable file
            "--windowed",  # Hide the console window (for GUI applications)
            f"--name={output_name}",  # Specify the name of the output executable
            main_script,  # The main Python script to package
        ]
    else:  # Windows and Linux
        icon_file = "handshake.ico"
        pyinstaller_options = [
            "pyinstaller",
            "--onefile",  # Create a single executable file
            "--noconsole",  # Hide the console window (for GUI applications)
            f"--icon={icon_file}",  # Specify the icon file for the executable
            f"--name={output_name}",  # Specify the name of the output executable
            main_script,  # The main Python script to package
        ]

    # Execute PyInstaller command
    subprocess.run(pyinstaller_options, check=True)


if __name__ == "__main__":
    build_application()
