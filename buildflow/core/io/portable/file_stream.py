"""Allows listening to file changes."""
import dataclasses

from buildflow.config.cloud_provider_config import CloudProvider, CloudProviderConfig
from buildflow.core.io.gcp.composite import GCSFileChangeStream
from buildflow.core.io.primitive import PortablePrimtive, Primitive
from buildflow.core.strategies._strategy import StategyType
from buildflow.core.types.portable_types import FilePath


@dataclasses.dataclass
class FileStream(PortablePrimtive):
    file_path: FilePath

    def to_cloud_primitive(
        self, cloud_provider_config: CloudProviderConfig, strategy_type: StategyType
    ) -> Primitive:
        # GCP Implementations
        if cloud_provider_config.default_cloud_provider == CloudProvider.GCP:
            if strategy_type == StategyType.SOURCE:
                return GCSFileChangeStream.from_gcp_options(
                    gcp_options=cloud_provider_config.gcp_options,
                    bucket_name=self.file_path,
                )
            elif strategy_type == StategyType.SINK:
                raise ValueError(
                    f"Unsupported strategy type for FileStream (GCP): {strategy_type}"
                )
        # AWS Implementations
        elif cloud_provider_config.default_cloud_provider == CloudProvider.AWS:
            raise NotImplementedError("AWS is not implemented for FileStream.")
        # Azure Implementations
        elif cloud_provider_config.default_cloud_provider == CloudProvider.AZURE:
            raise NotImplementedError("Azure is not implemented for FileStream.")
        # Local Implementations
        elif cloud_provider_config.default_cloud_provider == CloudProvider.LOCAL:
            raise NotImplementedError("Local is not implemented for FileStream.")
        # Sanity check
        else:
            raise ValueError(
                f"Unknown resource provider: {cloud_provider_config.default_cloud_provider}"  # noqa: E501
            )
