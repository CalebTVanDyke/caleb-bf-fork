from dataclasses import dataclass
from typing import Optional


@dataclass
class StreamingOptions:
    # The minimum number of replicas to maintain.
    min_replicas: int = 1
    # The maximum number of replicas to scale up to.
    max_replicas: int = 100
    # The number of replicas to start your pipeline with. If not set we will
    # start with whatever min_replicas is set to.
    num_replicas: Optional[int] = None
    # Whether or not we should autoscale your number of replicas. If this is
    # set to false your pipeline will always maintain the same number of
    # replicas as it started with.
    autoscaling: bool = True
    # If true flow.run() will block as the pipeline executes. If false we will
    # return a async ref allowing you to block with:
    #       ray.get(flow.run()['PROC_NAME'])
    blocking: bool = True
