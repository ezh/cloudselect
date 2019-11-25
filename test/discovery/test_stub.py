from cloudselect import Container
from cloudselect.cloudselect import CloudSelect


def test_stub_discovery():
    cloud = CloudSelect()
    # Read shared part
    profile = cloud.read_configuration()
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.discovery().__class__.__name__ == "Stub"
    assert Container.discovery().run() == []
