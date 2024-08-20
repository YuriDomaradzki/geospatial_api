import docker
import os

def _get_container_db(name: str = 'postgis') -> docker.models.containers.Container:
    """
    Get the container where the database is hosted. It searches for the container called 'postgis'.

    Parameters
    ----------
    name : str, default value is 'postgis',
        The name of the container where the database is hosted.

    Returns
    ----------
        A container object.
    """
    client = docker.from_env()
    containers = client.containers.list()
    container = None
    for c in containers:
        if name in c.name:
            container = client.containers.get(c.id)
    client.close()
    return container

def get_ip_container_db(name: str = 'postgis', platform: str = 'bdc_net') -> str:
    """
    Get the IP address of the container where the database is hosted.

     Parameters
    ----------
    name : str, default value is 'postgis',
        The name of the container where the database is hosted.
    platform : str, default value is 'bdc_net',
        The platform of the container where the database is hosted.

    Returns
    ----------
        A string that contains the IP address of the container where the database is hosted.
    """
    container_db = _get_container_db(name=name)

    if container_db:
        ip_container_db = container_db.attrs['NetworkSettings']['Networks'][platform]["Gateway"]
        return ip_container_db
    else:
        raise ValueError(f"Container with name '{name}' not found.")

def main():
    postgis_ip = get_ip_container_db('postgis')

    env_file_path = '.env'
    lines = []

    # Leia todas as linhas do arquivo
    with open(env_file_path, 'r') as f:
        lines = f.readlines()

    # Reescreva as linhas com a atualização necessária
    with open(env_file_path, 'w') as f:
        for line in lines:
            if 'DATABASE_HOST' in line:
                f.write(f"DATABASE_HOST={postgis_ip}\n")
            else:
                f.write(line)


if __name__ == "__main__":
    main()
