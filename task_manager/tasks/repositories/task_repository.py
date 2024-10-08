from django.db.models import Q

from task_manager.common.base_repositories import BaseRepository
from task_manager.tasks.entities.task_entity import (
    TaskEntity,
    TaskInput,
)
from task_manager.tasks.models import Task


class TaskRepository(BaseRepository):
    def __init__(self):
        self.task = Task

    def is_object_name_free(self, name: str, task_id: int) -> bool:
        return not self.task.objects.filter(
            Q(name=name) & ~Q(id=task_id),
        ).exists()

    def get_all_objects(self, query=Q()) -> list[TaskEntity]:
        tasks = self.task.objects.filter(query).select_related(
            "status",
            "author",
            "executor",
        ).prefetch_related('labels')

        return [task.to_entity() for task in tasks]

    def create_object(self, task: TaskInput) -> None:
        new_task = self.task.objects.create(
            name=task.name,
            description=task.description,
            status=task.status,
            author=task.author,
            executor=task.executor,
        )

        new_task.labels.set(task.labels)

    def update_object(self, task_id: int, new_task: TaskInput) -> None:
        task = self.task.objects.get(pk=task_id)
        task.name = new_task.name
        task.description = new_task.description
        task.status = new_task.status
        task.author = new_task.author
        task.executor = new_task.executor
        task.labels.set(new_task.labels)
        task.save()

    def delete_object(self, task_id: int) -> None:
        self.task.objects.filter(id=task_id).delete()

    def get_object(self, task_id: int) -> TaskEntity:
        return (
            self.task.objects.filter(id=task_id)
            .select_related("status", "author", "executor")
            .prefetch_related('labels')
            .get()
            .to_entity()
        )
