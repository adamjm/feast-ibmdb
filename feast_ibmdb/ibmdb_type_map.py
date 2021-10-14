from typing import Dict

import pyarrow as pa

from feast import ValueType

#TODO confirm the data types
def ibmdb_to_feast_value_type(ibmdb_type_as_str: str) -> ValueType:
    type_map: Dict[str, ValueType] = {
        "smallint": ValueType.INT32,
        "int": ValueType.INT32,
        "integer": ValueType.INT32,
        "bigint": ValueType.INT64,
        "real": ValueType.FLOAT,
        "double": ValueType.DOUBLE,
        "numeric": ValueType.DOUBLE,
        "timestamp": ValueType.UNIX_TIMESTAMP,
        "string": ValueType.STRING,
        "varchar": ValueType.STRING,
        "char": ValueType.STRING,
        "boolean": ValueType.BOOL,
    }
    return type_map[ibmdb_type_as_str.lower()]

#TODO confirm types for pyarrow to ibmdb
def pa_to_ibmdb_value_type(pa_type_as_str: str) -> str:
    # PyArrow types: https://arrow.apache.org/docs/python/api/datatypes.html
    # DB2 types: https://www.ibm.com/support/producthub/db2/docs/content/SSEPGG_11.5.0/com.ibm.db2.luw.sql.ref.doc/doc/r0008483.html
    pa_type_as_str = pa_type_as_str.lower()
    if pa_type_as_str.startswith("timestamp"):
        return "timestamp"

    if pa_type_as_str.startswith("date"):
        return "date"

    if pa_type_as_str.startswith("decimal"):
        return pa_type_as_str

    if pa_type_as_str.startswith("dictionary<values=string,"):
        return "string"

    type_map = {
        "null": "null",
        "bool": "boolean",
        "int8": "tinyint",
        "int16": "smallint",
        "int32": "int",
        "int64": "bigint",
        "uint8": "smallint",
        "uint16": "int",
        "uint32": "bigint",
        "uint64": "decimal",
        "float": "float",
        "double": "double",
        "binary": "binary",
        "string": "string",
    }
    return type_map[pa_type_as_str]


_IBMDB_TO_PA_TYPE_MAP = {
    "null": pa.null(),
    "boolean": pa.bool_(),
    "timestamp": pa.timestamp("us"),
    "date": pa.date32(),
    "smallint": pa.int16(),
    "int": pa.int32(),
    "bigint": pa.int64(),
    "float": pa.float32(),
    "double": pa.float64(),
    "binary": pa.binary(),
    "string": pa.string(),
    "varchar": pa.string(),
}


def ibmdb_to_pa_value_type(ibmdb_type_as_str: str) -> pa.DataType:
    ibmdb_type_as_str = ibmdb_type_as_str.lower()
    # if ibmdb_type_as_str.startswith("decimal"):
    #     return pa.decimal256()

    return _IBMDB_TO_PA_TYPE_MAP[hive_type_as_str]
