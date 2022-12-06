import os
from google.cloud import bigquery
from api.model.models import Task
from bq_schema.row_transformer import RowTransformer
from bq_schema.cli.migrate_tables import main as migrate_tables

project = os.environ.get("PROJECT_ID")


class BigQueryRepository:
    def __init__(self, ds: str, tbl: str) -> None:
        self._client = bigquery.Client()
        self._loc = f"{project}.{ds}.{tbl}"
        self.row_transformer = RowTransformer[Task](Task)
        dataset = self._client.get_dataset(ds)
        if dataset is None:
            dataset = bigquery.Dataset(f"{project}.{ds}")
            dataset.location = "US"
            self._client.create_dataset(dataset, timeout=30)

        # TODO:
        # ルートディレクトリに my_table.py その中に MyTable クラスを配置するということが大事そう
        # https://github.com/limehome/bq-schema
        # それ以外のパスの場合は下記を読みとく必要がある
        # https://github.com/limehome/bq-schema/blob/b33f349c6e7b7d5191971e847a3f6019c7efe07a/bq_schema/migration/table_finder.py#L12
        migrate_tables(project, ds, tbl, True, False, False)
        print("Complete BigQueryRepository Initialization")

    async def find_by_id(self, id: str) -> Task:
        query = f"SELECT * FROM {self._loc} WHERE id == {id}"
        for row in self._client.query(query=query):
            deserialized_row = self.row_transformer.bq_row_to_dataclass_instance(row)
            assert isinstance(deserialized_row, Task)
            return deserialized_row

    async def find_all(self) -> list[Task]:
        query = f"SELECT * FROM {self._loc}"
        tasks = []
        for row in self._client.query(query=query):
            deserialized_row = self.row_transformer.bq_row_to_dataclass_instance(row)
            assert isinstance(deserialized_row, Task)
            tasks += [deserialized_row]
        return tasks

    async def save(self, task: Task) -> None:
        serialized_row = RowTransformer.dataclass_instance_to_bq_row(task)
        table = self._client.get_table(self._loc)
        self._client.insert_rows(table, [serialized_row])

    async def delete(self, task: Task) -> None:
        query = f"DELETE * FROM {self._loc} WHERE id == {str(task.id)}"
        for row in self._client.query(query=query):
            self.row_transformer.bq_row_to_dataclass_instance(row)
