from buildflow.core.types.portable_types import TableName, TableID, TopicID, BucketName

# TODO: Add comments to show the str patterns
# Optional TODO: Add post-init validation on the str format


# Project Level Types
GCPProjectID = str

GCPRegion = str

GCPZone = str

# BigQuery Types
BigQueryDatasetName = str

BigQueryTableName = TableName

BigQueryTableID = TableID

# PubSub Types
PubSubSubscriptionName = str

PubSubSubscriptionID = str

PubSubTopicName = str

PubSubTopicID = TopicID

# Google Cloud Storage Types
GCSBucketName = BucketName

GCSBucketURL = str