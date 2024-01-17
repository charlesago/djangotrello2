from django.contrib.auth.models import User
from django.db import models


# Create your models here

class WorkspaceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Visibility(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(WorkspaceType, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='workspace_members')
    owner = models.ForeignKey(User, null=True, related_name='workspace_owner', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='members')
    is_starred = models.BooleanField(default=False)
    visibility = models.ForeignKey(Visibility, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, null=False, on_delete=models.CASCADE, related_name='boards')


class List(models.Model):
    name = models.CharField(max_length=255, default="liste non nommée")
    board = models.ForeignKey(Board, default="test", null=False, on_delete=models.CASCADE, related_name='lists')


class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    list = models.ForeignKey(List, null=False, related_name='cards', on_delete=models.CASCADE)


"""
class ArchiveList(models.Model):
    archived_items = models.ManyToManyField(List, related_name='archived_lists')
"""