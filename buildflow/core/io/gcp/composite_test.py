import unittest

from buildflow.config.cloud_provider_config import GCPOptions
from buildflow.core.io.gcp.composite import GCSFileStream


class GCSFileStreamTest(unittest.TestCase):
    def test_from_gcp_options(self):
        options = GCPOptions(
            default_project_id="pid",
            default_region="central",
            default_zone="central1-a",
        )
        stream = GCSFileStream.from_gcp_options(options, "my-bucket")
        self.assertEqual(stream.gcs_bucket.bucket_name, "my-bucket")
        self.assertEqual(
            stream.pubsub_subscription.subscription_name, "my-bucket_subscription"
        )
        self.assertEqual(stream.pubsub_topic.topic_name, "my-bucket_topic")


if __name__ == "__main__":
    unittest.main()
