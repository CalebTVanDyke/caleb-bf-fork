from typing import Iterable, Optional, Type

import pulumi
import pulumi_gcp

from buildflow.core.credentials import GCPCredentials
from buildflow.core.io.gcp.providers.storage import GCSBucketProvider
from buildflow.core.io.gcp.strategies.gcs_file_change_stream_strategies import (
    GCSFileChangeStreamSource,
)
from buildflow.core.providers.provider import PulumiProvider, SourceProvider
from buildflow.core.types.gcp_types import GCPProjectID
from buildflow.io.gcp.pubsub_subscription import GCPPubSubSubscription
from buildflow.io.gcp.storage import GCSBucket
from buildflow.types.gcp import GCSChangeStreamEventType


class _GCSFileChangeStreamPulumiResource(pulumi.ComponentResource):
    def __init__(
        self,
        bucket: GCSBucket,
        subscription: GCPPubSubSubscription,
        event_types: Iterable[GCSChangeStreamEventType],
        # pulumi_resource options (buildflow internal concept)
        type_: Optional[Type],
        credentials: GCPCredentials,
        opts: pulumi.ResourceOptions,
    ):
        self.bucket_resource = bucket.pulumi_provider().pulumi_resource(
            type_, credentials, opts
        )
        if self.bucket_resource is not None:
            opts = pulumi.ResourceOptions.merge(
                opts, pulumi.ResourceOptions(depends_on=self.bucket_resource)
            )
        self.subscription_resource = subscription.pulumi_provider().pulumi_resource(
            type_, credentials, opts
        )
        if self.subscription_resource is not None:
            opts = pulumi.ResourceOptions.merge(
                opts, pulumi.ResourceOptions(depends_on=self.subscription_resource)
            )

        super().__init__(
            "buildflow:gcp:storage:GCSFileChangeStream",
            f"buildflow-{bucket.project_id}-{bucket.bucket_name}",
            None,
            opts,
        )

        gcs_account = pulumi_gcp.storage.get_project_service_account(
            project=bucket.project_id,
            user_project=bucket.project_id,
        )
        self.binding = pulumi_gcp.pubsub.TopicIAMBinding(
            f"{bucket.bucket_name}-{subscription.topic.topic_name}_binding",
            opts=pulumi.ResourceOptions(parent=self),
            topic=subscription.topic.topic_name,
            role="roles/pubsub.publisher",
            project=subscription.topic.project_id,
            members=[f"serviceAccount:{gcs_account.email_address}"],
        )

        self.notification = pulumi_gcp.storage.Notification(
            f"{bucket.bucket_name}_notification",
            opts=pulumi.ResourceOptions(
                parent=self,
                depends_on=[
                    self.bucket_resource,
                    self.subscription_resource,
                    self.binding,
                ],
            ),
            bucket=bucket.bucket_name,
            topic=subscription.topic.topic_id,
            payload_format="JSON_API_V1",
            event_types=[et.name for et in event_types],
        )

        self.register_outputs(
            {
                "gcp.storage_notification.notification.": self.notification.id,
                "gcp.pubsub.topic.binding": self.binding.topic,
            }
        )


class GCSFileChangeStreamProvider(SourceProvider, PulumiProvider):
    def __init__(
        self,
        *,
        gcs_bucket: GCSBucketProvider,
        pubsub_subscription: GCPPubSubSubscription,
        project_id: GCPProjectID,
        # source-only options
        event_types: Iterable[GCSChangeStreamEventType],
        # pulumi-only options
        destroy_protection: bool = False,
    ):
        self.gcs_bucket = gcs_bucket
        self.pubsub_subscription = pubsub_subscription
        self.project_id = project_id
        # source-only options
        self.event_types = list(event_types)
        # pulumi-only options
        self.destroy_protection = destroy_protection

    def source(self, credentials: GCPCredentials):
        return GCSFileChangeStreamSource(
            project_id=self.project_id,
            credentials=credentials,
            pubsub_source=self.pubsub_subscription.source_provider().source(
                credentials
            ),
        )

    def pulumi_resource(
        self,
        type_: Optional[Type],
        credentials: GCPCredentials,
        opts: pulumi.ResourceOptions,
    ) -> Optional[pulumi.ComponentResource]:
        return _GCSFileChangeStreamPulumiResource(
            bucket=self.gcs_bucket,
            subscription=self.pubsub_subscription,
            event_types=self.event_types,
            type_=type_,
            credentials=credentials,
            opts=opts,
        )