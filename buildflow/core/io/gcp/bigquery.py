import dataclasses
from typing import Optional
from buildflow.core import utils
from buildflow.core.io.primitive import GCPPrimtive
from buildflow.config.cloud_provider_config import GCPOptions
from buildflow.core.types.gcp_types import (
    BigQueryDatasetName,
    GCPProjectID,
    BigQueryTableID,
    BigQueryTableName,
)
from buildflow.core.io.gcp.providers.bigquery_providers import (
    BigQueryTableProvider,
)
from buildflow.core.types.portable_types import TableName


@dataclasses.dataclass
class BigQueryTable(GCPPrimtive):
    project_id: GCPProjectID
    dataset_name: BigQueryDatasetName
    table_name: BigQueryTableName
    destroy_protection: bool = True

    @property
    def table_id(self) -> BigQueryTableID:
        return f"{self.project_id}.{self.dataset_name}.{self.table_name}"

    @classmethod
    def from_gcp_options(
        cls,
        gcp_options: GCPOptions,
        *,
        table_name: Optional[TableName] = None,
    ) -> "BigQueryTable":
        project_id = gcp_options.default_project_id
        if project_id is None:
            raise ValueError(
                "No Project ID was provided in the GCP options. Please provide one in "
                "the .buildflow config."
            )
        project_hash = utils.stable_hash(project_id)
        if table_name is None:
            table_name = f"table_{project_hash[:8]}"
        return cls(
            project_id=project_id,
            dataset_name="buildflow_managed",
            table_name=table_name,
            destroy_protection=True,
        )

    def sink_provider(self) -> BigQueryTableProvider:
        # TODO: Add support to supply the sink-only options
        return BigQueryTableProvider(
            project_id=self.project_id,
            dataset_name=self.dataset_name,
            table_name=self.table_name,
            destroy_protection=self.destroy_protection,
        )

    def pulumi_provider(self) -> BigQueryTableProvider:
        # TODO: Add support to supply the pulumi-only options
        return BigQueryTableProvider(
            project_id=self.project_id,
            dataset_name=self.dataset_name,
            table_name=self.table_name,
            destroy_protection=self.destroy_protection,
        )