# Running JAMO at NERSC

This directory contains all the necessary files for setting up JAMO at NERSC. Running JAMO at NERSC
is broken down into four parts:

- Building the JAMO application as a Docker image. The relevant files for this can be found in `jamo/docker`.
- Instantiating JAMO on NERSC's Spin infrastructure. The necessary files for this can be found in `jamo/k8s` and `jamo/config`.
- Running the data transfer service on Perlmutter and the Data transfer nodes. The necessary files for this can be found in `jamo/dt_service`.


## Building the JAMO application

### Prerequisites
Before getting started, you will need to set up an account on JGI's Gitlab and set up a personal access token (PAT). 
You can create an account on JGI's Gitlab by going [here](https://code.jgi.doe.gov/) and signing in with your LBL LDAP. 
Once you are signed in, click on your avatar and go to **Preferences->Access Tokens->Add Token**. Give the token a name and set
an expiration date. Under **Select scopes**, select the box for *read_repository*.

### Getting the JAMO code
After checking out this repository, change into `jamo/docker`. From here, set `USER` and `PAT` environment variables to your 
JGI Gitlab username and PAT, respectively, and run `get_code.sh` to retrieve the all the necessary code for running JAMO.

```bash
USER=<JGI Gitlab Username> PAT=<Gitlab personal access token> bash get_code.sh
docker build ...
```

### Building the Docker image
Now that you have all the JAMO code, you can build a Docker image for running JAMO at NERSC. You will need to make your image 
available from Spin at some Docker registry. This tutorial uses [NERSC's private registry](registry.nersc.gov). See the [NERSC
documentation](https://docs.nersc.gov/development/containers/registry/) for getting access to this registry.

Once you have access, sign in to the registry: 
```bash
docker login registry.nersc.gov
```

Now build and push your image to the registry:

```bash
docker build -t registry.nersc.gov/<PID>/jamo-service:<TAG> --push .
```

You will need to set a tag (i.e. `<TAG>`). Please see the registry for current set of tags and choose a nonexistent tag. You will also 
need to fill in the NERSC project ID.

If you are building your image locally, you will probably need to use `docker buildx` to build your image for multiple platforms or, at the very 
least, build for the platform running NERSC Spin (i.e. `linux/amd64`). Below is an example of how you would build an image for running on Apple silicon
and a Linux machine.

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t registry.nersc.gov/<PID>/jamo-service:<TAG> --push .
```

## Running JAMO on Spin
To run JAMO on Spin, you will first need to attend a [SpinUp Workshop](https://www.nersc.gov/users/training/spin/). NERSC's Spin infrastructure 
uses Rancher, a management and orchestration framework for Kubernetes clusters. The `jamo/k8s` directory contains the Kubernetes configuration 
files for setting up all the components necessary for running JAMO.

Update `k8s/deployments/jamo-app.yaml` with the correct image to pull from.

## `dt_service`
Shell scripts for running data transfer service
