# feast-ibmdb
IBM Db2 support for Feast offline store

# Feast db2 Support

!!NOTE this is a work in progress and may not work!!

IBM Db2 databases are not included in the current [Feast](https://github.com/feast-dev/feast) roadmap, this project intends to add Db2 Warehouse support as an Offline Store.  

This project draws heavily from the *feast-hive* impliementation (https://github.com/baineng/feast-hive) and could not have progressed this far without the work by Benn Ma.

**Important:** This project is still being developed and not ready for using yet.

## Quickstart

#### Install feast

```shell
pip install feast
```

#### Install feast-db2-warehouse

Install the latest dev version by pip:

```shell
pip install git+https://github.ibm.com/anz-tech-garage/feast-db2-warehouse.git 
```

or by clone the repo:

```shell
git clone https://github.ibm.com/anz-tech-garage/feast-db2-warehouse.git
cd feast-db2-warehouse
python setup.py install
```

#### Create a feature repository

```shell
feast init feature_repo
cd feature_repo
```

#### Edit `feature_store.yaml`

set `offline_store` type to be `feast_ibmdb_warehouse.IBMdbOfflineStore`

```yaml
project: ...
registry: ...
provider: local
offline_store:
    type: feast_ibmdb_warehouse.IBMdbOfflineStore
    host: localhost
    port: 10000 # default
    ... # other parameters
online_store:
    ...
```

#### Add `ibmdbwarehouse_example.py`

```python
# This is an example feature definition file

from google.protobuf.duration_pb2 import Duration

from feast import Entity, Feature, FeatureView, ValueType
from feast_ibmdbwarehouse import IBMdbwarehouseSource

# Read data from Hive table
# Need make sure the table_ref exists and have data before continue.
driver_hourly_stats = IBMdbwarehouseSource(
    table_ref='example.driver_stats',
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)

# Define an entity for the driver.
driver = Entity(name="driver_id", value_type=ValueType.INT64, description="driver id",)

# Define FeatureView
driver_hourly_stats_view = FeatureView(
    name="driver_hourly_stats",
    entities=["driver_id"],
    ttl=Duration(seconds=86400 * 1),
    features=[
        Feature(name="conv_rate", dtype=ValueType.FLOAT),
        Feature(name="acc_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_daily_trips", dtype=ValueType.INT64),
    ],
    online=True,
    input=driver_hourly_stats,
    tags={},
)
```

#### Apply the feature definitions

```shell
feast apply
```

#### Generating training data and so on

The rest are as same as [Feast Quickstart](https://docs.feast.dev/quickstart#generating-training-data)


## Developing and Testing

#### Developing

```shell
git clone https://github.ibm.com/anz-tech-garage/feast-db2-warehouse.git
cd feast-db2-warehouse   
# creating virtual env ...
pip install -e .[dev]

# before commit
make format
makr lint
```

#### Testing

```shell
pip install -e .[test]
pytest --ibmdbwarehouse_host=localhost --ibmdbwarehouse_port=10000
```
