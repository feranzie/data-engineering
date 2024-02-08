from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
#import parameterized_flow
#from week_2_workflow_orchestration import parameterized_flow
from parameterized_flow import etl_parent_flow

docker_block = DockerContainer.load("zoom")



docker_dep=Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="docker-flow",
    infrastructure=docker_block
)

if __name__=="__main__":
    docker_dep.apply()
