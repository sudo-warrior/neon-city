"""
Neon Crucible - Building Windows Implementation
Blender 4.2 Python Script for generating windows for buildings in the Neon Crucible cyberpunk world.
This script implements windows for all buildings based on their architectural style and tier level.
"""

import bpy
import bmesh
import random
import math
from mathutils import Vector

def create_neotech_windows(neotech_objects, materials, interior_materials):
    """Create windows for NeoTech Labs Tower (Upper Tier)"""
    # Extract objects from the neotech_objects dictionary
    tower = neotech_objects.get("tower")
    collection = neotech_objects.get("collection")
    
    if not tower or not collection:
        print("Error: Missing required NeoTech Tower objects")
        return None
    
    # Create a subcollection for window objects
    if "NeoTech_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("NeoTech_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["NeoTech_Windows"]
    
    window_objects = []
    
    # Get tower location and dimensions
    tower_loc = tower.location
    tower_radius = tower.dimensions.x / 2
    tower_height = tower.dimensions.z
    
    # Create windows in a spiral pattern up the tower
    window_count = 40
    for i in range(window_count):
        # Calculate position in a spiral pattern
        height_fraction = i / window_count
        angle = height_fraction * 8 * math.pi  # 4 full rotations
        
        window_x = tower_loc[0] + tower_radius * 0.9 * math.cos(angle)
        window_y = tower_loc[1] + tower_radius * 0.9 * math.sin(angle)
        window_z = tower_loc[2] - tower_height/2 + height_fraction * tower_height * 0.9 + 10
        
        # Create window frame
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"NeoTech_WindowFrame_{i}"
        
        # Edit the window frame
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Scale window frame
        for v in bm.verts:
            v.co.x *= 2.0
            v.co.y *= 0.1
            v.co.z *= 3.0
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward from tower center
        direction = Vector((window_x, window_y, 0)) - Vector((tower_loc[0], tower_loc[1], 0))
        rot_quat = direction.to_track_quat('Y', 'Z')
        window_frame.rotation_euler = rot_quat.to_euler()
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign material
        window_frame.data.materials.append(interior_materials["NeoTech_Interior"])
        
        window_objects.append(window_frame)
        
        # Create window glass
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.05, window_z)
        )
        window_glass = bpy.context.active_object
        window_glass.name = f"NeoTech_WindowGlass_{i}"
        
        # Edit the window glass
        bm = bmesh.from_edit_mesh(window_glass.data)
        
        # Scale window glass
        for v in bm.verts:
            v.co.x *= 1.8
            v.co.y *= 0.05
            v.co.z *= 2.8
        
        # Update mesh
        bmesh.update_edit_mesh(window_glass.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward from tower center
        window_glass.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign glass material
        window_glass.data.materials.append(interior_materials["NeoTech_Glass"])
        
        window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

def create_specter_windows(specter_objects, materials, interior_materials):
    """Create windows for Specter Station (Mid Tier)"""
    # Extract objects from the specter_objects dictionary
    tower = specter_objects.get("tower")
    collection = specter_objects.get("collection")
    
    if not tower or not collection:
        print("Error: Missing required Specter Station objects")
        return None
    
    # Create a subcollection for window objects
    if "Specter_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("Specter_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["Specter_Windows"]
    
    window_objects = []
    
    # Get tower location and dimensions
    tower_loc = tower.location
    tower_radius = tower.dimensions.x / 2
    tower_height = tower.dimensions.z
    
    # Create broken windows at random positions on the tower
    window_count = 15
    for i in range(window_count):
        # Calculate random position
        angle = random.uniform(0, 2 * math.pi)
        height_fraction = random.uniform(0.2, 0.9)
        
        window_x = tower_loc[0] + tower_radius * 1.1 * math.cos(angle)
        window_y = tower_loc[1] + tower_radius * 1.1 * math.sin(angle)
        window_z = tower_loc[2] - tower_height/2 + height_fraction * tower_height
        
        # Create window frame
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"Specter_WindowFrame_{i}"
        
        # Edit the window frame
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Scale window frame
        for v in bm.verts:
            v.co.x *= 1.5
            v.co.y *= 0.1
            v.co.z *= 2.0
        
        # Distort frame to look damaged
        for v in bm.verts:
            if random.random() > 0.7:
                v.co.x += random.uniform(-0.2, 0.2)
                v.co.z += random.uniform(-0.2, 0.2)
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward from tower center
        direction = Vector((window_x, window_y, 0)) - Vector((tower_loc[0], tower_loc[1], 0))
        rot_quat = direction.to_track_quat('Y', 'Z')
        window_frame.rotation_euler = rot_quat.to_euler()
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign material
        window_frame.data.materials.append(interior_materials["Specter_Interior"])
        
        window_objects.append(window_frame)
        
        # Create broken window glass (only for some windows)
        if random.random() > 0.3:  # 70% chance to have glass
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(window_x, window_y + 0.05, window_z)
            )
            window_glass = bpy.context.active_object
            window_glass.name = f"Specter_WindowGlass_{i}"
            
            # Edit the window glass
            bm = bmesh.from_edit_mesh(window_glass.data)
            
            # Scale window glass
            for v in bm.verts:
                v.co.x *= 1.3
                v.co.y *= 0.05
                v.co.z *= 1.8
            
            # Break the glass by deleting some vertices
            verts_to_delete = []
            for v in bm.verts:
                if random.random() > 0.7:
                    verts_to_delete.append(v)
            
            if verts_to_delete and len(verts_to_delete) < len(bm.verts):  # Don't delete all vertices
                bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
            
            # Update mesh
            bmesh.update_edit_mesh(window_glass.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Rotate window to face outward from tower center
            window_glass.rotation_euler = window_frame.rotation_euler
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Create cracked glass material
            cracked_glass = bpy.data.materials.new(name=f"Specter_CrackedGlass_{i}")
            cracked_glass.use_nodes = True
            nodes = cracked_glass.node_tree.nodes
            links = cracked_glass.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # Light gray
            principled.inputs['Metallic'].default_value = 0.1
            principled.inputs['Roughness'].default_value = 0.2
            #principled.inputs['Transmission'].default_value = 0.8  # Mostly transparent
            principled.inputs['IOR'].default_value = 1.45
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign glass material
            window_glass.data.materials.append(cracked_glass)
            
            window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

def create_black_nexus_windows(black_nexus_objects, materials, interior_materials):
    """Create windows for Black Nexus (Lower Tier)"""
    # Extract objects from the black_nexus_objects dictionary
    building = black_nexus_objects.get("building")
    collection = black_nexus_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Black Nexus objects")
        return None
    
    # Create a subcollection for window objects
    if "BlackNexus_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("BlackNexus_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["BlackNexus_Windows"]
    
    window_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create a few small, heavily reinforced windows
    window_count = 5
    for i in range(window_count):
        # Calculate position on the upper part of the building
        side = i % 4  # 0=front, 1=right, 2=back, 3=left
        
        if side == 0:
            window_x = building_loc[0]
            window_y = building_loc[1] - building_size.y/2
        elif side == 1:
            window_x = building_loc[0] + building_size.x/2
            window_y = building_loc[1]
        elif side == 2:
            window_x = building_loc[0]
            window_y = building_loc[1] + building_size.y/2
        else:  # side == 3
            window_x = building_loc[0] - building_size.x/2
            window_y = building_loc[1]
        
        # Randomize position slightly
        window_x += random.uniform(-1.0, 1.0)
        window_y += random.uniform(-1.0, 1.0)
        
        # Position near the top
        window_z = building_loc[2] + building_size.z/2 - random.uniform(1.0, 3.0)
        
        # Create window frame (reinforced)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"BlackNexus_WindowFrame_{i}"
        
        # Edit the window frame
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Scale window frame (small)
        for v in bm.verts:
            v.co.x *= 1.0
            v.co.y *= 0.3
            v.co.z *= 0.8
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward
        if side == 0:
            window_frame.rotation_euler.z = math.radians(0)
        elif side == 1:
            window_frame.rotation_euler.z = math.radians(90)
        elif side == 2:
            window_frame.rotation_euler.z = math.radians(180)
        else:  # side == 3
            window_frame.rotation_euler.z = math.radians(270)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign material
        window_frame.data.materials.append(interior_materials["BlackNexus_Interior"])
        
        window_objects.append(window_frame)
        
        # Create window bars
        for j in range(3):
            bar_offset = (j - 1) * 0.25
            
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(window_x, window_y, window_z + bar_offset)
            )
            window_bar = bpy.context.active_object
            window_bar.name = f"BlackNexus_WindowBar_{i}_{j}"
            
            # Scale bar
            window_bar.scale.x = 1.0
            window_bar.scale.y = 0.05
            window_bar.scale.z = 0.05
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Rotate bar to match window
            window_bar.rotation_euler = window_frame.rotation_euler
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            window_bar.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            window_objects.append(window_bar)
        
        # Create window glass (dark tinted)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.1, window_z)
        )
        window_glass = bpy.context.active_object
        window_glass.name = f"BlackNexus_WindowGlass_{i}"
        
        # Edit the window glass
        bm = bmesh.from_edit_mesh(window_glass.data)
        
        # Scale window glass
        for v in bm.verts:
            v.co.x *= 0.8
            v.co.y *= 0.05
            v.co.z *= 0.6
        
        # Update mesh
        bmesh.update_edit_mesh(window_glass.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to match frame
        window_glass.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create dark tinted glass material
        dark_glass = bpy.data.materials.new(name=f"BlackNexus_DarkGlass_{i}")
        dark_glass.use_nodes = True
        nodes = dark_glass.node_tree.nodes
        links = dark_glass.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)  # Very dark
        principled.inputs['Metallic'].default_value = 0.1
        principled.inputs['Roughness'].default_value = 0.3
        #principled.inputs['Transmission'].default_value = 0.5  # Semi-transparent
        principled.inputs['IOR'].default_value = 1.45
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign glass material
        window_glass.data.materials.append(dark_glass)
        
        window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

