"""List of development tasks."""
from invoke import task
from invoke.exceptions import Failure


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


@task(help={"version": "Version like vN.N.N"})
def release(ctx, version):
    """Create new release."""
    if not version.startswith("v"):
        print("Please provide version in format of vN.N.N")
        return

    print("Release new version {}".format(version))
    version_num = version[1:]
    try:
        ctx.run("$(git rev-parse --abbrev-ref HEAD) == master")
        ctx.run("git tag")
        ctx.run(
            'sed -i \'s#__version__ = ".*"#__version__ = "{}"#\' setup.py'.format(
                version,
            ),
        )
        ctx.run("git add setup.py")
        ctx.run("git commit -m 'Release version {}'".format(version_num))
        ctx.run("git tag -a -m 'Release version {}' {}".format(version_num, version))
        ctx.run("git push --follow-tags")
        ctx.run("rm CHANGELOG.md")
        ctx.run("gren changelog --generate --tags=all && remark CHANGELOG.md -o")
        ctx.run("git add CHANGELOG.md")
        ctx.run(
            "git commit -m 'Update changelog for release version {}'".format(
                version_num,
            ),
        )
        ctx.run("git push")
        ctx.run("gren release --tags={}".format(version))
    except Failure as e:
        print(e)


@task
def test(cmd):
    """Run unit tests."""
    cmd.run("py.test")


@task
def test_venv(cmd):
    """Run unit tests in dedicated environment."""
    cmd.run("tox")
