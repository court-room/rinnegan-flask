# rinnegan-flask

[![test Actions Status](https://github.com/court-room/rinnegan-flask/workflows/test/badge.svg)](https://github.com/court-room/rinnegan-flask/actions)
[![docker Actions Status](https://github.com/court-room/rinnegan-flask/workflows/docker/badge.svg)](https://github.com/court-room/rinnegan-flask/actions)
[![codecov](https://codecov.io/gh/court-room/rinnegan-flask/branch/master/graph/badge.svg)](https://codecov.io/gh/court-room/rinnegan-flask)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/court-room/rinnegan-flask/?ref=repository-badge)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=court-room/rinnegan-flask)](https://dependabot.com)

## Development

The server can be used for locally testing the client or the entire set of services.
In order to use the server you need to follow certain steps

- Build the image locally

  ```bash
  $ docker build  --compress --force-rm --tag rinnegan-flask:latest .
  ```

- Tag the latest image to local registry format

  ```bash
  $ docker image tag rinnegan-flask:latest localhost:6000/rinnegan-flask:latest
  ```

- Push the image to the registry

  ```bash
  $ docker push localhost:6000/rinnegan-flask:latest
  ```

_OPTIONAL_

There is a shell script at `bin/build.sh` that handles the image build,
tagging and pushing it to the local registry.

## Contact

For any issue please contact the following persons

- [onlinejudge95](https://github.com/onlinejudge95)
