import os
import docker
from docker.client import DockerClient
from docker.errors import DockerException, ContainerError, ImageNotFound
from docker.models.networks import Network

script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"dir: {script_dir}")
api_root_path = os.path.dirname(script_dir)


def get_network(network_name) -> Network:
    client = get_docker_client()
    return client.networks.get(network_name)


def get_docker_client() -> DockerClient:
    try:
        client = docker.from_env()
        return client
    except DockerException:
        print("Error: Could not connect to the Docker daemon.")
        print("Please make sure Docker is running.")
        exit()


def create_device(endpoint: str, device_id: str, user_id: str, interval: int = 60):
    client = get_docker_client()
    docker_file_path = f"{api_root_path}/Sim.Dockerfile"
    image_tag = "device_" + device_id

    network = get_network("api_default")
    custom_env = {
        "DEVICE_ID": device_id,
        "USER_ID": user_id,
        "API_URL": f"http://{network.name}:8000{endpoint}",
        "INTERVAL": interval,
    }

    print(f"docker file path: {docker_file_path}")

    try:
        image, _ = client.images.build(
            path=script_dir,
            tag=image_tag,
            dockerfile="Sim.Dockerfile",
            rm=True,
            nocache=True,
        )
        print(f"Created image for {device_id}. image: {image.short_id}")

        print(f"\nRunning container from image '{image_tag}'...")

        print("sette network as {network}")
        client.containers.run(
            image_tag,
            environment=custom_env,
            remove=True,
            detach=True,
            network=network.name,
        )

        print("\n✅ Container ran and exited successfully.")

    except ContainerError as e:
        print(f"❌ Error running container: {e}")
    except ImageNotFound:
        print(f"❌ Error: Image '{image_tag}' not found. The build may have failed.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    return
