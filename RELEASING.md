# Releasing `braggedgemodeling`

Releases are **fully automated from a git tag**. The package version is derived
from the latest `vX.Y.Z` tag by [versioningit] — there is no version string to
hand-edit. Pushing a `vX.Y.Z` tag to `main` triggers
[`.github/workflows/publish.yml`](.github/workflows/publish.yml), which:

- publishes the **wheel + sdist to PyPI** via GitHub OIDC *trusted publishing*
  (no API tokens),
- builds the **noarch conda package** and uploads it to **anaconda.org** on the
  `neutronimaging` channel, and
- creates a **GitHub Release** for the tag with auto-generated notes and the
  build artifacts attached.

Nothing is published until a tag is pushed — pushes and PRs only build/test.

[versioningit]: https://versioningit.readthedocs.io/

## Prerequisites (one-time, already in place)

- **PyPI trusted publisher** registered for project `braggedgemodeling`
  (owner `ornlneutronimaging`, repo `braggedgemodeling`, workflow `publish.yml`,
  environment `pypi`).
- **`ANACONDA_TOKEN`** organization secret (used for the anaconda.org upload).

## Versioning

- versioningit computes the version from the most recent `vX.Y.Z` tag;
  `[tool.versioningit.next-version] method = "minor"`.
- Tag format is **`vMAJOR.MINOR.PATCH`** (e.g. `v0.2.0`).
- Pre-releases use a suffix: **`v0.2.0rc1`**, `v0.2.0a1`, `v0.2.0b1`. A tag whose
  name contains `rc` is uploaded to anaconda under the **`rc`** label (otherwise
  `main`), and `rc`/`alpha`/`beta` tags are marked as a **prerelease** on GitHub.
- There is no `CHANGELOG` to edit — the GitHub Release notes are auto-generated
  from merged PRs.

## Cutting a release

1. **Fetch and update** your local `main`:
   ```bash
   git switch main
   git fetch origin
   git pull --ff-only
   ```
2. **Confirm `main` is green and clean.** The latest CI run on `main` should be
   passing (unit tests on py3.12/3.13, `linux` build, `pre-commit`). Optionally
   rehearse the build locally:
   ```bash
   pixi run -e package build-conda   # -> local-channel/**/braggedgemodeling-*.conda
   pixi run -e package build         # -> dist/*.whl, dist/*.tar.gz
   ```
3. **Choose the version** (e.g. `v0.2.0`; use `v0.2.0rc1` for a rehearsal —
   see below).
4. **Tag and push** — an annotated tag on `main`:
   ```bash
   git tag -a v0.2.0 -m "Release 0.2.0"
   git push origin v0.2.0
   ```
5. **Watch the release workflow**:
   ```bash
   gh run watch --repo ornlneutronimaging/braggedgemodeling
   ```
   The tag triggers `publish.yml` → `linux` (build) → `pypi-publish` +
   `github-release`, plus the anaconda upload.

## Verify the release

- **PyPI** — https://pypi.org/project/braggedgemodeling/ , then in a clean env:
  ```bash
  pip install "braggedgemodeling==0.2.0"
  python -c "import braggedgemodeling as bem; print(bem.__version__)"   # -> 0.2.0
  ```
- **conda / anaconda.org**:
  ```bash
  conda install -c conda-forge -c neutronimaging "braggedgemodeling=0.2.0"
  ```
- **GitHub Release** — appears at `releases/tag/v0.2.0` with the wheel, sdist,
  and `.conda` attached.
- **Read the Docs** — https://braggedge.readthedocs.io/ builds the new tag.

## First modernized release / rehearsing

The first release on the new pipeline exercises PyPI trusted publishing for the
very first time. To de-risk it, cut a pre-release tag first:

```bash
git tag -a v0.2.0rc1 -m "Release candidate 0.2.0rc1"
git push origin v0.2.0rc1
```

This runs the entire pipeline (PyPI + anaconda `rc` label + a GitHub
*prerelease*) without claiming the final version, so any misconfiguration
surfaces before `v0.2.0`.

## If a release fails

- **PyPI and anaconda.org do not allow re-uploading the same version.** If a
  publish step fails after a version was already uploaded, do **not** try to
  reuse the version — fix the problem and cut the next patch (e.g. `v0.2.1`).
- Deleting a pushed tag is discouraged (others may have fetched it); prefer
  moving forward with a new tag.
- Re-running the failed workflow job is safe as long as no artifact for that
  version was uploaded yet.
