import pickle
from typing import Callable, Dict, Iterable, Optional, Tuple

from feast import RepoConfig, ValueType
from feast.data_source import DataSource
from feast.errors import DataSourceNotFoundException
from feast.protos.feast.core.DataSource_pb2 import DataSource as DataSourceProto
from feast_ibmdb.ibmdb_type_map import ibmdb_to_feast_value_type


class IBMdboptions:
    """
    DataSource IBM db2 options used to source features from IBM db2
    """

    def __init__(self, table: Optional[str], query: Optional[str]):
        self._table = table
        self._query = query

    @property
    def query(self):
        """
        Returns the query referenced by this source
        """
        return self._query

    @query.setter
    def query(self, query):
        """
        Sets the query referenced by this source
        """
        self._query = query

    @property
    def table(self):
        """
        Returns the table ref of this data source
        """
        return self._table

    @table.setter
    def table(self, table):
        """
        Sets the table ref of this data source
        """
        self._table = table

    @classmethod
    def from_proto(cls, ibmdb_options_proto: DataSourceProto.CustomSourceOptions):
        """
        Creates a IBMdbOptions from a protobuf representation of a IBM db option

        Args:
            ibmdb_options_proto: A protobuf representation of a DataSource

        Returns:
            Returns a IBMdbOptions object based on the ibmdb_options protobuf
        """
        ibmdb_configuration = pickle.loads(ibmdb_options_proto.configuration)

        ibmdb_options = cls(
            table=ibmdb_configuration.table, query=ibmdb_configuration.query
        )

        return ibmdb_options

    def to_proto(self) -> DataSourceProto.CustomSourceOptions:
        """
        Converts an IBMdbOptionsProto object to its protobuf representation.

        Returns:
            IBMdbOptionsProto protobuf
        """
        ibmdb_options_proto = DataSourceProto.CustomSourceOptions(
            configuration=pickle.dumps(self)
        )
        return ibmdb_options_proto


class IBMdbSource(DataSource):
    def __init__(
        self,
        table: Optional[str] = None,
        query: Optional[str] = None,
        event_timestamp_column: Optional[str] = "",
        created_timestamp_column: Optional[str] = "",
        field_mapping: Optional[Dict[str, str]] = None,
        date_partition_column: Optional[str] = "",
    ):
        assert (
            table is not None or query is not None
        ), '"table" or "query" is required for IBMdbSource.'

        super().__init__(
            event_timestamp_column,
            created_timestamp_column,
            field_mapping,
            date_partition_column,
        )

        self._ibmdb_options = IBMdbOptions(table=table, query=query)

    def __eq__(self, other):
        if not isinstance(other, IBMdbSource):
            raise TypeError("Comparisons should only involve IBMdbSource class objects.")

        return (
            self.ibmdb_options.table == other.ibmdb_options.table
            and self.ibmdb_options.query == other.ibmdb_options.query
            and self.event_timestamp_column == other.event_timestamp_column
            and self.created_timestamp_column == other.created_timestamp_column
            and self.field_mapping == other.field_mapping
            and self.date_partition_column == other.date_partition_column
        )

    @property
    def table(self):
        return self._ibmdb_options.table

    @property
    def query(self):
        return self._ibmdb_options.query

    @property
    def ibmdb_options(self):
        """
        Returns the ibmdb options of this data source
        """
        return self._ibmdb_options

    @ibmdb_options.setter
    def ibmdb_options(self, ibmdb_options):
        """
        Sets the ibm db2 options of this data source
        """
        self._ibmdb_options = ibmdb_options

    def to_proto(self) -> DataSourceProto:
        data_source_proto = DataSourceProto(
            type=DataSourceProto.CUSTOM_SOURCE,
            field_mapping=self.field_mapping,
            custom_options=self.ibmdb_options.to_proto(),
        )

        data_source_proto.event_timestamp_column = self.event_timestamp_column
        data_source_proto.created_timestamp_column = self.created_timestamp_column
        data_source_proto.date_partition_column = self.date_partition_column
        return data_source_proto

    @staticmethod
    def from_proto(data_source: DataSourceProto):

        assert data_source.HasField("custom_options")

        ibmdb_options = IBMdbOptions.from_proto(data_source.custom_options)

        return IBMdbSource(
            field_mapping=dict(data_source.field_mapping),
            table=ibmdb_options.table,
            query=ibmdb_options.query,
            event_timestamp_column=data_source.event_timestamp_column,
            created_timestamp_column=data_source.created_timestamp_column,
            date_partition_column=data_source.date_partition_column,
        )

    def validate(self, config: RepoConfig):
        self.get_table_column_names_and_types(config)

    def get_table_query_string(self) -> str:
        """Returns a string that can directly be used to reference this table in SQL"""
        if self.table:
            return f"`{self.table}`"
        else:
            return f"({self.query})"

    @staticmethod
    def source_datatype_to_feast_value_type() -> Callable[[str], ValueType]:
        return ibmdb_to_feast_value_type

    #TODO update to connect to DB2 
    def get_table_column_names_and_types(
        self, config: RepoConfig
    ) -> Iterable[Tuple[str, str]]:
        from ibm_db import conn_error()
        from ibm_db import conn_errormsg()


        from feast_ibmdb.ibmdb import IBMdbConnection

        conn = IBMdbConnection(config.offline_store)
        cursor = conn.cursor()
        if self.table is not None:
            table_splits = self.table.rsplit(".", 1)
            database_name = table_splits[0] if len(table_splits) == 2 else None
                    table_name = (
                        table_splits[1] if len(table_splits) == 2 else table_splits[0]
                    )

            try:
                ## TODO need to fix how this selects the correct table
                return cursor.get_current_schema()
            except:
                raise DataSourceNotFoundException(self.table)

        else:
            try:
                cursor.execute(f"SELECT * FROM ({self.query}) AS t LIMIT 1")
                if not cursor.fetchone():
                    raise DataSourceNotFoundException(self.query)

                    return [(field[0], field[1]) for field in cursor.description]
            except IBMdbServer2Error:
                raise DataSourceNotFoundException(self.query)
