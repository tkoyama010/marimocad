# Post-Merge Setup Checklist

After merging this PR, the repository maintainer needs to complete the following steps to enable PyPI publishing:

## 1. PyPI Account Setup

### Create PyPI Account (if not already done)
- [ ] Sign up at https://pypi.org
- [ ] Verify email address
- [ ] Enable 2FA (required for trusted publishing)

### Create TestPyPI Account (recommended for testing)
- [ ] Sign up at https://test.pypi.org
- [ ] Verify email address

## 2. Configure PyPI Trusted Publishing

### For PyPI (Production)

1. [ ] Log in to https://pypi.org
2. [ ] Go to Account Settings → Publishing
3. [ ] Click "Add a new publisher"
4. [ ] Fill in the form:
   - **PyPI Project Name**: `marimocad`
   - **Owner**: `tkoyama010`
   - **Repository name**: `marimocad`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi` (leave blank if not using environments)

### For TestPyPI (Optional but Recommended)

1. [ ] Log in to https://test.pypi.org
2. [ ] Go to Account Settings → Publishing
3. [ ] Click "Add a new publisher"
4. [ ] Fill in the form with same details as above

## 3. GitHub Repository Settings (Optional but Recommended)

### Create Protected Environment for PyPI

1. [ ] Go to repository Settings → Environments
2. [ ] Click "New environment"
3. [ ] Name it `pypi`
4. [ ] Add protection rules:
   - [ ] Required reviewers: Add yourself or team members
   - [ ] Deployment branches: Selected branches → `main`

This adds an extra safety layer requiring manual approval before publishing to PyPI.

## 4. Test the Workflows

### Test 1: Verify CI Workflows

All these should run automatically on the next push:
- [ ] Test workflow passes on all OS and Python versions
- [ ] Lint workflow passes
- [ ] Build workflow passes
- [ ] Security workflow passes (may take longer on first run)

### Test 2: Test Package Build (Local)

```bash
# Build the package
python -m build

# Check with twine
twine check dist/*

# Test installation
pip install dist/*.whl
python -c "import marimocad; print(marimocad.__version__)"
```

### Test 3: Test PyPI Publishing to TestPyPI

1. [ ] Go to Actions → "Publish to PyPI"
2. [ ] Click "Run workflow"
3. [ ] Select `main` branch
4. [ ] Select target: `testpypi`
5. [ ] Click "Run workflow"
6. [ ] Wait for workflow to complete
7. [ ] Verify package appears at https://test.pypi.org/project/marimocad/
8. [ ] Test installation from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ \
               --extra-index-url https://pypi.org/simple/ \
               marimocad
   ```

## 5. Create First Release

### Option A: Manual Release (Recommended for First Release)

1. [ ] Update version in `src/marimocad/__init__.py` from `0.1.dev0` to `0.1.0`
2. [ ] Commit and push to main
3. [ ] Create a git tag:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```
4. [ ] Go to GitHub → Releases → "Draft a new release"
5. [ ] Select the `v0.1.0` tag
6. [ ] Write release notes
7. [ ] Click "Publish release"
8. [ ] The publish workflow will automatically trigger and publish to PyPI

### Option B: Automated Release (Once Confident)

1. [ ] Go to Actions → "Release"
2. [ ] Click "Run workflow"
3. [ ] Enter version: `0.1.0`
4. [ ] Click "Run workflow"
5. [ ] Wait for completion
6. [ ] Check that GitHub Release was created
7. [ ] Verify publish workflow triggered automatically

## 6. Verify Publication

After publishing:

1. [ ] Check package appears on PyPI: https://pypi.org/project/marimocad/
2. [ ] Test installation:
   ```bash
   pip install marimocad
   python -c "import marimocad; print(marimocad.__version__)"
   ```
3. [ ] Check README displays correctly on PyPI
4. [ ] Verify all metadata (classifiers, description, etc.)

## 7. Post-Publication

1. [ ] Update GitHub repository description and topics
2. [ ] Add PyPI badge to README (already added)
3. [ ] Announce the release (GitHub Discussions, Twitter, etc.)
4. [ ] Monitor for any installation issues

## Troubleshooting

### If PyPI publishing fails:

1. **Check trusted publishing configuration**
   - Verify all fields match exactly
   - Check workflow name is `publish.yml`
   - Ensure repository and owner are correct

2. **Check workflow logs**
   - Go to Actions → Failed workflow
   - Review error messages
   - Common issues: version conflicts, missing metadata

3. **Verify package quality**
   ```bash
   twine check dist/*
   ```

4. **Test locally first**
   - Build package
   - Test installation
   - Check all metadata

### If workflows don't trigger:

1. **Check branch protection**
   - Workflows may need permissions
   - Review Actions permissions in repo settings

2. **Check workflow triggers**
   - Some workflows run on specific events only
   - Manual workflows need to be triggered via UI

## Documentation

- See [RELEASE_GUIDE.md](RELEASE_GUIDE.md) for detailed release process
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- See workflow files in `.github/workflows/` for CI/CD configuration

## Support

If you encounter issues:
1. Check GitHub Actions logs
2. Review PyPI project settings
3. Open an issue on GitHub with details