def create_wire_nest_windows(wire_nest_objects, materials, interior_materials):
    """Create windows for Wire Nest (Mid Tier hacker den)"""
    # Extract objects from the wire_nest_objects dictionary
    building = wire_nest_objects.get("building")
    collection = wire_nest_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Wire Nest objects")
        return None
    
    # Create a subcollection for window objects
    if "WireNest_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("WireNest_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["WireNest_Windows"]
    
    window_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create a few small, concealed windows
    window_count = 6
    for i in range(window_count):
        # Calculate position on the building
        side = i % 4  # 0=front, 1=right, 2=back, 3=left
        
        if side == 0:
            window_x = building_loc[0]
            window_y = building_loc[1] - building_size.y/2
        elif side == 1:
            window_x = building_loc[0] + building_size.x/2
            window_y = building_loc[1]
        elif side == 2:
            window_x = building_loc[0]
            window_y = building_loc[1] + building_size.y/2
        else:  # side == 3
            window_x = building_loc[0] - building_size.x/2
            window_y = building_loc[1]
        
        # Randomize position slightly
        window_x += random.uniform(-1.0, 1.0)
        window_y += random.uniform(-1.0, 1.0)
        
        # Randomize height
        window_z = building_loc[2] + random.uniform(-building_size.z/3, building_size.z/3)
        
        # Create window frame (concealed)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"WireNest_WindowFrame_{i}"
        
        # Edit the window frame
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Scale window frame (small)
        for v in bm.verts:
            v.co.x *= 0.8
            v.co.y *= 0.2
            v.co.z *= 0.6
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward
        if side == 0:
            window_frame.rotation_euler.z = math.radians(0)
        elif side == 1:
            window_frame.rotation_euler.z = math.radians(90)
        elif side == 2:
            window_frame.rotation_euler.z = math.radians(180)
        else:  # side == 3
            window_frame.rotation_euler.z = math.radians(270)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign material
        window_frame.data.materials.append(interior_materials["WireNest_Interior"])
        
        window_objects.append(window_frame)
        
        # Create window cover (partially open)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.05, window_z)
        )
        window_cover = bpy.context.active_object
        window_cover.name = f"WireNest_WindowCover_{i}"
        
        # Edit the window cover
        bm = bmesh.from_edit_mesh(window_cover.data)
        
        # Scale window cover
        for v in bm.verts:
            v.co.x *= 0.7
            v.co.y *= 0.05
            v.co.z *= 0.5
        
        # Update mesh
        bmesh.update_edit_mesh(window_cover.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window cover to match frame
        window_cover.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Rotate cover to be partially open
        window_cover.rotation_euler.x = math.radians(random.uniform(20, 60))
        
        # Create cover material
        cover_material = bpy.data.materials.new(name=f"WireNest_CoverMaterial_{i}")
        cover_material.use_nodes = True
        nodes = cover_material.node_tree.nodes
        links = cover_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.25, 1.0)  # Dark blue-gray
        principled.inputs['Metallic'].default_value = 0.7
        principled.inputs['Roughness'].default_value = 0.6
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        window_cover.data.materials.append(cover_material)
        
        window_objects.append(window_cover)
        
        # Create window glass (dark tinted)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.1, window_z)
        )
        window_glass = bpy.context.active_object
        window_glass.name = f"WireNest_WindowGlass_{i}"
        
        # Edit the window glass
        bm = bmesh.from_edit_mesh(window_glass.data)
        
        # Scale window glass
        for v in bm.verts:
            v.co.x *= 0.6
            v.co.y *= 0.05
            v.co.z *= 0.4
        
        # Update mesh
        bmesh.update_edit_mesh(window_glass.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to match frame
        window_glass.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create dark tinted glass material
        dark_glass = bpy.data.materials.new(name=f"WireNest_DarkGlass_{i}")
        dark_glass.use_nodes = True
        nodes = dark_glass.node_tree.nodes
        links = dark_glass.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.05, 0.05, 0.1, 1.0)  # Very dark blue
        principled.inputs['Metallic'].default_value = 0.1
        principled.inputs['Roughness'].default_value = 0.3
        #principled.inputs['Transmission'].default_value = 0.4  # Semi-transparent
        principled.inputs['IOR'].default_value = 1.45
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign glass material
        window_glass.data.materials.append(dark_glass)
        
        window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

