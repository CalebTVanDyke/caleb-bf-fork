import dataclasses
import enum

from buildflow.types.portable import FileChangeEvent, PortableFileChangeEventType


class FileChangeStreamEventType(enum.Enum):
    CREATED = "created"
    DELETED = "deleted"
    MODIFIED = "modified"
    MOVED = "moved"

    @classmethod
    def from_portable_type(cls, portable_type: PortableFileChangeEventType):
        try:
            return cls(portable_type.value)
        except ValueError:
            raise ValueError(
                "Cannot convert portable file event type to local file "
                f"event type: {portable_type}"
            ) from None


@dataclasses.dataclass
class LocalFileChangeEvent(FileChangeEvent):
    event_type: FileChangeStreamEventType

    @property
    def blob(self) -> bytes:
        if self.metadata["eventType"] == "deleted":
            raise ValueError("Can't fetch blob for `delete` event.")
        with open(self.metadata["srcPath"], "rb") as f:
            return f.read()
