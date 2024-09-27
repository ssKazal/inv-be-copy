import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from inventory.custom.general_data import groups_and_permissions


class Command(BaseCommand):
    """
    To run this command start env and type
            ```python manage.py create_groups_and_permissions```
    This will create all the groups and it's permission in the beginning of installing the projects
    """

    help = "Create Groups While Installing Project [ Need To Call Once With Frist Migration ]"

    def handle(self, *args, **kwargs):
        for group_name, permissions_name in groups_and_permissions.items():
            group_obj, created = Group.objects.get_or_create(name=group_name)
            permissons = Permission.objects.filter(name__in=permissions_name)
            group_obj.permissions.set(permissons)

            if len(permissions_name) != len(permissons):
                num_of_permission = len(permissions_name) - len(permissons)
                logging.warning(
                    "{} permissions don't found in '{}' group.".format(
                        num_of_permission, group_obj
                    )
                )
                continue

        self.stdout.write("Group created")
