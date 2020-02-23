# Copyright 2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""This module is used for testing Kubernetes discovery plugin."""
import os

from cloudselect import Container
from cloudselect.cloudselect import CloudSelect
from cloudselect.discovery.kubernetes import Kubernetes

import yaml


def test_kubernetes_discovery(cfgdir, mocker):
    """
    Testing Kubernetes initializaion.

    Is fabric creating Stub by default?
    Does Kubernetes return []?
    """
    k8s = os.path.join(os.path.dirname(__file__), "..", "fixture", "k8s.cloud.yaml",)
    k8s_data = os.path.join(
        os.path.dirname(__file__), "..", "fixture", "k8s_discovery_data.yaml",
    )
    k8s_pods = []
    with open(k8s_data, "r") as data:
        k8s_pods = yaml.safe_load(data)
    cloud = CloudSelect(cfgdir)
    profile = cloud.configuration_read()
    profile = cloud.merge(profile, cloud.configuration_read(k8s))
    args = cloud.parse_args([])
    cloud.fabric(profile, args)
    assert Container.discovery().__class__.__name__ == "Kubernetes"
    mocker.patch.object(Kubernetes, "get_pods", return_value=k8s_pods)
    representation, instances = Container.discovery().run()
    assert len(instances) == 2
    assert representation == [36, 37, 21, 7, 7, 11]
