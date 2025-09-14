import pygame
import os
from game.loader import load_layout, load_object_type
from game.objects import GameObject

def normalize_object_type(name):
    return name.lower()

def create_scene(screen, layout_name):
    layout_data = load_layout(layout_name)
    scene_objects = []

    print("[DEBUG] layout_data keys:", layout_data.keys())

    def create_game_object(inst):
        obj_type = inst.get("type")
        if not obj_type:
            return None

        obj_data = load_object_type(normalize_object_type(obj_type))

        name = inst.get("name", obj_type)
        x = inst.get("x", 0)
        y = inst.get("y", 0)
        angle = inst.get("angle", 0)

        # Try to get image path from object data
        image_path = obj_data.get("firstTexture")
        if not image_path:
            textures = obj_data.get("textures", [])
            image_path = textures[0] if textures else None

        # Fallback: guess image based on object type
        if not image_path:
            guessed_image_path = f"images/{normalize_object_type(obj_type)}.png"
            guessed_full_path = os.path.join("c3data", *guessed_image_path.split("/"))
            if os.path.exists(guessed_full_path):
                image_path = guessed_image_path

        if not image_path:
            print(f"[WARN] No image path found for object '{name}' of type '{obj_type}'")
            return None

        return GameObject(name, image_path, x, y, angle)

    # Load normal world objects
    for layer in layout_data.get("layers", []):
        instances = layer.get("instances", [])
        print(f"[DEBUG] Found {len(instances)} instances in layer '{layer.get('name')}'")
        for inst in instances:
            game_obj = create_game_object(inst)
            if game_obj:
                scene_objects.append(game_obj)

    # Load HUD/UI objects
    for inst in layout_data.get("nonworld-instances", []):
        game_obj = create_game_object(inst)
        if game_obj:
            scene_objects.append(game_obj)

    print(f"[DEBUG] Total instances loaded: {len(scene_objects)}")
    return scene_objects
