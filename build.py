import subprocess
import sys
import platform
import os


def build_application():
    # Define the name of the main Python script for your application
    main_script = (
        "main.py"  # Replace with the name of your main script if it's different
    )

    # Define the name of the output executable
    output_name = "Presence Maker"

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
        if not os.path.isfile(icon_file):
            print(
                f"Icon file '{icon_file}' not found. Please ensure it is in the correct directory."
            )
            sys.exit(1)
        pyinstaller_options = [
            "pyinstaller",
            "--onefile",  # Create a single executable file
            "--noconsole",  # Hide the console window (for GUI applications)
            f"--icon={icon_file}",  # Specify the icon file for the executable
            f"--name={output_name}",  # Specify the name of the output executable
            main_script,  # The main Python script to package
        ]

    # Verify that the main script exists
    if not os.path.isfile(main_script):
        print(
            f"Main script '{main_script}' not found. Please ensure it is in the correct directory."
        )
        sys.exit(1)

    try:
        # Execute PyInstaller command
        print(f"Building application with the command: {' '.join(pyinstaller_options)}")
        subprocess.run(pyinstaller_options, check=True)

        # Remove the .spec file if it exists
        spec_file = f"{output_name}.spec"
        if os.path.isfile(spec_file):
            os.remove(spec_file)
            print(f"Removed spec file '{spec_file}'")

        print("Build completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the build process: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_application()
