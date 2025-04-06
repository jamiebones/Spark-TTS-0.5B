# Getting Started with Create Lilypad Module

This project was bootstrapped with [Create Lilypad Module](https://github.com/DevlinRocha/create-lilypad-module).

## Prerequisites

To build and run a module on Lilypad Network, you'll need to have the [Lilypad CLI](https://docs.lilypad.tech/lilypad/lilypad-testnet/install-run-requirements), [Python](https://www.python.org/), and [Docker](https://www.docker.com/) on your machine, as well as [GitHub](https://github.com/) and [Docker Hub](https://hub.docker.com/) accounts.

## Configuration

Additional configuration is required to run the Lilypad module.

### [`.env`](.env)

```
WEB3_PRIVATE_KEY = ""
```

#### `WEB3_PRIVATE_KEY`

> 🚨 **DO NOT SHARE THIS KEY** 🚨

The private key for the wallet that will be used to run the job.

A new development wallet is highly recommended to use for development.

The wallet must have enough LP tokens and Arbitrum Sepolia ETH to fund the job.

- [Funding your wallet](https://docs.lilypad.tech/lilypad/lilypad-testnet/quick-start/funding-your-wallet-from-faucet)

### [`config/constants.py`](./config/constants.py)

```python
DOCKER_REPO = ""
DOCKER_TAG = "latest"
GITHUB_REPO = ""
GITHUB_TAG = "main"
```

#### `DOCKER_REPO`

The Docker Hub repository storing the container image of the module code.

This is required to push the image to Docker Hub and run the module on Lilypad Network.

e.g. `"<dockerhub_username>/<dockerhub_image>"`

###### <dockerhub_username>/<dockerhub_image>

#### `DOCKER_TAG`

The specific tag of the `DOCKER_REPO` containing the module code.

Default: `"latest"`

#### `GITHUB_REPO`

The URL for the GitHub repository storing the `lilypad_module.json.tmpl` file. The visibility of the repository must be public.

The `lilypad_module.json.tmpl` file points to a `DOCKER_REPO` and Lilypad runs the module from the image.

e.g. `"github.com/<github_username>/<github_repo>"`

#### `GITHUB_TAG`

The GitHub tag, branch, or commit hash that contains the `lilypad_module.json.tmpl` file you want to run.

To ensure the most current version of your module is utilized during development and testing, it's advisable to specify a commit hash. Otherwise, the resource provider computing the job might use an outdated cached version of your module. Specifying the commit hash guarantees the latest version of your module is downloaded and used.

Use `git log` to find and set this easily.

Default: `"main"`

## Available Scripts

Your module will be bootstrapped with some handy scripts to help you download the model(s) for your module, build and push Docker images, and run your module locally or on Lilypad Network. Some additional configuration may be required.

In the project directory, you can run:

### [`python -m scripts.download_models`](./scripts/download_models.py)

A basic outline for downloading a model from [Hugging Face](https://huggingface.co/) is provided, but the structure of the script and the methods for downloading a model can differ between models and libraries. It’s important to tailor the process to the specific requirements of the model you're working with.

Most (but not all) models that utilize machine learning use the [🤗 Transformers](https://huggingface.co/docs/transformers/index) library, which provides APIs and tools to easily download and train pretrained models.

- [Learn more about downloading models from Hugging Face](https://huggingface.co/docs/hub/en/models-downloading)
- [Learn more about the 🤗 Transformers library](https://huggingface.co/docs/hub/en/transformers)

No matter which model you are using, be sure to thoroughly read the documentation to learn how to properly download and use the model locally.

### [`python -m scripts.docker_build`](./scripts/docker_build.py)

Builds and optionally publishes a Docker image for the module to use.

For most use cases, this script should be sufficient and won't require any configuration or modification (aside from setting your `DOCKER_REPO` and `DOCKER_TAG`).

In the modules `Dockerfile`, you'll find 3 COPY instructions.

```Dockerfile
COPY requirements.txt .
COPY src /src
COPY models /models
```

These instructions copy the `requirements.txt` file, the `src` directory, and the `models` directory from your local machine into the Docker image. It's important to remember that any modifications to these files or directories will necessitate a rebuild of the module's Docker image to ensure the changes are reflected in the container.

#### `--local` Flag

Running the script with `--local` passed in builds the Docker image and loads it into the local Docker daemon instead of pushing to Docker Hub.

#### `--no-cache` Flag

Running the script with `--no-cache` passed in builds the Docker image without using the cache. This flag is useful if you need a fresh build to debug caching issues, force system or dependency updates, pull the latest base image, or ensure clean builds in CI/CD pipelines.

### [`python -m scripts.run_module`](./scripts/run_module.py)

This script is provided for convenience to speed up development. It is equivalent to running the Lilypad module with the provided input and private key (unless running the module locally, then no private key is required). Depending on how your module works, you may need to change the default behavior of this script.

### Running the module locally on Docker

```bash
docker run -it --rm \
  -e INPUT="Your text to convert to speech goes here" \
  -v $(pwd)/outputs:/outputs \
  texttospeech:v1
```
This will run a container from the `texttospeech:v1` image. This text is converted to speech using the default audio saved /app/audio/voice.wav in the container.

To clone a voice, you can use the following command:

```bash
docker run -it --rm   -e INPUT="This is a text to speech module"   \
-e PROMPT_TEXT="This prompt text is the transcript of the voice you want to clone"  \
-e PROMPT_SPEECH_PATH="/app/audio/voice.wav"  \
 -v $(pwd)/outputs:/outputs \
-v $(pwd)/audio:/app/audio \   
  texttospeech:latest

```
You mount the audio directory and ensure it contains the voice.wav file. Running the container will use the voice.wav file as the voice for the text to speech module.


### Running the module on Lilypad Network

Basic usage:

```bash
  lilypad run github.com/jamiebones/Spark-TTS-0.5B.git:v1.6  --web3-private-key <private-key> -i input="This is a test of the text to speech system."
```

This will run the module on Lilypad's Network using the default audio file in the /app/audio/voice.wav directory.



## Learn More

Learn how to [build a Lilypad job module](https://docs.lilypad.tech/lilypad/developer-resources/build-a-job-module).

Reference the [Lilypad Module Builder Guide](https://blog.lilypadnetwork.org/lilypad-module-builder-guide).

To learn more about Lilypad, check out the [Lilypad documentation](https://docs.lilypad.tech/lilypad).
