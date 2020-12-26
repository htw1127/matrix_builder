from Group import *


class GroupList:
    def __init__(self):
        self.group_dict = dict()

    def add_group(self, group):
        if self.contains(group.get_name()):
            return

        self.group_dict[group.get_name()] = group

    def delete_group(self, group_name):
        self.group_dict.pop(group_name)

    def get_group(self, group_name):
        if not self.contains(group_name):
            return None
        return self.group_dict[group_name]

    def contains(self, group_name):
        return group_name in self.group_dict.keys()
