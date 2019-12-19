"""List of development tasks."""
from invoke import task


@task
def build(cmd):
    """Create dist files."""
    cmd.run("rm -rf dist")
    cmd.run("python setup.py sdist bdist_wheel")


@task
def doc(cmd):
    """Generate API documentation in docs/Reference/."""
    cmd.run("pydocmd build")
    cmd.run(
        "find docs/Reference/ -name '*.md' | xargs -n1 sed '$!N; /^\\(.*\\)\\n\\1$/!P; D' '-i' ",
    )


@task
def test(cmd):
    """Run unit tests."""
    cmd.run("py.test")


@task
def test_venv(cmd):
    """Run unit tests in dedicated environment."""
    cmd.run("tox")