def create_rust_vault_windows(rust_vault_objects, materials, interior_materials):
    """Create windows for Rust Vault (Lower Tier hacker den)"""
    # Extract objects from the rust_vault_objects dictionary
    building = rust_vault_objects.get("building")
    collection = rust_vault_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Rust Vault objects")
        return None
    
    # Create a subcollection for window objects
    if "RustVault_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("RustVault_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["RustVault_Windows"]
    
    window_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create a few small, heavily reinforced windows with bars
    window_count = 4
    for i in range(window_count):
        # Calculate position on the building
        side = i % 4  # 0=front, 1=right, 2=back, 3=left
        
        if side == 0:
            window_x = building_loc[0]
            window_y = building_loc[1] - building_size.y/2
        elif side == 1:
            window_x = building_loc[0] + building_size.x/2
            window_y = building_loc[1]
        elif side == 2:
            window_x = building_loc[0]
            window_y = building_loc[1] + building_size.y/2
        else:  # side == 3
            window_x = building_loc[0] - building_size.x/2
            window_y = building_loc[1]
        
        # Randomize position slightly
        window_x += random.uniform(-1.0, 1.0)
        window_y += random.uniform(-1.0, 1.0)
        
        # Position near the top
        window_z = building_loc[2] + building_size.z/2 - random.uniform(1.0, 2.0)
        
        # Create window frame (reinforced)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"RustVault_WindowFrame_{i}"
        
        # Edit the window frame
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Scale window frame (small)
        for v in bm.verts:
            v.co.x *= 0.8
            v.co.y *= 0.3
            v.co.z *= 0.6
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward
        if side == 0:
            window_frame.rotation_euler.z = math.radians(0)
        elif side == 1:
            window_frame.rotation_euler.z = math.radians(90)
        elif side == 2:
            window_frame.rotation_euler.z = math.radians(180)
        else:  # side == 3
            window_frame.rotation_euler.z = math.radians(270)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create rusty frame material
        rusty_frame = bpy.data.materials.new(name=f"RustVault_WindowFrameMaterial_{i}")
        rusty_frame.use_nodes = True
        nodes = rusty_frame.node_tree.nodes
        links = rusty_frame.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        noise = nodes.new(type='ShaderNodeTexNoise')
        mapping = nodes.new(type='ShaderNodeMapping')
        texcoord = nodes.new(type='ShaderNodeTexCoord')
        colorramp = nodes.new(type='ShaderNodeValToRGB')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.3, 0.2, 0.15, 1.0)  # Rusty brown
        principled.inputs['Metallic'].default_value = 0.7
        principled.inputs['Roughness'].default_value = 0.9
        
        noise.inputs['Scale'].default_value = 15.0
        noise.inputs['Detail'].default_value = 10.0
        noise.inputs['Roughness'].default_value = 0.8
        
        # Setup color ramp for heavy rust effect
        colorramp.color_ramp.elements[0].position = 0.3
        colorramp.color_ramp.elements[0].color = (0.4, 0.15, 0.05, 1.0)  # Heavy rust color
        colorramp.color_ramp.elements[1].position = 0.7
        colorramp.color_ramp.elements[1].color = (0.25, 0.2, 0.15, 1.0)  # Metal color
        
        # Connect nodes
        links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(colorramp.outputs['Color'], principled.inputs['Roughness'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        window_frame.data.materials.append(rusty_frame)
        
        window_objects.append(window_frame)
        
        # Create window bars
        for j in range(4):
            # Horizontal bars
            if j < 2:
                bar_offset = (j - 0.5) * 0.3
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(window_x, window_y, window_z + bar_offset)
                )
                window_bar = bpy.context.active_object
                window_bar.name = f"RustVault_WindowBarH_{i}_{j}"
                
                # Scale bar
                window_bar.scale.x = 0.8
                window_bar.scale.y = 0.05
                window_bar.scale.z = 0.05
            else:  # Vertical bars
                bar_offset = (j - 2.5) * 0.3
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(window_x + bar_offset, window_y, window_z)
                )
                window_bar = bpy.context.active_object
                window_bar.name = f"RustVault_WindowBarV_{i}_{j}"
                
                # Scale bar
                window_bar.scale.x = 0.05
                window_bar.scale.y = 0.05
                window_bar.scale.z = 0.6
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Rotate bar to match window
            window_bar.rotation_euler = window_frame.rotation_euler
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            window_bar.data.materials.append(rusty_frame)
            
            window_objects.append(window_bar)
        
        # Create window glass (dirty)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.1, window_z)
        )
        window_glass = bpy.context.active_object
        window_glass.name = f"RustVault_WindowGlass_{i}"
        
        # Edit the window glass
        bm = bmesh.from_edit_mesh(window_glass.data)
        
        # Scale window glass
        for v in bm.verts:
            v.co.x *= 0.7
            v.co.y *= 0.05
            v.co.z *= 0.5
        
        # Update mesh
        bmesh.update_edit_mesh(window_glass.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to match frame
        window_glass.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create dirty glass material
        dirty_glass = bpy.data.materials.new(name=f"RustVault_DirtyGlass_{i}")
        dirty_glass.use_nodes = True
        nodes = dirty_glass.node_tree.nodes
        links = dirty_glass.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        noise = nodes.new(type='ShaderNodeTexNoise')
        mapping = nodes.new(type='ShaderNodeMapping')
        texcoord = nodes.new(type='ShaderNodeTexCoord')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
        principled.inputs['Metallic'].default_value = 0.0
        principled.inputs['Roughness'].default_value = 0.7
        #principled.inputs['Transmission'].default_value = 0.3  # Slightly transparent
        principled.inputs['IOR'].default_value = 1.45
        
        noise.inputs['Scale'].default_value = 20.0
        noise.inputs['Detail'].default_value = 8.0
        noise.inputs['Roughness'].default_value = 0.5
        
        # Connect nodes
        links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        links.new(noise.outputs['Fac'], principled.inputs['Roughness'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign glass material
        window_glass.data.materials.append(dirty_glass)
        
        window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

def create_militech_windows(militech_objects, materials, interior_materials):
    """Create windows for Militech Armory (Upper Tier)"""
    # Extract objects from the militech_objects dictionary
    building = militech_objects.get("building")
    collection = militech_objects.get("collection")

    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    bm.verts.ensure_lookup_table()

    if not building or not collection:
        print("Error: Missing required Militech Armory objects")
        return None
    
    # Create a subcollection for window objects
    if "Militech_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("Militech_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["Militech_Windows"]
    
    window_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create reinforced windows with red accents
    window_count = 12
    for i in range(window_count):
        # Calculate position on the building
        side = i % 4  # 0=front, 1=right, 2=back, 3=left
        level = i // 4  # 0=bottom, 1=middle, 2=top
        
        if side == 0:
            window_x = building_loc[0]
            window_y = building_loc[1] - building_size.y/2
        elif side == 1:
            window_x = building_loc[0] + building_size.x/2
            window_y = building_loc[1]
        elif side == 2:
            window_x = building_loc[0]
            window_y = building_loc[1] + building_size.y/2
        else:  # side == 3
            window_x = building_loc[0] - building_size.x/2
            window_y = building_loc[1]
        
        # Randomize position slightly
        window_x += random.uniform(-1.0, 1.0)
        window_y += random.uniform(-1.0, 1.0)
        
        # Position based on level
        window_z = building_loc[2] - building_size.z/2 + (level + 0.5) * (building_size.z / 3)
        
        # Create window frame (reinforced)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"Militech_WindowFrame_{i}"
        
        # Edit the window frame
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Scale window frame
        for v in bm.verts:
            v.co.x *= 2.0
            v.co.y *= 0.3
            v.co.z *= 1.5
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward
        if side == 0:
            window_frame.rotation_euler.z = math.radians(0)
        elif side == 1:
            window_frame.rotation_euler.z = math.radians(90)
        elif side == 2:
            window_frame.rotation_euler.z = math.radians(180)
        else:  # side == 3
            window_frame.rotation_euler.z = math.radians(270)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign material
        window_frame.data.materials.append(interior_materials["Militech_Interior"])
        
        window_objects.append(window_frame)
        
        # Create red accent around window
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.05, window_z)
        )
        window_accent = bpy.context.active_object
        window_accent.name = f"Militech_WindowAccent_{i}"
        
        # Edit the window accent
        bm = bmesh.from_edit_mesh(window_accent.data)
        
        # Scale window accent
        for v in bm.verts:
            v.co.x *= 2.1
            v.co.y *= 0.05
            v.co.z *= 1.6
        
        # Make it hollow
        inner_verts = []
        bm.faces.ensure_lookup_table()
        bm.verts.ensure_lookup_table()
        for j in range(8):
            inner_vert = bm.verts.new((
                0.9 * bm.verts[j].co.x,
                1.1 * bm.verts[j].co.y,  # Make it go through
                0.9 * bm.verts[j].co.z
            ))
            inner_verts.append(inner_vert)

        bm.verts.ensure_lookup_table()  # Update after adding new vertices

        # Create faces for inner cutout
        for j in range(4):
            bm.faces.new([
                inner_verts[j],
                inner_verts[(j+1)%4],
                inner_verts[(j+1)%4+4],
                inner_verts[j+4]
            ])

        # Update mesh
        bmesh.update_edit_mesh(window_accent.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window accent to match frame
        window_accent.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign red accent material
        if "Militech_Accent" in materials:
            window_accent.data.materials.append(materials["Militech_Accent"])
        
        window_objects.append(window_accent)
        
        # Create window glass (bulletproof)
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y + 0.1, window_z)
        )
        window_glass = bpy.context.active_object
        window_glass.name = f"Militech_WindowGlass_{i}"
        
        # Edit the window glass
        bm = bmesh.from_edit_mesh(window_glass.data)
        
        # Scale window glass
        for v in bm.verts:
            v.co.x *= 1.8
            v.co.y *= 0.05
            v.co.z *= 1.3
        
        # Update mesh
        bmesh.update_edit_mesh(window_glass.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to match frame
        window_glass.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create bulletproof glass material
        bulletproof_glass = bpy.data.materials.new(name=f"Militech_BulletproofGlass_{i}")
        bulletproof_glass.use_nodes = True
        nodes = bulletproof_glass.node_tree.nodes
        links = bulletproof_glass.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # Light gray
        principled.inputs['Metallic'].default_value = 0.2
        principled.inputs['Roughness'].default_value = 0.1
        #principled.inputs['Transmission'].default_value = 0.7  # Transparent
        principled.inputs['IOR'].default_value = 1.5  # Higher IOR for bulletproof glass
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign glass material
        window_glass.data.materials.append(bulletproof_glass)
        
        window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

def create_biotechnica_windows(biotechnica_objects, materials, interior_materials):
    """Create windows for Biotechnica Spire (Upper Tier)"""
    # Extract objects from the biotechnica_objects dictionary
    building = biotechnica_objects.get("building")
    collection = biotechnica_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Biotechnica Spire objects")
        return None
    
    # Create a subcollection for window objects
    if "Biotechnica_Windows" not in bpy.data.collections:
        windows_collection = bpy.data.collections.new("Biotechnica_Windows")
        collection.children.link(windows_collection)
    else:
        windows_collection = bpy.data.collections["Biotechnica_Windows"]
    
    window_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create organic-looking windows with green-tinted glass
    window_count = 20
    for i in range(window_count):
        # Calculate position in a spiral pattern up the building
        height_fraction = i / window_count
        angle = height_fraction * 6 * math.pi  # 3 full rotations
        
        window_x = building_loc[0] + building_size.x/2 * 0.9 * math.cos(angle)
        window_y = building_loc[1] + building_size.y/2 * 0.9 * math.sin(angle)
        window_z = building_loc[2] - building_size.z/2 + height_fraction * building_size.z * 0.9
        
        # Create window frame with organic shape
        bpy.ops.mesh.primitive_circle_add(
            vertices=16,
            radius=1.0,
            fill_type='NGON',
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z)
        )
        window_frame = bpy.context.active_object
        window_frame.name = f"Biotechnica_WindowFrame_{i}"
        
        # Edit the window frame to make it organic
        bm = bmesh.from_edit_mesh(window_frame.data)
        
        # Make it slightly irregular for organic look
        for v in bm.verts:
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            # Add sine wave variation to radius
            new_radius = radius * (1.0 + 0.2 * math.sin(5 * angle))
            v.co.x = new_radius * math.cos(angle)
            v.co.y = new_radius * math.sin(angle)
        
        # Extrude to create depth
        faces = [f for f in bm.faces]
        result = bmesh.ops.extrude_face_region(bm, geom=faces)
        extruded_verts = [v for v in result['geom'] if isinstance(v, bmesh.types.BMVert)]
        
        # Move extruded vertices
        for v in extruded_verts:
            v.co.z -= 0.1
        
        # Update mesh
        bmesh.update_edit_mesh(window_frame.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window to face outward from building center
        direction = Vector((window_x, window_y, 0)) - Vector((building_loc[0], building_loc[1], 0))
        rot_quat = direction.to_track_quat('Z', 'Y')
        window_frame.rotation_euler = rot_quat.to_euler()
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Scale window frame
        window_frame.scale.x = random.uniform(0.8, 1.2)
        window_frame.scale.y = random.uniform(0.8, 1.2)
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        window_frame.data.materials.append(interior_materials["Biotechnica_Interior"])
        
        window_objects.append(window_frame)
        
        # Create window glass with green tint
        bpy.ops.mesh.primitive_circle_add(
            vertices=16,
            radius=0.9,
            fill_type='NGON',
            enter_editmode=True,
            align='WORLD',
            location=(window_x, window_y, window_z - 0.05)
        )
        window_glass = bpy.context.active_object
        window_glass.name = f"Biotechnica_WindowGlass_{i}"
        
        # Edit the window glass to match frame's organic shape
        bm = bmesh.from_edit_mesh(window_glass.data)
        
        # Make it slightly irregular for organic look (same pattern as frame)
        for v in bm.verts:
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            # Add sine wave variation to radius
            new_radius = radius * (1.0 + 0.2 * math.sin(5 * angle))
            v.co.x = new_radius * math.cos(angle)
            v.co.y = new_radius * math.sin(angle)
        
        # Update mesh
        bmesh.update_edit_mesh(window_glass.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate window glass to match frame
        window_glass.rotation_euler = window_frame.rotation_euler
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Scale window glass to match frame
        window_glass.scale.x = window_frame.scale.x * 0.9
        window_glass.scale.y = window_frame.scale.y * 0.9
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create green-tinted glass material
        green_glass = bpy.data.materials.new(name=f"Biotechnica_GreenGlass_{i}")
        green_glass.use_nodes = True
        nodes = green_glass.node_tree.nodes
        links = green_glass.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.2, 1.0)  # Green-tinted
        principled.inputs['Metallic'].default_value = 0.3
        principled.inputs['Roughness'].default_value = 0.1
        #principled.inputs['Transmission'].default_value = 0.8  # Mostly transparent
        principled.inputs['IOR'].default_value = 1.45
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign glass material
        window_glass.data.materials.append(green_glass)
        
        window_objects.append(window_glass)
    
    # Move all objects to the windows collection
    for obj in window_objects:
        if obj.name not in windows_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(windows_collection.name))
    
    return windows_collection

