import subprocess

def get_available_space():
    try:
        # Assuming you want to check the available space on the filesystem of the current directory
        space_output = subprocess.check_output(['df', '-BG', '--output=avail', '.'], stderr=subprocess.STDOUT).splitlines()[-1]
        return space_output.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Problem getting space: {e.output.decode()}")
        return None
    except Exception as e:
        print(f"Unexpected error getting space: {e}")
        return None

space = get_available_space()

print(space)