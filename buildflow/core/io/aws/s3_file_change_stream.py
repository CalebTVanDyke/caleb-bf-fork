import dataclasses
from typing import Iterable
from buildflow.config.cloud_provider_config import AWSOptions

from buildflow.core.io.aws.s3 import S3Bucket
from buildflow.core.io.aws.sqs import SQSQueue
from buildflow.core.io.primitive import AWSPrimtive, CompositePrimitive
from buildflow.core.types.aws_types import S3BucketName, S3ChangeStreamEventType
from buildflow.core.io.aws.providers.s3_file_change_stream_provider import (
    S3FileChangeStreamProvider,
)


@dataclasses.dataclass
class S3FileChangeStream(AWSPrimtive, CompositePrimitive):
    s3_bucket: S3Bucket
    event_types: Iterable[S3ChangeStreamEventType] = (
        S3ChangeStreamEventType.OBJECT_CREATED_ALL,
    )

    # The sqs queue is always managed by the S3FileChangeStream and
    # is setup in __post_init__ based on the bucket configuration.
    sqs_queue: SQSQueue = dataclasses.field(init=False)

    def __post_init__(self):
        self.sqs_queue = SQSQueue(
            queue_name=f"{self.s3_bucket.bucket_name}_queue",
            aws_region=self.s3_bucket.aws_region,
        ).options(managed=True)

    @classmethod
    def from_aws_options(
        cls, aws_options: AWSOptions, bucket_name: S3BucketName
    ) -> AWSPrimtive:
        bucket = S3Bucket.from_aws_options(
            aws_options, bucket_name=bucket_name
        ).options(managed=True)
        return cls(bucket)

    def source_provider(self) -> S3FileChangeStreamProvider:
        return S3FileChangeStreamProvider(
            s3_bucket_provider=None,
            sqs_queue_provider=self.sqs_queue.source_provider(),
            event_types=self.event_types,
        )

    def pulumi_provider(self) -> S3FileChangeStreamProvider:
        return S3FileChangeStreamProvider(
            s3_bucket_provider=self.s3_bucket.pulumi_provider(),
            sqs_queue_provider=self.sqs_queue.pulumi_provider(),
            bucket_managed=self.s3_bucket.managed,
            event_types=self.event_types,
        )