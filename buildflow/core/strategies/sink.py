from typing import Any, Callable, Type

from buildflow.core.strategies._stategy import Strategy, StrategyID, StategyType


class Batch:
    pass


class SinkStrategy(Strategy):
    strategy_type = StategyType.SINK

    def __init__(self, strategy_id: StrategyID):
        super().__init__(strategy_id=strategy_id)

    async def push(self, batch: Batch):
        """Push pushes a batch of data to the source."""
        raise NotImplementedError("push not implemented")

    def push_converter(self, user_defined_type: Type) -> Callable[[Any], Any]:
        raise NotImplementedError("push_converter not implemented")