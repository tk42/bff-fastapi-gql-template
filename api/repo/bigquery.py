import os
from google.cloud import bigquery
from api.model.models import Task
from bq_schema import RowTransformer

project = os.environ.get("PROJECT_ID")


class BigQueryRepository:
    def __init__(self, ds: str, tbl: str) -> None:
        self._client = bigquery.Client()
        self._loc = f"{project}.{ds}.{tbl}"
        self.row_transformer = RowTransformer[Task](Task)

    async def find_by_id(self, id: str) -> Task:
        query = f"SELECT * FROM {self.loc} WHERE id == {id}"
        for row in self._client.query(query=query):
            deserialized_row = self.row_transformer.bq_row_to_dataclass_instance(row)
            assert isinstance(deserialized_row, Task)
            return deserialized_row

    async def find_all(self) -> list[Task]:
        query = f"SELECT * FROM {self.loc}"
        tasks = []
        for row in self._client.query(query=query):
            deserialized_row = self.row_transformer.bq_row_to_dataclass_instance(row)
            assert isinstance(deserialized_row, Task)
            tasks += [deserialized_row]
        return tasks

    async def save(self, task: Task) -> None:
        serialized_row = RowTransformer.dataclass_instance_to_bq_row(task)
        table = self._client.get_table(f"{self.loc}")
        self._client.insert_rows(table, [serialized_row])

    async def delete(self, task: Task) -> None:
        query = f"DELETE * FROM {self.loc} WHERE id == {str(task.id)}"
        for row in self._client.query(query=query):
            self.row_transformer.bq_row_to_dataclass_instance(row)
