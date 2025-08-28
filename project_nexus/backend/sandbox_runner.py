import docker
import os
import sys

# --- Constants ---
IMAGE_NAME = "project-nexus-sandbox"
# The path to the Dockerfile is relative to the project root, assuming this script is run from the root.
DOCKERFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def build_docker_image(client):
    """Builds the Docker image for the sandbox if it doesn't exist."""
    print(f"Building Docker image '{IMAGE_NAME}' from path: {DOCKERFILE_DIR}")
    try:
        client.images.build(path=DOCKERFILE_DIR, tag=IMAGE_NAME, rm=True)
        print("Image built successfully.")
    except docker.errors.BuildError as e:
        print(f"Error building Docker image: {e}")
        for line in e.build_log:
            if 'stream' in line:
                print(line['stream'].strip())
        raise

def run_script_in_sandbox(script_path):
    """
    Runs a given Python script inside a secure Docker container.
    """
    if not os.path.exists(script_path):
        print(f"Error: Script file not found at '{script_path}'")
        return

    client = docker.from_env()

    # Ensure the sandbox image is built
    try:
        client.images.get(IMAGE_NAME)
        print(f"Docker image '{IMAGE_NAME}' found.")
    except docker.errors.ImageNotFound:
        print(f"Docker image '{IMAGE_NAME}' not found. Building it now...")
        build_docker_image(client)

    # Get the absolute path of the script to mount it correctly
    abs_script_path = os.path.abspath(script_path)
    script_dir = os.path.dirname(abs_script_path)
    script_filename = os.path.basename(abs_script_path)

    print(f"\n--- Running script '{script_filename}' in sandbox ---")

    try:
        container = client.containers.run(
            IMAGE_NAME,
            command=["python", f"/app/{script_filename}"],
            volumes={script_dir: {'bind': '/app', 'mode': 'ro'}}, # Mount script read-only
            detach=True,
            auto_remove=True
        )

        # Wait for the container to finish and get the exit code
        result = container.wait()
        exit_code = result['StatusCode']

        # Get logs
        stdout = container.logs(stdout=True, stderr=False).decode('utf-8').strip()
        stderr = container.logs(stdout=False, stderr=True).decode('utf-8').strip()

        print("--- Sandbox Output ---")
        if stdout:
            print(f"STDOUT:\n{stdout}")
        if stderr:
            print(f"STDERR:\n{stderr}")
        print("----------------------")
        print(f"Script finished with exit code: {exit_code}")

    except docker.errors.ContainerError as e:
        print(f"Error running container: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python backend/sandbox_runner.py <path_to_script>")
        sys.exit(1)

    script_to_run = sys.argv[1]
    run_script_in_sandbox(script_to_run)
