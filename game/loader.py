#--------------------------IMPORTS--------------------------#


import json
import os
import importlib
from game.entities.object import GameObject


#--------------------------ENTITY LOADER--------------------------#


# Dynamically imports the module for an entity by name (lowercase),
# then returns the class object with the exact given name.
# Assumes module name matches entity name in lowercase,
# and class name matches entity name exactly.
# Enables flexible entity instantiation from strings in JSON data.
def get_class(name):
    module = importlib.import_module(f"game.entities.{name.lower()}")
    return getattr(module, name)


#--------------------------LEVEL LOADER--------------------------#

def load_level(level_name: str):

    # Loads a level JSON by name from assets/layouts and returns lists
    # of instantiated objects for each layer.

    level_path = os.path.join("assets", "layouts", f"{level_name}.json")
    with open(level_path, "r") as f:
        data = json.load(f)

    layers = data.get("layers", [])

    instantiated_objects = []

    for layer in layers:
        for instance in layer.get("instances", []):
            obj_type = instance.get("type")

            try:
                cls = get_class(obj_type)
            except:
                print("No class found for obj_type: ", obj_type)
                continue

            if cls is None:
                print(f"Warning: Unknown type {obj_type} in level {level_name}")
                continue

            world = instance.get("world", {})
            x = world.get("x", 0)
            y = world.get("y", 0)
            width = world.get("width")
            height = world.get("height")

            # Some objects might need additional properties passed

            # Instantiate object with position and optional size
            game_obj = cls(x=x, y=y, width=width, height=height)

            instantiated_objects.append(game_obj)

    return instantiated_objects
