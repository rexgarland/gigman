# deploy

1. `./test`
2. uprev in `pyproject.toml`
3. commit and push to remote
4. `./clean` and `./build`
5. update image url in README for pypi.org
   - should be prepended with repo server url
   - e.g. `https://git.sr.ht/~rexgarland/gigman/blob/HEAD/images/demo.gif`
6. `./upload`
7. revert the image url in README
