## `docker`
Files for building Docker container for JAMO service

First, run `get_code.sh` to retrieve the code needed for running JAMO from JGI's repositories.

Then run `docker build` to build the Docker image

```bash
USER=<JGI Gitlab Username> PAT=<Gitlab personal access token> bash get_code.sh
docker build ...
```

## `k8s`
Config files for deploying JAMO service on Kubernetes

Update `k8s/deployments/jamo-app.yaml` with the correct image to pull from.

## `dt_service`
Shell scripts for running data transfer service