# Main function to implement windows for all buildings
def implement_building_windows(building_objects, materials, interior_materials):
    """Implement windows for all buildings"""
    # Implement windows for each building
    windows = {}
    
    # NeoTech Labs Tower
    if "neotech_tower" in building_objects:
        windows["NeoTech_Windows"] = create_neotech_windows(
            building_objects["neotech_tower"],
            materials,
            interior_materials
        )
    
    # Specter Station
    if "specter_station" in building_objects:
        windows["Specter_Windows"] = create_specter_windows(
            building_objects["specter_station"],
            materials,
            interior_materials
        )
    
    # Black Nexus
    if "black_nexus" in building_objects:
        windows["BlackNexus_Windows"] = create_black_nexus_windows(
            building_objects["black_nexus"],
            materials,
            interior_materials
        )
    
    # Wire Nest
    if "wire_nest" in building_objects:
        windows["WireNest_Windows"] = create_wire_nest_windows(
            building_objects["wire_nest"],
            materials,
            interior_materials
        )
    
    # Rust Vault
    if "rust_vault" in building_objects:
        windows["RustVault_Windows"] = create_rust_vault_windows(
            building_objects["rust_vault"],
            materials,
            interior_materials
        )
    
    # Militech Armory
    if "militech_armory" in building_objects:
        windows["Militech_Windows"] = create_militech_windows(
            building_objects["militech_armory"],
            materials,
            interior_materials
        )
    
    # Biotechnica Spire
    if "biotechnica_spire" in building_objects:
        windows["Biotechnica_Windows"] = create_biotechnica_windows(
            building_objects["biotechnica_spire"],
            materials,
            interior_materials
        )
    
    # Move all objects to the windows collection
    for building_name, window_collection in windows.items():
        if window_collection:
            for obj in window_collection.objects:
                # Determine the correct rooms collection name based on the building name
                rooms_collection_name = building_name.replace("Windows", "Rooms")
                # Find the rooms collection
                rooms_collection = bpy.data.collections.get(rooms_collection_name)
                if rooms_collection:
                    # Move the object to the rooms collection
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
                    print(f"Info: {obj.name} moved to {rooms_collection.name}")
                else:
                    print(f"Warning: Rooms collection '{rooms_collection_name}' not found for {building_name}.")
    
    return windows
