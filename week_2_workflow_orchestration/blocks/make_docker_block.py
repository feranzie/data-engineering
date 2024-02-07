from prefect.infrastructure.docker import DockerContainer

#alternative for creatig docker block in the ui
docker_block= DockerContainer(
    image="feranzie/prefect:zoom",
    image_pull_policy="AlWAYS",
    auto_remove=True,
)

docker_block.save('zoom', overwrite=True)
#docker_container_block = DockerContainer.load("zoom")