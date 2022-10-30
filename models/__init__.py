__all__ = []
import os
script_path = os.path.dirname(__file__)
for file in os.scandir(script_path):
    if file.name.endswith('.py') and not file.name == '__init__.py':
        __all__.append(file.name[:-3])
