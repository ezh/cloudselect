# Copyright 2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from Kubernetes namespaces."""
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
        self.log = logging.getLogger("cloudselect.discovery.Kubernetes")

    def run(self):
        """Collect Kubernetes pods."""
        self.log.debug("Discover Kubernetes pods")
        return list(self.instances())

    def instances(self):
        """Collect Kubernetes pods."""
        for i in self.find():
            metadata = self.simplify_metadata(i["metadata"])
            container = i["container"]
            instance_id = metadata["metadata"]["uid"]
            name = metadata["metadata"]["name"]
            namespace = metadata["metadata"]["namespace"]

            representation = [instance_id, name, container]
            self.enrich_representation(representation, metadata)

            instance = PodContainer(
                instance_id,
                name,
                None,
                metadata,
                representation,
                i["configuration"],
                container,
                i["context"],
                namespace,
                metadata["status"]["pod_ip"],
                metadata["status"]["host_ip"],
            )
            yield instance

    def find(self):
        """Discover pods in Kubernetes clouds."""
        cluster = Container.config.discovery.cluster()
        for cluster_id in cluster:
            patterns = [re.compile(i) for i in cluster[cluster_id].get("namespace", [])]
            configuration = cluster[cluster_id].get("configuration")
            context = cluster[cluster_id].get("context")
            pods = self.get_pods(cluster_id, configuration, context)
            for pod in pods.items:
                namespace = pod.metadata.namespace
                matched = True
                if patterns:
                    matched = False
                    for i in patterns:
                        if i.match(namespace) is not None:
                            matched = True
                            break
                if pod.status.phase == "Running" and matched:
                    for container in pod.spec.containers:
                        yield {
                            "configuration": configuration,
                            "container": container.name,
                            "context": context,
                            "metadata": pod.to_dict(),
                        }

    def get_pods(self, cluster_id, configuration, context):
        """Get list of pods from cluster."""
        api_client = config.new_client_from_config(
            config_file=configuration, context=context,
        )
        version_api = client.VersionApi(api_client=api_client)
        version = version_api.get_code()
        self.log.debug(
            "Connected to '%s', control plane version %s",
            cluster_id,
            version.git_version,
        )
        core_v1 = client.CoreV1Api(api_client=api_client)
        return core_v1.list_pod_for_all_namespaces(watch=False)
