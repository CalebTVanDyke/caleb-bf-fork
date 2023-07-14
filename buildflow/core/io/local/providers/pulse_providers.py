from typing import Any, Iterable, Optional, Type

from buildflow.core.io.local.strategies.pulse_strategies import PulseSource
from buildflow.core.providers.provider import PulumiProvider, SourceProvider


class PulseProvider(SourceProvider, PulumiProvider):
    def __init__(
        self,
        *,
        items: Iterable[Any],
        pulse_interval_seconds: float,
        backlog_size: int = 0,
        # source-only options
        # sink-only options
        # pulumi-only options
    ):
        self.items = items
        self.pulse_interval_seconds = pulse_interval_seconds
        self.backlog_size = backlog_size
        # sink-only options
        # pulumi-only options

    def source(self):
        return PulseSource(
            items=self.items,
            pulse_interval_seconds=self.pulse_interval_seconds,
            backlog_size=self.backlog_size,
        )

    def pulumi_resources(self, type_: Optional[Type]):
        # Local pulse provider does not have any Pulumi resources
        return []