# Copyright 2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from Kubernetes namespaces."""
import copy
import logging
import re

from kubernetes import client, config

from cloudselect import Container, PodContainer

from . import DiscoveryService


class Kubernetes(DiscoveryService):
    """Class implementing discovery service plugin."""

    log = None

    def __init__(self):
        """Class constructor."""
        self.log = logging.getLogger("cloudselect.discovery.kubernetes")

    def run(self):
        """Collect Kubernetes pods."""
        self.log.debug("Discover Kubernetes pods")
        return list(self.instances())

    def instances(self):
        """Collect Kubernetes pods."""
        for i in self.find():
            instance_id = i["metadata"]["uid"]
            metadata = self.simplify_metadata(i)
            configuration = i["cluster"]["configuration"]
            container = i["container"]
            context = i["cluster"]["context"]
            ip = i["status"]["pod_ip"]
            name = i["metadata"]["name"]
            namespace = i["metadata"]["namespace"]
            node_ip = i["status"]["host_ip"]

            representation = [instance_id, name, container]
            self.enrich_representation(representation, metadata)

            instance = PodContainer(
                instance_id,
                name,
                None,
                metadata,
                representation,
                configuration,
                container,
                context,
                namespace,
                ip,
                node_ip,
            )
            yield instance

    def find(self):
        """Discover pods in Kubernetes clouds."""
        cluster = Container.config.discovery.cluster()
        for cluster_id in cluster:
            patterns = [re.compile(i) for i in cluster[cluster_id].get("namespace", [])]
            config_file = cluster[cluster_id].get("configuration")
            context = cluster[cluster_id].get("context")
            api_client = config.new_client_from_config(
                config_file=config_file, context=context,
            )
            version_api = client.VersionApi(api_client=api_client)
            version = version_api.get_code()
            self.log.debug(
                "Connected to '%s', control plane version %s",
                cluster_id,
                version.git_version,
            )
            core_v1 = client.CoreV1Api(api_client=api_client)
            ret = core_v1.list_pod_for_all_namespaces(watch=False)
            for pod in ret.items:
                for container in pod.spec.containers:
                    instance = copy.deepcopy(pod.to_dict())
                    if instance["status"]["phase"] == "Running":
                        instance["cluster"] = {
                            "configuration": config_file,
                            "context": context,
                        }
                        instance["container"] = container.name
                        if patterns:
                            namespace = instance["metadata"]["namespace"]
                            matched = next(
                                (m for m in patterns if m.match(namespace) is not None),
                                None,
                            )
                            if matched is not None:
                                yield instance
                        else:
                            yield instance
