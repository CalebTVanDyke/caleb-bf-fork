import enum


# TODO: allow users to set as a string
class FileFormat(enum.Enum):
    # TODO: Support additional file formats (Arrow, Avro, etc..)
    PARQUET = 1
    CSV = 2
    JSON = 3


FilePath = str
