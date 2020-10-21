# -*- coding: utf-8 -*-
from types import ModuleType


def register_classes(base, module_dict):
    for name, table in base.classes.items():
        schema_name, table_name = name.split('.')
        class_name = table_name
        if schema_name not in module_dict:
            module = module_dict[schema_name] = ModuleType(schema_name)
        else:
            module = module_dict[schema_name]
        setattr(module, class_name, table)
