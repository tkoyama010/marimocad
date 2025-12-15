# Release and Publishing Guide

This document describes the release and publishing process for marimocad maintainers.

## Prerequisites

Before the first release, maintainers need to:

1. **Set up PyPI Trusted Publishing:**
   - Log in to [PyPI](https://pypi.org)
   - Go to account settings → Publishing
   - Add a new publisher with these details:
     - PyPI Project Name: `marimocad`
     - Owner: `tkoyama010`
     - Repository name: `marimocad`
     - Workflow name: `publish.yml`
     - Environment name: `pypi`

2. **Configure GitHub Environment (optional but recommended):**
   - Go to repository Settings → Environments
   - Create a new environment named `pypi`
   - Add protection rules (e.g., require review before deployment)

3. **Test with TestPyPI first:**
   - Register on [TestPyPI](https://test.pypi.org)
   - Set up trusted publishing for TestPyPI (similar to PyPI)
   - Run the publish workflow with "testpypi" target

## Release Workflow

### Step 1: Create a Release

Use the GitHub Actions Release workflow:

```bash
# Via GitHub UI:
# 1. Go to Actions → Release
# 2. Click "Run workflow"
# 3. Enter version (e.g., 0.1.0)
```

This will:
- Update version in `src/marimocad/__init__.py`
- Create a git tag `vX.Y.Z`
- Generate release notes from commits
- Create a GitHub Release

### Step 2: Automatic PyPI Publishing

The GitHub Release triggers the Publish workflow automatically:
- Builds the package (wheel and sdist)
- Validates with `twine check`
- Publishes to PyPI via trusted publishing
- Uploads artifacts to GitHub Release

### Manual Publishing (if needed)

If automatic publishing fails, you can trigger manually:

```bash
# Via GitHub UI:
# 1. Go to Actions → Publish to PyPI
# 2. Click "Run workflow"
# 3. Select target: "pypi" or "testpypi"
```

## Testing Before Release

### Local Testing

1. **Build the package:**
   ```bash
   python -m build
   ```

2. **Check the package:**
   ```bash
   twine check dist/*
   ```

3. **Test installation:**
   ```bash
   pip install dist/marimocad-*.whl
   python -c "import marimocad; print(marimocad.__version__)"
   ```

### TestPyPI Testing

1. **Publish to TestPyPI:**
   - Run the Publish workflow with "testpypi" target
   
2. **Install and test:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ \
               --extra-index-url https://pypi.org/simple/ \
               marimocad
   ```

## CI/CD Workflows

### Test Workflow (`test.yml`)
- Runs on every push and PR
- Tests on multiple OS (Linux, macOS, Windows)
- Tests on multiple Python versions (3.9-3.12)
- Uploads coverage to Codecov

### Lint Workflow (`lint.yml`)
- Runs ruff check and format
- Runs mypy type checking
- Ensures code quality standards

### Build Workflow (`build.yml`)
- Verifies package builds correctly
- Validates with twine
- Tests installation
- Uploads build artifacts

### Security Workflow (`security.yml`)
- Runs CodeQL analysis
- Scheduled weekly scans
- Checks for security vulnerabilities

### Publish Workflow (`publish.yml`)
- Triggered by GitHub Release or manual dispatch
- Builds and publishes to PyPI/TestPyPI
- Uses trusted publishing (no tokens needed)
- Uploads artifacts to GitHub Release

### Release Workflow (`release.yml`)
- Manual trigger only
- Updates version
- Creates git tags
- Generates release notes
- Creates GitHub Release

## Version Management

The package version is stored in:
- `src/marimocad/__init__.py` as `__version__`
- Hatch automatically reads from this file

Update version for release:
1. Use the Release workflow (recommended)
2. Or manually edit `__init__.py` and create tag

## Troubleshooting

### PyPI Publishing Fails

1. **Check trusted publishing setup:**
   - Verify PyPI publisher configuration
   - Ensure workflow name matches exactly
   - Check environment name if using

2. **Check package quality:**
   ```bash
   twine check dist/*
   ```

3. **Test with TestPyPI first:**
   - Use the manual publish workflow
   - Select "testpypi" target

### Build Fails

1. **Check pyproject.toml configuration:**
   - Verify dependencies are correct
   - Check build-backend settings

2. **Test locally:**
   ```bash
   python -m build
   pip install dist/*.whl
   ```

### Version Conflicts

If a version is already published:
1. You cannot republish the same version to PyPI
2. Increment the version number
3. Create a new release

## Security Notes

- **Never commit API tokens** - We use trusted publishing
- **Protected branches** - Releases should come from `main`
- **Environment protection** - Consider requiring reviews for releases
- **Security scanning** - CodeQL runs automatically

## Support

For issues with releases:
1. Check GitHub Actions logs
2. Review PyPI project settings
3. Open an issue on GitHub
