# Copyright 2020 Alexey Aksenov and individual contributors
# See the LICENSE.txt file at the top-level directory of this distribution.
#
# Licensed under the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>
# This file may not be copied, modified, or distributed
# except according to those terms.
"""Module collecting instances from Kubernetes namespaces."""
import logging
import os
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
        instances = list(self.instances())
        representation = instances[-1]
        del instances[-1]
        return (representation, instances)

    def instances(self):
        """Collect Kubernetes pods."""
        # Array with maximum field length for each element in representation
        fields_length = []
        for i in self.find():
            metadata = self.simplify_metadata(i["metadata"])
            container = i["container"]
            instance_id = metadata["metadata"]["uid"]
            name = metadata["metadata"]["name"]
            namespace = metadata["metadata"]["namespace"]

            representation = [instance_id, name, container]
            self.enrich_representation(representation, metadata)

            # Update maximum field length
            for idx, value in enumerate(representation):
                if idx >= len(fields_length):
                    fields_length.append(len(value))
                else:
                    fields_length[idx] = max(fields_length[idx], len(value))

            yield PodContainer(
                instance_id,
                name,
                None,
                metadata,
                representation,
                i["aws_profile"],
                i["aws_region"],
                i["configuration"],
                container,
                i["context"],
                metadata["status"]["pod_ip"],
                namespace,
                metadata["status"]["host_ip"],
            )
        yield fields_length

    @staticmethod
    def aws_apply(aws_profile, aws_region):
        """Apply AWS environmen variables if necessary.

        Those variables are using by k8s aws-iam-authenticator.
        """
        aws_profile_save = os.environ.get("AWS_PROFILE")
        aws_region_save = os.environ.get("AWS_REGION")
        if aws_profile:
            os.environ["AWS_PROFILE"] = aws_profile
        if aws_region:
            os.environ["AWS_REGION"] = aws_region
        return [aws_profile_save, aws_region_save]

    @staticmethod
    def aws_restore(aws_profile, aws_region):
        """Restore AWS environment variables."""
        if aws_profile:
            os.environ["AWS_PROFILE"] = aws_profile
        else:
            del os.environ["AWS_PROFILE"]
        if aws_profile:
            os.environ["AWS_REGION"] = aws_region
        else:
            del os.environ["AWS_REGION"]

    def find(self):
        """Discover pods in Kubernetes clouds."""
        cluster = Container.config.discovery.cluster()
        for cluster_id in cluster:
            aws_profile = cluster[cluster_id].get("aws_profile")
            aws_region = cluster[cluster_id].get("aws_region")
            configuration = cluster[cluster_id].get("configuration")
            context = cluster[cluster_id].get("context")
            patterns = [re.compile(i) for i in cluster[cluster_id].get("namespace", [])]
            aws_envs = self.aws_apply(aws_profile, aws_region)
            pods = self.get_pods(cluster_id, configuration, context)
            self.aws_restore(*aws_envs)
            for pod in pods:
                if pod["status"]["phase"] in ["Running"] and (
                    not patterns
                    or any(
                        i.match(pod["metadata"]["namespace"]) is not None
                        for i in patterns
                    )
                ):
                    for container in pod["spec"]["containers"]:
                        yield {
                            "aws_profile": aws_profile,
                            "aws_region": aws_region,
                            "configuration": configuration,
                            "container": container["name"],
                            "context": context,
                            "metadata": pod,
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
        return [
            i.to_dict() for i in core_v1.list_pod_for_all_namespaces(watch=False).items
        ]
