"""
Neon Crucible - Building Rooms Implementation
Blender 4.2 Python Script for generating rooms per floor for buildings in the Neon Crucible cyberpunk world.
This script implements interior rooms for all buildings based on their function and tier level.
"""

import bpy
import bmesh
import random
import math
from mathutils import Vector

def create_neotech_rooms(neotech_objects, materials, interior_materials):
    """Create rooms per floor for NeoTech Labs Tower (Upper Tier)"""
    # Extract objects from the neotech_objects dictionary
    tower = neotech_objects.get("tower")
    collection = neotech_objects.get("collection")
    
    if not tower or not collection:
        print("Error: Missing required NeoTech Tower objects")
        return None
    
    # Create a subcollection for room objects
    if "NeoTech_Rooms" not in bpy.data.collections:
        rooms_collection = bpy.data.collections.new("NeoTech_Rooms")
        collection.children.link(rooms_collection)
    else:
        rooms_collection = bpy.data.collections["NeoTech_Rooms"]
    
    room_objects = []
    
    # Get tower location and dimensions
    tower_loc = tower.location
    tower_radius = tower.dimensions.x / 2
    tower_height = tower.dimensions.z
    
    # Define floor heights
    floor_heights = [
        0,                      # Ground/Lobby level
        tower_height * 0.2,     # Research labs
        tower_height * 0.4,     # Server room
        tower_height * 0.6,     # Meeting rooms
        tower_height * 0.8      # Executive office
    ]
    
    # Create floors and rooms for each level
    for floor_idx, floor_height in enumerate(floor_heights):
        floor_z = tower_loc[2] - tower_height/2 + floor_height
        floor_name = ["Lobby", "Research", "Server", "Meeting", "Executive"][floor_idx]
        
        # Create floor
        floor_radius = tower_radius * (1.0 - floor_idx * 0.1)  # Taper as we go up
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=floor_radius,
            depth=0.2,
            enter_editmode=False,
            align='WORLD',
            location=(tower_loc[0], tower_loc[1], floor_z)
        )
        floor = bpy.context.active_object
        floor.name = f"NeoTech_{floor_name}_Floor"
        
        # Assign material
        floor.data.materials.append(interior_materials["NeoTech_Floor"])
        
        room_objects.append(floor)
        
        # Create ceiling (except for top floor which uses tower top)
        if floor_idx < len(floor_heights) - 1:
            ceiling_z = tower_loc[2] - tower_height/2 + floor_heights[floor_idx + 1] - 0.1
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=floor_radius,
                depth=0.2,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], ceiling_z)
            )
            ceiling = bpy.context.active_object
            ceiling.name = f"NeoTech_{floor_name}_Ceiling"
            
            # Assign material
            ceiling.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(ceiling)
        
        # Create rooms based on floor type
        if floor_name == "Lobby":
            # Create reception desk
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1] + floor_radius * 0.3, floor_z + 0.5)
            )
            desk = bpy.context.active_object
            desk.name = "NeoTech_Reception_Desk"
            
            # Scale desk
            desk.scale.x = floor_radius * 0.6
            desk.scale.y = floor_radius * 0.2
            desk.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            desk.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(desk)
            
            # Create holographic receptionist
            bpy.ops.mesh.primitive_plane_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1] + floor_radius * 0.3, floor_z + 1.5)
            )
            hologram = bpy.context.active_object
            hologram.name = "NeoTech_Receptionist_Hologram"
            
            # Scale hologram
            hologram.scale.x = 1.0
            hologram.scale.y = 2.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            hologram.data.materials.append(interior_materials["Hologram"])
            
            room_objects.append(hologram)
            
            # Create security barriers
            for i in range(2):
                barrier_x = tower_loc[0] + (i * 2 - 1) * floor_radius * 0.3
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(barrier_x, tower_loc[1], floor_z + 0.5)
                )
                barrier = bpy.context.active_object
                barrier.name = f"NeoTech_Security_Barrier_{i}"
            
            # Scale barrier
            barrier.scale.x = 0.1
            barrier.scale.y = floor_radius * 0.6
            barrier.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            barrier.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(barrier)
            
            # Create security scanner
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=floor_radius * 0.15,
                depth=0.1,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.05)
            )
            scanner = bpy.context.active_object
            scanner.name = "NeoTech_Security_Scanner"
            
            # Assign material
            scanner_material = bpy.data.materials.new(name="NeoTech_Scanner_Material")
            scanner_material.use_nodes = True
            nodes = scanner_material.node_tree.nodes
            links = scanner_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            emission = nodes.new(type='ShaderNodeEmission')
            
            # Set properties
            emission.inputs['Color'].default_value = (0.0, 0.8, 1.0, 1.0)  # Cyan
            emission.inputs['Strength'].default_value = 1.0
            
            # Connect nodes
            links.new(emission.outputs['Emission'], output.inputs['Surface'])
            
            # Assign material
            scanner.data.materials.append(scanner_material)
            
            room_objects.append(scanner)
            
        elif floor_name == "Research":
            # Create research lab equipment
            
            # Create central lab table
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.5)
            )
            lab_table = bpy.context.active_object
            lab_table.name = "NeoTech_Lab_Table"
            
            # Scale lab table
            lab_table.scale.x = floor_radius * 0.6
            lab_table.scale.y = floor_radius * 0.4
            lab_table.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            lab_table.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(lab_table)
            
            # Create lab equipment
            for i in range(4):
                angle = i * (2 * math.pi / 4)
                equip_x = tower_loc[0] + floor_radius * 0.3 * math.cos(angle)
                equip_y = tower_loc[1] + floor_radius * 0.3 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(equip_x, equip_y, floor_z + 1.0)
                )
                equipment = bpy.context.active_object
                equipment.name = f"NeoTech_Lab_Equipment_{i}"
                
                # Scale equipment
                equipment.scale.x = 0.5
                equipment.scale.y = 0.5
                equipment.scale.z = 0.5
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                equip_material = bpy.data.materials.new(name=f"NeoTech_Equipment_Material_{i}")
                equip_material.use_nodes = True
                nodes = equip_material.node_tree.nodes
                links = equip_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.15, 1.0)  # Dark blue-gray
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.2
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                equipment.data.materials.append(equip_material)
                
                room_objects.append(equipment)
                
                # Create holographic display above equipment
                bpy.ops.mesh.primitive_plane_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(equip_x, equip_y, floor_z + 1.5)
                )
                holo_display = bpy.context.active_object
                holo_display.name = f"NeoTech_Lab_Display_{i}"
                
                # Scale display
                holo_display.scale.x = 0.4
                holo_display.scale.y = 0.4
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                holo_display.data.materials.append(interior_materials["Hologram"])
                
                room_objects.append(holo_display)
            
        elif floor_name == "Server":
            # Create server racks in circular pattern
            rack_count = 8
            for i in range(rack_count):
                angle = i * (2 * math.pi / rack_count)
                rack_x = tower_loc[0] + floor_radius * 0.7 * math.cos(angle)
                rack_y = tower_loc[1] + floor_radius * 0.7 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(rack_x, rack_y, floor_z + 1.0)
                )
                rack = bpy.context.active_object
                rack.name = f"NeoTech_Server_Rack_{i}"
                
                # Scale rack
                rack.scale.x = 0.5
                rack.scale.y = 0.5
                rack.scale.z = 2.0
                
                # Rotate to face center
                direction = Vector((tower_loc[0], tower_loc[1], 0)) - Vector((rack_x, rack_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                rack.rotation_euler = rot_quat.to_euler()
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                rack.data.materials.append(interior_materials["NeoTech_Interior"])
                
                room_objects.append(rack)
                
                # Create server lights
                for j in range(5):
                    light_z = floor_z + 0.5 + j * 0.3
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(rack_x, rack_y - 0.26, light_z)
                    )
                    light = bpy.context.active_object
                    light.name = f"NeoTech_Server_Light_{i}_{j}"
                    
                    # Scale light
                    light.scale.x = 0.1
                    light.scale.y = 0.02
                    light.scale.z = 0.02
                    
                    # Rotate to match rack
                    light.rotation_euler = rack.rotation_euler
                    
                    # Apply transformations
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                    
                    # Create light material with random color
                    light_material = bpy.data.materials.new(name=f"NeoTech_ServerLight_Material_{i}_{j}")
                    light_material.use_nodes = True
                    nodes = light_material.node_tree.nodes
                    links = light_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    emission = nodes.new(type='ShaderNodeEmission')
                    
                    # Set properties with random color
                    r = random.choice([0.0, 0.0, 1.0, 0.0])
                    g = random.choice([0.0, 1.0, 0.0, 0.0])
                    b = random.choice([1.0, 0.0, 0.0, 1.0])
                    emission.inputs['Color'].default_value = (r, g, b, 1.0)
                    emission.inputs['Strength'].default_value = 3.0
                    
                    # Connect nodes
                    links.new(emission.outputs['Emission'], output.inputs['Surface'])
                    
                    # Assign material
                    light.data.materials.append(light_material)
                    
                    room_objects.append(light)
            
            # Create central data visualization
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=32,
                radius=floor_radius * 0.3,
                depth=3.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 1.5)
            )
            data_vis = bpy.context.active_object
            data_vis.name = "NeoTech_Data_Visualization"
            
            # Assign hologram material
            data_vis.data.materials.append(interior_materials["Hologram"])
            
            room_objects.append(data_vis)
            
        elif floor_name == "Meeting":
            # Create meeting room with conference table
            
            # Create conference table
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=32,
                radius=floor_radius * 0.4,
                depth=0.1,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.5)
            )
            table = bpy.context.active_object
            table.name = "NeoTech_Conference_Table"
            
            # Assign material
            table.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(table)
            
            # Create chairs around table
            chair_count = 8
            for i in range(chair_count):
                angle = i * (2 * math.pi / chair_count)
                chair_x = tower_loc[0] + floor_radius * 0.5 * math.cos(angle)
                chair_y = tower_loc[1] + floor_radius * 0.5 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(chair_x, chair_y, floor_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"NeoTech_Chair_{i}"
                
                # Scale chair
                chair.scale.x = 0.3
                chair.scale.y = 0.3
                chair.scale.z = 0.3
                
                # Rotate to face table
                direction = Vector((tower_loc[0], tower_loc[1], 0)) - Vector((chair_x, chair_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                chair.rotation_euler = rot_quat.to_euler()
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                chair.data.materials.append(interior_materials["NeoTech_Interior"])
                
                room_objects.append(chair)
            
            # Create holographic presentation
            bpy.ops.mesh.primitive_plane_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 1.5)
            )
            presentation = bpy.context.active_object
            presentation.name = "NeoTech_Presentation"
            
            # Scale presentation
            presentation.scale.x = floor_radius * 0.6
            presentation.scale.y = floor_radius * 0.4
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            presentation.data.materials.append(interior_materials["Hologram"])
            
            room_objects.append(presentation)
            
        elif floor_name == "Executive":
            # Create executive office with desk and panoramic views
            
            # Create executive desk
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1] + floor_radius * 0.3, floor_z + 0.5)
            )
            desk = bpy.context.active_object
            desk.name = "NeoTech_Executive_Desk"
            
            # Scale desk
            desk.scale.x = floor_radius * 0.5
            desk.scale.y = floor_radius * 0.2
            desk.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            desk.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(desk)
            
            # Create executive chair
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1] + floor_radius * 0.5, floor_z + 0.3)
            )
            chair = bpy.context.active_object
            chair.name = "NeoTech_Executive_Chair"
            
            # Scale chair
            chair.scale.x = 0.6
            chair.scale.y = 0.6
            chair.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            chair.data.materials.append(interior_materials["NeoTech_Interior"])
            
            room_objects.append(chair)
            
            # Create holographic displays
            for i in range(3):
                offset_x = (i - 1) * floor_radius * 0.3
                
                bpy.ops.mesh.primitive_plane_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(tower_loc[0] + offset_x, tower_loc[1] + floor_radius * 0.3, floor_z + 1.0)
                )
                display = bpy.context.active_object
                display.name = f"NeoTech_Executive_Display_{i}"
                
                # Scale display
                display.scale.x = 0.4
                display.scale.y = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                display.data.materials.append(interior_materials["Hologram"])
                
                room_objects.append(display)
            
            # Create visitor chairs
            for i in range(2):
                offset_x = (i * 2 - 1) * floor_radius * 0.2
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(tower_loc[0] + offset_x, tower_loc[1], floor_z + 0.3)
                )
                visitor_chair = bpy.context.active_object
                visitor_chair.name = f"NeoTech_Visitor_Chair_{i}"
                
                # Scale chair
                visitor_chair.scale.x = 0.3
                visitor_chair.scale.y = 0.3
                visitor_chair.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                visitor_chair.data.materials.append(interior_materials["NeoTech_Interior"])
                
                room_objects.append(visitor_chair)
    
    # Move all objects to the rooms collection
    for obj in room_objects:
        if obj.name not in rooms_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
    
    return rooms_collection

def create_specter_rooms(specter_objects, materials, interior_materials):
    """Create rooms per floor for Specter Station (Mid Tier)"""
    # Extract objects from the specter_objects dictionary
    tower = specter_objects.get("tower")
    collection = specter_objects.get("collection")
    
    if not tower or not collection:
        print("Error: Missing required Specter Station objects")
        return None
    
    # Create a subcollection for room objects
    if "Specter_Rooms" not in bpy.data.collections:
        rooms_collection = bpy.data.collections.new("Specter_Rooms")
        collection.children.link(rooms_collection)
    else:
        rooms_collection = bpy.data.collections["Specter_Rooms"]
    
    room_objects = []
    
    # Get tower location and dimensions
    tower_loc = tower.location
    tower_radius = tower.dimensions.x / 2
    tower_height = tower.dimensions.z
    
    # Define floor heights
    floor_heights = [
        0,                      # Ground/Market level
        tower_height * 0.3,     # Living quarters
        tower_height * 0.6      # Command center
    ]
    
    # Create floors and rooms for each level
    for floor_idx, floor_height in enumerate(floor_heights):
        floor_z = tower_loc[2] - tower_height/2 + floor_height
        floor_name = ["Market", "Living", "Command"][floor_idx]
        
        # Create floor
        floor_radius = tower_radius * 1.5  # Wider than tower
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=floor_radius,
            depth=0.2,
            enter_editmode=True,
            align='WORLD',
            location=(tower_loc[0], tower_loc[1], floor_z)
        )
        floor = bpy.context.active_object
        floor.name = f"Specter_{floor_name}_Floor"
        
        # Edit the floor to make it look damaged/worn
        bm = bmesh.from_edit_mesh(floor.data)
        
        # Distort vertices slightly for worn look
        for v in bm.verts:
            if random.random() > 0.7:
                v.co.z += random.uniform(-0.05, 0.05)
        
        # Update mesh
        bmesh.update_edit_mesh(floor.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        floor.data.materials.append(interior_materials["Specter_Interior"])
        
        room_objects.append(floor)
        
        # Create ceiling (except for top floor which uses tower top)
        if floor_idx < len(floor_heights) - 1:
            ceiling_z = tower_loc[2] - tower_height/2 + floor_heights[floor_idx + 1] - 0.1
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=floor_radius,
                depth=0.2,
                enter_editmode=True,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], ceiling_z)
            )
            ceiling = bpy.context.active_object
            ceiling.name = f"Specter_{floor_name}_Ceiling"
            
            # Edit the ceiling to make it look damaged/worn
            bm = bmesh.from_edit_mesh(ceiling.data)
            
            # Distort vertices slightly for worn look
            for v in bm.verts:
                if random.random() > 0.7:
                    v.co.z += random.uniform(-0.05, 0.05)
            
            # Update mesh
            bmesh.update_edit_mesh(ceiling.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Assign material
            ceiling.data.materials.append(interior_materials["Specter_Interior"])
            
            room_objects.append(ceiling)
        
        # Create rooms based on floor type
        if floor_name == "Market":
            # Create market stalls in circular pattern
            stall_count = 8
            for i in range(stall_count):
                angle = i * (2 * math.pi / stall_count)
                stall_x = tower_loc[0] + (tower_radius * 1.5) * math.cos(angle)
                stall_y = tower_loc[1] + (tower_radius * 1.5) * math.sin(angle)
                
                # Create stall base
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(stall_x, stall_y, floor_z + 0.5)
                )
                stall = bpy.context.active_object
                stall.name = f"Specter_MarketStall_{i}"
                
                # Scale stall
                stall.scale.x = 2.0
                stall.scale.y = 1.5
                stall.scale.z = 1.0
                
                # Rotate to face center
                direction = Vector((tower_loc[0], tower_loc[1], 0)) - Vector((stall_x, stall_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                stall.rotation_euler = rot_quat.to_euler()
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                stall.data.materials.append(interior_materials["Specter_Interior"])
                
                # Create stall canopy
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(stall_x, stall_y, floor_z + 1.5)
                )
                canopy = bpy.context.active_object
                canopy.name = f"Specter_StallCanopy_{i}"
                
                # Edit the canopy
                bm = bmesh.from_edit_mesh(canopy.data)
                
                # Scale canopy
                for v in bm.verts:
                    v.co.x *= 2.2
                    v.co.y *= 1.7
                    v.co.z *= 0.1
                
                # Rotate to face center
                direction = Vector((tower_loc[0], tower_loc[1], 0)) - Vector((stall_x, stall_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                canopy.rotation_euler = rot_quat.to_euler()
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material with random color
                canopy_material = bpy.data.materials.new(name=f"StallCanopy_{i}")
                canopy_material.use_nodes = True
                nodes = canopy_material.node_tree.nodes
                links = canopy_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set random color
                r = random.uniform(0.5, 1.0)
                g = random.uniform(0.5, 1.0)
                b = random.uniform(0.5, 1.0)
                emission.inputs['Color'].default_value = (r, g, b, 1.0)
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                canopy.data.materials.append(canopy_material)
                
                room_objects.append(stall)
                room_objects.append(canopy)
            
        elif floor_name == "Living":
            # Create maintenance tunnels/living quarters
            tunnel_count = 4
            for i in range(tunnel_count):
                angle = i * (2 * math.pi / tunnel_count) + math.pi/tunnel_count
                tunnel_x = tower_loc[0] + (tower_radius * 1.8) * math.cos(angle)
                tunnel_y = tower_loc[1] + (tower_radius * 1.8) * math.sin(angle)
                
                # Calculate tunnel direction
                direction = Vector((tunnel_x, tunnel_y, 0)) - Vector((tower_loc[0], tower_loc[1], 0))
                direction.normalize()
                
                # Create tunnel entrance
                bpy.ops.mesh
                principled.inputs['Roughness'].default_value = 0.8
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                canopy.data.materials.append(canopy_material)
                
                room_objects.append(canopy)
                
                # Create merchandise on stall
                for j in range(3):
                    merch_x = stall_x - 0.5 + j * 0.5
                    merch_y = stall_y - 0.3
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(merch_x, merch_y, floor_z + 1.0)
                    )
                    merchandise = bpy.context.active_object
                    merchandise.name = f"Specter_Merchandise_{i}_{j}"
                    
                    # Scale merchandise
                    merchandise.scale.x = 0.2
                    merchandise.scale.y = 0.2
                    merchandise.scale.z = 0.2
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create merchandise material with random color
                    merch_material = bpy.data.materials.new(name=f"Specter_MerchMaterial_{i}_{j}")
                    merch_material.use_nodes = True
                    nodes = merch_material.node_tree.nodes
                    links = merch_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set random color
                    r = random.uniform(0.2, 0.8)
                    g = random.uniform(0.2, 0.8)
                    b = random.uniform(0.2, 0.8)
                    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                    principled.inputs['Roughness'].default_value = 0.5
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    merchandise.data.materials.append(merch_material)
                    
                    room_objects.append(merchandise)
            
            # Create central gathering area
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=floor_radius * 0.2,
                depth=0.1,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.05)
            )
            gathering = bpy.context.active_object
            gathering.name = "Specter_Gathering_Area"
            
            # Assign material
            gathering.data.materials.append(interior_materials["Specter_Interior"])
            
            room_objects.append(gathering)
            
            # Create makeshift seating around gathering area
            seat_count = 6
            for i in range(seat_count):
                angle = i * (2 * math.pi / seat_count)
                seat_x = tower_loc[0] + floor_radius * 0.3 * math.cos(angle)
                seat_y = tower_loc[1] + floor_radius * 0.3 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(seat_x, seat_y, floor_z + 0.2)
                )
                seat = bpy.context.active_object
                seat.name = f"Specter_Makeshift_Seat_{i}"
                
                # Edit the seat to make it look makeshift
                bm = bmesh.from_edit_mesh(seat.data)
                
                # Scale seat
                for v in bm.verts:
                    v.co.x *= 0.4
                    v.co.y *= 0.4
                    v.co.z *= 0.4
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.5:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(seat.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Assign material
                seat.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(seat)
            
        elif floor_name == "Living":
            # Create living quarters in the maintenance tunnels
            
            # Create central corridor
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=floor_radius * 0.3,
                depth=0.1,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.05)
            )
            corridor = bpy.context.active_object
            corridor.name = "Specter_Living_Corridor"
            
            # Assign material
            corridor.data.materials.append(interior_materials["Specter_Interior"])
            
            room_objects.append(corridor)
            
            # Create living quarters around the perimeter
            quarter_count = 6
            for i in range(quarter_count):
                angle = i * (2 * math.pi / quarter_count)
                quarter_x = tower_loc[0] + floor_radius * 0.7 * math.cos(angle)
                quarter_y = tower_loc[1] + floor_radius * 0.7 * math.sin(angle)
                
                # Create living quarter room
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(quarter_x, quarter_y, floor_z + 1.0)
                )
                quarter = bpy.context.active_object
                quarter.name = f"Specter_Living_Quarter_{i}"
                
                # Edit the quarter to make it look makeshift
                bm = bmesh.from_edit_mesh(quarter.data)
                
                # Scale quarter
                for v in bm.verts:
                    v.co.x *= 2.0
                    v.co.y *= 2.0
                    v.co.z *= 2.0
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.1, 0.1)
                        v.co.y += random.uniform(-0.1, 0.1)
                        v.co.z += random.uniform(-0.1, 0.1)
                
                # Update mesh
                bmesh.update_edit_mesh(quarter.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Assign material
                quarter.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(quarter)
                
                # Create bed
                bed_x = quarter_x - 0.5
                bed_y = quarter_y - 0.5
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(bed_x, bed_y, floor_z + 0.3)
                )
                bed = bpy.context.active_object
                bed.name = f"Specter_Bed_{i}"
                
                # Scale bed
                bed.scale.x = 0.8
                bed.scale.y = 1.8
                bed.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create bed material
                bed_material = bpy.data.materials.new(name=f"Specter_BedMaterial_{i}")
                bed_material.use_nodes = True
                nodes = bed_material.node_tree.nodes
                links = bed_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.4, 1.0)  # Dark blue-gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                bed.data.materials.append(bed_material)
                
                room_objects.append(bed)
                
                # Create small table
                table_x = quarter_x + 0.5
                table_y = quarter_y - 0.5
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(table_x, table_y, floor_z + 0.5)
                )
                table = bpy.context.active_object
                table.name = f"Specter_Table_{i}"
                
                # Scale table
                table.scale.x = 0.5
                table.scale.y = 0.5
                table.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                table.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(table)
                
                # Create personal items on table
                for j in range(2):
                    item_x = table_x - 0.1 + j * 0.2
                    item_y = table_y - 0.1 + j * 0.2
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(item_x, item_y, floor_z + 1.0)
                    )
                    item = bpy.context.active_object
                    item.name = f"Specter_PersonalItem_{i}_{j}"
                    
                    # Scale item
                    item.scale.x = 0.1
                    item.scale.y = 0.1
                    item.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create item material with random color
                    item_material = bpy.data.materials.new(name=f"Specter_ItemMaterial_{i}_{j}")
                    item_material.use_nodes = True
                    nodes = item_material.node_tree.nodes
                    links = item_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set random color
                    r = random.uniform(0.2, 0.8)
                    g = random.uniform(0.2, 0.8)
                    b = random.uniform(0.2, 0.8)
                    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                    principled.inputs['Roughness'].default_value = 0.5
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    item.data.materials.append(item_material)
                    
                    room_objects.append(item)
            
            # Create connecting tunnels to living quarters
            for i in range(quarter_count):
                angle = i * (2 * math.pi / quarter_count)
                quarter_x = tower_loc[0] + floor_radius * 0.7 * math.cos(angle)
                quarter_y = tower_loc[1] + floor_radius * 0.7 * math.sin(angle)
                
                # Calculate direction from center to quarter
                direction = Vector((quarter_x, quarter_y, 0)) - Vector((tower_loc[0], tower_loc[1], 0))
                direction.normalize()
                
                # Create tunnel
                tunnel_length = floor_radius * 0.4
                tunnel_start_x = tower_loc[0] + direction.x * floor_radius * 0.3
                tunnel_start_y = tower_loc[1] + direction.y * floor_radius * 0.3
                tunnel_end_x = tower_loc[0] + direction.x * floor_radius * 0.7
                tunnel_end_y = tower_loc[1] + direction.y * floor_radius * 0.7
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=((tunnel_start_x + tunnel_end_x) / 2, (tunnel_start_y + tunnel_end_y) / 2, floor_z + 1.0)
                )
                tunnel = bpy.context.active_object
                tunnel.name = f"Specter_Tunnel_{i}"
                
                # Edit the tunnel
                bm = bmesh.from_edit_mesh(tunnel.data)
                
                # Scale tunnel
                for v in bm.verts:
                    v.co.x *= tunnel_length
                    v.co.y *= 1.0
                    v.co.z *= 2.0
                
                # Update mesh
                bmesh.update_edit_mesh(tunnel.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate tunnel to point from center to quarter
                tunnel.rotation_euler.z = math.atan2(direction.y, direction.x)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                tunnel.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(tunnel)
            
        elif floor_name == "Command":
            # Create command center in former station control room
            
            # Create central command table
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=floor_radius * 0.3,
                depth=0.2,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.5)
            )
            command_table = bpy.context.active_object
            command_table.name = "Specter_Command_Table"
            
            # Assign material
            command_table.data.materials.append(interior_materials["Specter_Interior"])
            
            room_objects.append(command_table)
            
            # Create holographic display on table
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=32,
                radius=floor_radius * 0.25,
                depth=0.1,
                enter_editmode=False,
                align='WORLD',
                location=(tower_loc[0], tower_loc[1], floor_z + 0.6)
            )
            holo_display = bpy.context.active_object
            holo_display.name = "Specter_Command_Display"
            
            # Assign hologram material
            holo_display.data.materials.append(interior_materials["Hologram"])
            
            room_objects.append(holo_display)
            
            # Create chairs around command table
            chair_count = 6
            for i in range(chair_count):
                angle = i * (2 * math.pi / chair_count)
                chair_x = tower_loc[0] + floor_radius * 0.4 * math.cos(angle)
                chair_y = tower_loc[1] + floor_radius * 0.4 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(chair_x, chair_y, floor_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"Specter_Command_Chair_{i}"
                
                # Edit the chair to make it look makeshift
                bm = bmesh.from_edit_mesh(chair.data)
                
                # Scale chair
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.3
                    v.co.z *= 0.3
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(chair.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate to face table
                direction = Vector((tower_loc[0], tower_loc[1], 0)) - Vector((chair_x, chair_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                chair.rotation_euler = rot_quat.to_euler()
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                chair.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(chair)
            
            # Create control stations around the perimeter
            station_count = 8
            for i in range(station_count):
                angle = i * (2 * math.pi / station_count)
                station_x = tower_loc[0] + floor_radius * 0.7 * math.cos(angle)
                station_y = tower_loc[1] + floor_radius * 0.7 * math.sin(angle)
                
                # Create station desk
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(station_x, station_y, floor_z + 0.5)
                )
                station = bpy.context.active_object
                station.name = f"Specter_Control_Station_{i}"
                
                # Scale station
                station.scale.x = 1.0
                station.scale.y = 0.5
                station.scale.z = 1.0
                
                # Rotate to face center
                direction = Vector((tower_loc[0], tower_loc[1], 0)) - Vector((station_x, station_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                station.rotation_euler = rot_quat.to_euler()
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                station.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(station)
                
                # Create station chair
                chair_x = station_x + direction.x * 0.7
                chair_y = station_y + direction.y * 0.7
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(chair_x, chair_y, floor_z + 0.3)
                )
                station_chair = bpy.context.active_object
                station_chair.name = f"Specter_Station_Chair_{i}"
                
                # Edit the chair to make it look makeshift
                bm = bmesh.from_edit_mesh(station_chair.data)
                
                # Scale chair
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.3
                    v.co.z *= 0.3
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(station_chair.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate to face station
                station_chair.rotation_euler = station.rotation_euler
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                station_chair.data.materials.append(interior_materials["Specter_Interior"])
                
                room_objects.append(station_chair)
                
                # Create monitors on station
                for j in range(2):
                    monitor_x = station_x - direction.x * 0.25
                    monitor_y = station_y - direction.y * 0.25
                    monitor_z = floor_z + 1.0 + j * 0.3
                    
                    bpy.ops.mesh.primitive_plane_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(monitor_x, monitor_y, monitor_z)
                    )
                    monitor = bpy.context.active_object
                    monitor.name = f"Specter_Monitor_{i}_{j}"
                    
                    # Scale monitor
                    monitor.scale.x = 0.4
                    monitor.scale.y = 0.3
                    
                    # Rotate to face chair
                    monitor.rotation_euler = station.rotation_euler
                    
                    # Apply transformations
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                    
                    # Create monitor material
                    monitor_material = bpy.data.materials.new(name=f"Specter_MonitorMaterial_{i}_{j}")
                    monitor_material.use_nodes = True
                    nodes = monitor_material.node_tree.nodes
                    links = monitor_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    emission = nodes.new(type='ShaderNodeEmission')
                    
                    # Set properties with random color
                    r = random.uniform(0.0, 0.5)
                    g = random.uniform(0.2, 0.8)
                    b = random.uniform(0.2, 0.8)
                    emission.inputs['Color'].default_value = (r, g, b, 1.0)
                    emission.inputs['Strength'].default_value = 1.0
                    
                    # Connect nodes
                    links.new(emission.outputs['Emission'], output.inputs['Surface'])
                    
                    # Assign material
                    monitor.data.materials.append(monitor_material)
                    
                    room_objects.append(monitor)
            
            # Create hidden storage area
            storage_x = tower_loc[0] + floor_radius * 0.6
            storage_y = tower_loc[1] - floor_radius * 0.6
            
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(storage_x, storage_y, floor_z + 1.0)
            )
            storage = bpy.context.active_object
            storage.name = "Specter_Hidden_Storage"
            
            # Scale storage
            storage.scale.x = 1.5
            storage.scale.y = 1.5
            storage.scale.z = 2.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            storage.data.materials.append(interior_materials["Specter_Interior"])
            
            room_objects.append(storage)
            
            # Create false wall hiding storage
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(storage_x - 1.5, storage_y, floor_z + 1.0)
            )
            false_wall = bpy.context.active_object
            false_wall.name = "Specter_False_Wall"
            
            # Scale false wall
            false_wall.scale.x = 0.1
            false_wall.scale.y = 1.5
            false_wall.scale.z = 2.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            false_wall.data.materials.append(interior_materials["Specter_Interior"])
            
            room_objects.append(false_wall)
    
    # Move all objects to the rooms collection
    for obj in room_objects:
        if obj.name not in rooms_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
    
    return rooms_collection


def create_black_nexus_rooms(black_nexus_objects, materials, interior_materials):
    """Create rooms for Black Nexus (Lower Tier rebel hideout)
	Neon Crucible - Black Nexus Rooms Implementation
	Blender 4.2 Python Script for generating rooms per floor for the Black Nexus building
	in the Neon Crucible cyberpunk world.
	"""
    # Extract objects from the black_nexus_objects dictionary
    building = black_nexus_objects.get("building")
    collection = black_nexus_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Black Nexus objects")
        return None
    
    # Create a subcollection for room objects
    if "BlackNexus_Rooms" not in bpy.data.collections:
        rooms_collection = bpy.data.collections.new("BlackNexus_Rooms")
        collection.children.link(rooms_collection)
    else:
        rooms_collection = bpy.data.collections["BlackNexus_Rooms"]
    
    room_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Define room positions relative to building center
    rooms_data = [
        {
            "name": "Main_Hub",
            "position": (0, 0, 0),
            "size": (building_size.x * 0.6, building_size.y * 0.6, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Communication_Center",
            "position": (building_size.x * 0.25, building_size.y * 0.25, 0),
            "size": (building_size.x * 0.3, building_size.y * 0.3, building_size.z * 0.2),
            "floor_level": 1
        },
        {
            "name": "Sleeping_Quarters",
            "position": (-building_size.x * 0.25, building_size.y * 0.25, 0),
            "size": (building_size.x * 0.3, building_size.y * 0.3, building_size.z * 0.2),
            "floor_level": 1
        },
        {
            "name": "Weapons_Cache",
            "position": (building_size.x * 0.25, -building_size.y * 0.25, 0),
            "size": (building_size.x * 0.3, building_size.y * 0.3, building_size.z * 0.2),
            "floor_level": 1
        },
        {
            "name": "Planning_Room",
            "position": (-building_size.x * 0.25, -building_size.y * 0.25, 0),
            "size": (building_size.x * 0.3, building_size.y * 0.3, building_size.z * 0.2),
            "floor_level": 1
        }
    ]
    
    # Create each room
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        room_size = room_data["size"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.3
        
        # Create room floor
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(room_x, room_y, room_z)
        )
        floor = bpy.context.active_object
        floor.name = f"BlackNexus_{room_name}_Floor"
        
        # Edit the floor to make it look worn
        bm = bmesh.from_edit_mesh(floor.data)
        
        # Scale floor
        for v in bm.verts:
            v.co.x *= room_size[0]
            v.co.y *= room_size[1]
            v.co.z *= 0.1
        
        # Distort vertices slightly for worn look
        for v in bm.verts:
            if v.co.z > 0 and random.random() > 0.7:
                v.co.z += random.uniform(-0.05, 0.05)
        
        # Update mesh
        bmesh.update_edit_mesh(floor.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        floor.data.materials.append(interior_materials["BlackNexus_Interior"])
        
        room_objects.append(floor)
        
        # Create room ceiling
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(room_x, room_y, room_z + room_size[2])
        )
        ceiling = bpy.context.active_object
        ceiling.name = f"BlackNexus_{room_name}_Ceiling"
        
        # Edit the ceiling to make it look worn
        bm = bmesh.from_edit_mesh(ceiling.data)
        
        # Scale ceiling
        for v in bm.verts:
            v.co.x *= room_size[0]
            v.co.y *= room_size[1]
            v.co.z *= 0.1
        
        # Distort vertices slightly for worn look
        for v in bm.verts:
            if v.co.z < 0 and random.random() > 0.7:
                v.co.z += random.uniform(-0.05, 0.05)
        
        # Update mesh
        bmesh.update_edit_mesh(ceiling.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        ceiling.data.materials.append(interior_materials["BlackNexus_Interior"])
        
        room_objects.append(ceiling)
        
        # Create room walls
        for wall_idx in range(4):
            # Determine wall position
            if wall_idx == 0:  # Front wall
                wall_x = room_x
                wall_y = room_y - room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            elif wall_idx == 1:  # Right wall
                wall_x = room_x + room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            elif wall_idx == 2:  # Back wall
                wall_x = room_x
                wall_y = room_y + room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            else:  # Left wall
                wall_x = room_x - room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            
            # Create wall
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(wall_x, wall_y, room_z + room_size[2]/2)
            )
            wall = bpy.context.active_object
            wall.name = f"BlackNexus_{room_name}_Wall_{wall_idx}"
            
            # Edit the wall
            bm = bmesh.from_edit_mesh(wall.data)
            
            # Scale wall
            for v in bm.verts:
                v.co.x *= wall_width
                v.co.y *= 0.1
                v.co.z *= room_size[2]
            
            # Update mesh
            bmesh.update_edit_mesh(wall.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Rotate wall
            wall.rotation_euler.z = wall_rot_z
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            wall.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(wall)
        
        # Add room-specific elements
        if room_name == "Main_Hub":
            # Create central meeting table
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=room_size[0] * 0.2,
                depth=0.5,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            table = bpy.context.active_object
            table.name = "BlackNexus_Central_Table"
            
            # Assign material
            table.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(table)
            
            # Create chairs around table
            chair_count = 6
            for i in range(chair_count):
                angle = i * (2 * math.pi / chair_count)
                chair_x = room_x + room_size[0] * 0.25 * math.cos(angle)
                chair_y = room_y + room_size[1] * 0.25 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(chair_x, chair_y, room_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"BlackNexus_Chair_{i}"
                
                # Edit the chair to make it look makeshift
                bm = bmesh.from_edit_mesh(chair.data)
                
                # Scale chair
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.3
                    v.co.z *= 0.3
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(chair.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate to face table
                direction = Vector((room_x, room_y, 0)) - Vector((chair_x, chair_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                chair.rotation_euler = rot_quat.to_euler()
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                chair.data.materials.append(interior_materials["BlackNexus_Interior"])
                
                room_objects.append(chair)
            
            # Create escape tunnel entrance
            tunnel_x = room_x - room_size[0] * 0.3
            tunnel_y = room_y - room_size[1] * 0.3
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=1.0,
                depth=0.2,
                enter_editmode=False,
                align='WORLD',
                location=(tunnel_x, tunnel_y, room_z + 0.1)
            )
            tunnel = bpy.context.active_object
            tunnel.name = "BlackNexus_Escape_Tunnel"
            
            # Assign material
            tunnel.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(tunnel)
            
            # Create tunnel hatch
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=0.9,
                depth=0.05,
                enter_editmode=False,
                align='WORLD',
                location=(tunnel_x, tunnel_y, room_z + 0.2)
            )
            hatch = bpy.context.active_object
            hatch.name = "BlackNexus_Tunnel_Hatch"
            
            # Create hatch material
            hatch_material = bpy.data.materials.new(name="BlackNexus_HatchMaterial")
            hatch_material.use_nodes = True
            nodes = hatch_material.node_tree.nodes
            links = hatch_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
            principled.inputs['Metallic'].default_value = 0.8
            principled.inputs['Roughness'].default_value = 0.6
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            hatch.data.materials.append(hatch_material)
            
            room_objects.append(hatch)
            
            # Create surveillance system
            for i in range(3):
                camera_x = room_x + room_size[0] * 0.4 * math.cos(i * 2 * math.pi / 3)
                camera_y = room_y + room_size[1] * 0.4 * math.sin(i * 2 * math.pi / 3)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(camera_x, camera_y, room_z + room_size[2] - 0.2)
                )
                camera = bpy.context.active_object
                camera.name = f"BlackNexus_Camera_{i}"
                
                # Scale camera
                camera.scale.x = 0.1
                camera.scale.y = 0.1
                camera.scale.z = 0.1
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Rotate to face center
                direction = Vector((room_x, room_y, room_z)) - Vector((camera_x, camera_y, room_z + room_size[2] - 0.2))
                rot_quat = direction.to_track_quat('Z', 'Y')
                camera.rotation_euler = rot_quat.to_euler()
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                camera.data.materials.append(interior_materials["BlackNexus_Interior"])
                
                room_objects.append(camera)
            
        elif room_name == "Communication_Center":
            # Create communication equipment
            
            # Create main console
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            console = bpy.context.active_object
            console.name = "BlackNexus_Comm_Console"
            
            # Scale console
            console.scale.x = room_size[0] * 0.4
            console.scale.y = room_size[1] * 0.2
            console.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            console.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(console)
            
            # Create monitors
            for i in range(3):
                monitor_x = room_x - room_size[0] * 0.2 + i * room_size[0] * 0.2
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(monitor_x, room_y - room_size[1] * 0.15, room_z + 1.0)
                )
                monitor = bpy.context.active_object
                monitor.name = f"BlackNexus_Monitor_{i}"
                
                # Scale monitor
                monitor.scale.x = 0.3
                monitor.scale.y = 0.05
                monitor.scale.z = 0.2
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create monitor screen material
                monitor_material = bpy.data.materials.new(name=f"BlackNexus_MonitorMaterial_{i}")
                monitor_material.use_nodes = True
                nodes = monitor_material.node_tree.nodes
                links = monitor_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties with random color
                r = random.uniform(0.0, 0.3)
                g = random.uniform(0.3, 0.8)
                b = random.uniform(0.0, 0.3)
                emission.inputs['Color'].default_value = (r, g, b, 1.0)
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                monitor.data.materials.append(monitor_material)
                
                room_objects.append(monitor)
            
            # Create antenna
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.05,
                depth=2.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x + room_size[0] * 0.3, room_y + room_size[1] * 0.3, room_z + room_size[2] - 1.0)
            )
            antenna = bpy.context.active_object
            antenna.name = "BlackNexus_Antenna"
            
            # Assign material
            antenna.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(antenna)
            
            # Create chair
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.3)
            )
            chair = bpy.context.active_object
            chair.name = "BlackNexus_Comm_Chair"
            
            # Edit the chair to make it look makeshift
            bm = bmesh.from_edit_mesh(chair.data)
            
            # Scale chair
            for v in bm.verts:
                v.co.x *= 0.3
                v.co.y *= 0.3
                v.co.z *= 0.3
            
            # Distort vertices for makeshift look
            for v in bm.verts:
                if random.random() > 0.7:
                    v.co.x += random.uniform(-0.05, 0.05)
                    v.co.y += random.uniform(-0.05, 0.05)
                    v.co.z += random.uniform(-0.05, 0.05)
            
            # Update mesh
            bmesh.update_edit_mesh(chair.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Assign material
            chair.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(chair)
            
        elif room_name == "Sleeping_Quarters":
            # Create sleeping areas
            
            # Create bunks
            for i in range(4):
                bunk_x = room_x - room_size[0] * 0.3 + (i % 2) * room_size[0] * 0.6
                bunk_y = room_y - room_size[1] * 0.3 + (i // 2) * room_size[1] * 0.6
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(bunk_x, bunk_y, room_z + 0.3)
                )
                bunk = bpy.context.active_object
                bunk.name = f"BlackNexus_Bunk_{i}"
                
                # Scale bunk
                bunk.scale.x = room_size[0] * 0.2
                bunk.scale.y = room_size[1] * 0.3
                bunk.scale.z = 0.1
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create bunk material
                bunk_material = bpy.data.materials.new(name=f"BlackNexus_BunkMaterial_{i}")
                bunk_material.use_nodes = True
                nodes = bunk_material.node_tree.nodes
                links = bunk_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.3, 1.0)  # Dark blue-gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                bunk.data.materials.append(bunk_material)
                
                room_objects.append(bunk)
                
                # Create pillow
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(bunk_x - room_size[0] * 0.15, bunk_y, room_z + 0.35)
                )
                pillow = bpy.context.active_object
                pillow.name = f"BlackNexus_Pillow_{i}"
                
                # Scale pillow
                pillow.scale.x = room_size[0] * 0.05
                pillow.scale.y = room_size[1] * 0.1
                pillow.scale.z = 0.05
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create pillow material
                pillow_material = bpy.data.materials.new(name=f"BlackNexus_PillowMaterial_{i}")
                pillow_material.use_nodes = True
                nodes = pillow_material.node_tree.nodes
                links = pillow_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.4, 1.0)  # Dark blue-gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                pillow.data.materials.append(pillow_material)
                
                room_objects.append(pillow)
            
            # Create storage lockers
            for i in range(4):
                locker_x = room_x - room_size[0] * 0.4 + (i % 2) * room_size[0] * 0.8
                locker_y = room_y - room_size[1] * 0.4 + (i // 2) * room_size[1] * 0.8
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(locker_x, locker_y, room_z + 1.0)
                )
                locker = bpy.context.active_object
                locker.name = f"BlackNexus_Locker_{i}"
                
                # Scale locker
                locker.scale.x = room_size[0] * 0.1
                locker.scale.y = room_size[1] * 0.1
                locker.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                locker.data.materials.append(interior_materials["BlackNexus_Interior"])
                
                room_objects.append(locker)
            
        elif room_name == "Weapons_Cache":
            # Create weapons storage
            
            # Create weapon racks
            for i in range(2):
                rack_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.6
                rack_y = room_y
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(rack_x, rack_y, room_z + 1.0)
                )
                rack = bpy.context.active_object
                rack.name = f"BlackNexus_Weapon_Rack_{i}"
                
                # Scale rack
                rack.scale.x = room_size[0] * 0.2
                rack.scale.y = room_size[1] * 0.1
                rack.scale.z = 2.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                rack.data.materials.append(interior_materials["BlackNexus_Interior"])
                
                room_objects.append(rack)
                
                # Create weapons on rack
                for j in range(3):
                    weapon_z = room_z + 0.5 + j * 0.5
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(rack_x, rack_y - room_size[1] * 0.05, weapon_z)
                    )
                    weapon = bpy.context.active_object
                    weapon.name = f"BlackNexus_Weapon_{i}_{j}"
                    
                    # Scale weapon
                    weapon.scale.x = 0.1
                    weapon.scale.y = 0.5
                    weapon.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create weapon material
                    weapon_material = bpy.data.materials.new(name=f"BlackNexus_WeaponMaterial_{i}_{j}")
                    weapon_material.use_nodes = True
                    nodes = weapon_material.node_tree.nodes
                    links = weapon_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set properties
                    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
                    principled.inputs['Metallic'].default_value = 0.8
                    principled.inputs['Roughness'].default_value = 0.2
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    weapon.data.materials.append(weapon_material)
                    
                    room_objects.append(weapon)
            
            # Create ammo crates
            for i in range(4):
                crate_x = room_x - room_size[0] * 0.3 + (i % 2) * room_size[0] * 0.6
                crate_y = room_y - room_size[1] * 0.3 + (i // 2) * room_size[1] * 0.6
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(crate_x, crate_y, room_z + 0.3)
                )
                crate = bpy.context.active_object
                crate.name = f"BlackNexus_Ammo_Crate_{i}"
                
                # Scale crate
                crate.scale.x = room_size[0] * 0.1
                crate.scale.y = room_size[1] * 0.1
                crate.scale.z = 0.2
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create crate material
                crate_material = bpy.data.materials.new(name=f"BlackNexus_CrateMaterial_{i}")
                crate_material.use_nodes = True
                nodes = crate_material.node_tree.nodes
                links = crate_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.1, 1.0)  # Dark olive
                principled.inputs['Metallic'].default_value = 0.1
                principled.inputs['Roughness'].default_value = 0.8
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                crate.data.materials.append(crate_material)
                
                room_objects.append(crate)
            
            # Create hidden compartment
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y - room_size[1] * 0.4, room_z + 0.1)
            )
            compartment = bpy.context.active_object
            compartment.name = "BlackNexus_Hidden_Compartment"
            
            # Scale compartment
            compartment.scale.x = room_size[0] * 0.3
            compartment.scale.y = room_size[1] * 0.1
            compartment.scale.z = 0.1
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            compartment.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(compartment)
            
        elif room_name == "Planning_Room":
            # Create planning room with maps and strategy table
            
            # Create strategy table
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            table = bpy.context.active_object
            table.name = "BlackNexus_Strategy_Table"
            
            # Scale table
            table.scale.x = room_size[0] * 0.5
            table.scale.y = room_size[1] * 0.3
            table.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            table.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(table)
            
            # Create map on table
            bpy.ops.mesh.primitive_plane_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 1.01)
            )
            map_obj = bpy.context.active_object
            map_obj.name = "BlackNexus_Map"
            
            # Scale map
            map_obj.scale.x = room_size[0] * 0.45
            map_obj.scale.y = room_size[1] * 0.25
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create map material
            map_material = bpy.data.materials.new(name="BlackNexus_MapMaterial")
            map_material.use_nodes = True
            nodes = map_material.node_tree.nodes
            links = map_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.8, 0.7, 0.5, 1.0)  # Tan color for map
            principled.inputs['Roughness'].default_value = 0.9
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            map_obj.data.materials.append(map_material)
            
            room_objects.append(map_obj)
            
            # Create chairs around table
            chair_count = 4
            for i in range(chair_count):
                if i < 2:
                    chair_x = room_x - room_size[0] * 0.2 + i * room_size[0] * 0.4
                    chair_y = room_y - room_size[1] * 0.2
                else:
                    chair_x = room_x - room_size[0] * 0.2 + (i-2) * room_size[0] * 0.4
                    chair_y = room_y + room_size[1] * 0.2
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(chair_x, chair_y, room_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"BlackNexus_Planning_Chair_{i}"
                
                # Edit the chair to make it look makeshift
                bm = bmesh.from_edit_mesh(chair.data)
                
                # Scale chair
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.3
                    v.co.z *= 0.3
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(chair.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate to face table
                direction = Vector((room_x, room_y, 0)) - Vector((chair_x, chair_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                chair.rotation_euler = rot_quat.to_euler()
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                chair.data.materials.append(interior_materials["BlackNexus_Interior"])
                
                room_objects.append(chair)
            
            # Create wall maps
            for i in range(2):
                map_x = room_x - room_size[0] * 0.4 + i * room_size[0] * 0.8
                map_y = room_y + room_size[1] * 0.49
                
                bpy.ops.mesh.primitive_plane_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(map_x, map_y, room_z + 1.5)
                )
                wall_map = bpy.context.active_object
                wall_map.name = f"BlackNexus_Wall_Map_{i}"
                
                # Scale wall map
                wall_map.scale.x = room_size[0] * 0.3
                wall_map.scale.y = room_size[1] * 0.3
                
                # Rotate to face into room
                wall_map.rotation_euler.x = math.radians(90)
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Create wall map material
                wall_map_material = bpy.data.materials.new(name=f"BlackNexus_WallMapMaterial_{i}")
                wall_map_material.use_nodes = True
                nodes = wall_map_material.node_tree.nodes
                links = wall_map_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Light gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                wall_map.data.materials.append(wall_map_material)
                
                room_objects.append(wall_map)
    
    # Create connecting corridors between rooms
    corridor_data = [
        {
            "start": "Main_Hub",
            "end": "Communication_Center",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Main_Hub",
            "end": "Sleeping_Quarters",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Main_Hub",
            "end": "Weapons_Cache",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Main_Hub",
            "end": "Planning_Room",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        }
    ]
    
    # Find room positions
    room_positions = {}
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.3
        
        room_positions[room_name] = (room_x, room_y, room_z)
    
    # Create corridors
    for corridor in corridor_data:
        start_name = corridor["start"]
        end_name = corridor["end"]
        corridor_width = corridor["width"]
        corridor_height = corridor["height"]
        
        if start_name in room_positions and end_name in room_positions:
            start_pos = room_positions[start_name]
            end_pos = room_positions[end_name]
            
            # Calculate corridor direction and length
            direction = Vector((end_pos[0], end_pos[1], 0)) - Vector((start_pos[0], start_pos[1], 0))
            length = direction.length
            direction.normalize()
            
            # Create corridor
            corridor_x = (start_pos[0] + end_pos[0]) / 2
            corridor_y = (start_pos[1] + end_pos[1]) / 2
            corridor_z = end_pos[2]  # Use end room's z position
            
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(corridor_x, corridor_y, corridor_z + corridor_height/2)
            )
            corridor_obj = bpy.context.active_object
            corridor_obj.name = f"BlackNexus_Corridor_{start_name}_to_{end_name}"
            
            # Edit the corridor
            bm = bmesh.from_edit_mesh(corridor_obj.data)
            
            # Scale corridor
            for v in bm.verts:
                v.co.x *= length
                v.co.y *= corridor_width
                v.co.z *= corridor_height
            
            # Update mesh
            bmesh.update_edit_mesh(corridor_obj.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Rotate corridor to point from start to end
            corridor_obj.rotation_euler.z = math.atan2(direction.y, direction.x)
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            corridor_obj.data.materials.append(interior_materials["BlackNexus_Interior"])
            
            room_objects.append(corridor_obj)
    
    # Move all objects to the rooms collection
    for obj in room_objects:
        if obj.name not in rooms_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
    
    return rooms_collection


def create_wire_nest_rooms(wire_nest_objects, materials, interior_materials):
    """Create rooms for Wire Nest (Mid Tier hacker den)
	Neon Crucible - Wire Nest Rooms Implementation
	Blender 4.2 Python Script for generating rooms per floor for the Wire Nest building
	in the Neon Crucible cyberpunk world.
	"""
    # Extract objects from the wire_nest_objects dictionary
    building = wire_nest_objects.get("building")
    collection = wire_nest_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Wire Nest objects")
        return None
    
    # Create a subcollection for room objects
    if "WireNest_Rooms" not in bpy.data.collections:
        rooms_collection = bpy.data.collections.new("WireNest_Rooms")
        collection.children.link(rooms_collection)
    else:
        rooms_collection = bpy.data.collections["WireNest_Rooms"]
    
    room_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Define room positions relative to building center
    rooms_data = [
        {
            "name": "Server_Room",
            "position": (0, 0, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.4, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Communal_Hacking",
            "position": (building_size.x * 0.3, 0, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.6, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Private_Booths",
            "position": (-building_size.x * 0.3, 0, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.6, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Hardware_Workshop",
            "position": (0, building_size.y * 0.3, 0),
            "size": (building_size.x * 0.6, building_size.y * 0.3, building_size.z * 0.3),
            "floor_level": 1
        },
        {
            "name": "Relaxation_Area",
            "position": (0, -building_size.y * 0.3, 0),
            "size": (building_size.x * 0.6, building_size.y * 0.3, building_size.z * 0.3),
            "floor_level": 1
        }
    ]
    
    # Create each room
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        room_size = room_data["size"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.4
        
        # Create room floor
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(room_x, room_y, room_z)
        )
        floor = bpy.context.active_object
        floor.name = f"WireNest_{room_name}_Floor"
        
        # Edit the floor
        bm = bmesh.from_edit_mesh(floor.data)
        
        # Scale floor
        for v in bm.verts:
            v.co.x *= room_size[0]
            v.co.y *= room_size[1]
            v.co.z *= 0.1
        
        # Update mesh
        bmesh.update_edit_mesh(floor.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        floor.data.materials.append(interior_materials["WireNest_Interior"])
        
        room_objects.append(floor)
        
        # Create room ceiling
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(room_x, room_y, room_z + room_size[2])
        )
        ceiling = bpy.context.active_object
        ceiling.name = f"WireNest_{room_name}_Ceiling"
        
        # Edit the ceiling
        bm = bmesh.from_edit_mesh(ceiling.data)
        
        # Scale ceiling
        for v in bm.verts:
            v.co.x *= room_size[0]
            v.co.y *= room_size[1]
            v.co.z *= 0.1
        
        # Update mesh
        bmesh.update_edit_mesh(ceiling.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        ceiling.data.materials.append(interior_materials["WireNest_Interior"])
        
        room_objects.append(ceiling)
        
        # Create room walls
        for wall_idx in range(4):
            # Determine wall position
            if wall_idx == 0:  # Front wall
                wall_x = room_x
                wall_y = room_y - room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            elif wall_idx == 1:  # Right wall
                wall_x = room_x + room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            elif wall_idx == 2:  # Back wall
                wall_x = room_x
                wall_y = room_y + room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            else:  # Left wall
                wall_x = room_x - room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            
            # Create wall
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(wall_x, wall_y, room_z + room_size[2]/2)
            )
            wall = bpy.context.active_object
            wall.name = f"WireNest_{room_name}_Wall_{wall_idx}"
            
            # Edit the wall
            bm = bmesh.from_edit_mesh(wall.data)
            
            # Scale wall
            for v in bm.verts:
                v.co.x *= wall_width
                v.co.y *= 0.1
                v.co.z *= room_size[2]
            
            # Update mesh
            bmesh.update_edit_mesh(wall.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Rotate wall
            wall.rotation_euler.z = wall_rot_z
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            wall.data.materials.append(interior_materials["WireNest_Interior"])
            
            room_objects.append(wall)
        
        # Add room-specific elements
        if room_name == "Server_Room":
            # Create server racks
            rack_count = 6
            for i in range(rack_count):
                angle = i * (2 * math.pi / rack_count)
                rack_x = room_x + room_size[0] * 0.3 * math.cos(angle)
                rack_y = room_y + room_size[1] * 0.3 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(rack_x, rack_y, room_z + room_size[2]/2)
                )
                rack = bpy.context.active_object
                rack.name = f"WireNest_Server_Rack_{i}"
                
                # Scale rack
                rack.scale.x = 0.5
                rack.scale.y = 0.5
                rack.scale.z = room_size[2] * 0.9
                
                # Rotate to face center
                direction = Vector((room_x, room_y, 0)) - Vector((rack_x, rack_y, 0))
                rot_quat = direction.to_track_quat('Y', 'Z')
                rack.rotation_euler = rot_quat.to_euler()
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                rack.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(rack)
                
                # Create server lights
                for j in range(10):
                    light_z = room_z + 0.2 + j * (room_size[2] * 0.8 / 10)
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(rack_x, rack_y - 0.26, light_z)
                    )
                    light = bpy.context.active_object
                    light.name = f"WireNest_Server_Light_{i}_{j}"
                    
                    # Scale light
                    light.scale.x = 0.1
                    light.scale.y = 0.02
                    light.scale.z = 0.02
                    
                    # Rotate to match rack
                    light.rotation_euler = rack.rotation_euler
                    
                    # Apply transformations
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                    
                    # Create light material with random color
                    light_material = bpy.data.materials.new(name=f"WireNest_ServerLight_Material_{i}_{j}")
                    light_material.use_nodes = True
                    nodes = light_material.node_tree.nodes
                    links = light_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    emission = nodes.new(type='ShaderNodeEmission')
                    
                    # Set properties with random color
                    r = random.choice([0.0, 0.0, 1.0, 0.0])
                    g = random.choice([0.0, 1.0, 0.0, 0.0])
                    b = random.choice([1.0, 0.0, 0.0, 1.0])
                    emission.inputs['Color'].default_value = (r, g, b, 1.0)
                    emission.inputs['Strength'].default_value = 3.0
                    
                    # Connect nodes
                    links.new(emission.outputs['Emission'], output.inputs['Surface'])
                    
                    # Assign material
                    light.data.materials.append(light_material)
                    
                    room_objects.append(light)
            
            # Create central cooling unit
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=room_size[0] * 0.1,
                depth=room_size[2] * 0.8,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + room_size[2]/2)
            )
            cooling = bpy.context.active_object
            cooling.name = "WireNest_Cooling_Unit"
            
            # Assign material
            cooling_material = bpy.data.materials.new(name="WireNest_CoolingMaterial")
            cooling_material.use_nodes = True
            nodes = cooling_material.node_tree.nodes
            links = cooling_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Light gray
            principled.inputs['Metallic'].default_value = 0.9
            principled.inputs['Roughness'].default_value = 0.1
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            cooling.data.materials.append(cooling_material)
            
            room_objects.append(cooling)
            
            # Create cable ceiling
            cable_count = 20
            for i in range(cable_count):
                start_x = room_x + random.uniform(-room_size[0] * 0.4, room_size[0] * 0.4)
                start_y = room_y + random.uniform(-room_size[1] * 0.4, room_size[1] * 0.4)
                end_x = room_x + random.uniform(-room_size[0] * 0.4, room_size[0] * 0.4)
                end_y = room_y + random.uniform(-room_size[1] * 0.4, room_size[1] * 0.4)
                
                # Create cable curve
                curve_data = bpy.data.curves.new(f'WireNest_Cable_Curve_{i}', type='CURVE')
                curve_data.dimensions = '3D'
                curve_data.resolution_u = 2
                
                # Create spline
                spline = curve_data.splines.new('BEZIER')
                spline.bezier_points.add(1)  # Two points total
                
                # Set spline points
                spline.bezier_points[0].co = (start_x, start_y, room_z + room_size[2] - 0.05)
                spline.bezier_points[1].co = (end_x, end_y, room_z + room_size[2] - 0.05)
                
                # Set handle types
                for point in spline.bezier_points:
                    point.handle_left_type = 'AUTO'
                    point.handle_right_type = 'AUTO'
                
                # Create curve object
                cable = bpy.data.objects.new(f"WireNest_Cable_{i}", curve_data)
                
                # Set curve properties
                cable.data.bevel_depth = 0.02  # Cable thickness
                
                # Create cable material with random color
                cable_material = bpy.data.materials.new(name=f"WireNest_CableMaterial_{i}")
                cable_material.use_nodes = True
                nodes = cable_material.node_tree.nodes
                links = cable_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set random color
                r = random.uniform(0.0, 0.3)
                g = random.uniform(0.0, 0.3)
                b = random.uniform(0.0, 0.3)
                
                # Randomly choose one color to be brighter
                bright_channel = random.randint(0, 2)
                if bright_channel == 0:
                    r = random.uniform(0.7, 1.0)
                elif bright_channel == 1:
                    g = random.uniform(0.7, 1.0)
                else:
                    b = random.uniform(0.7, 1.0)
                
                principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                principled.inputs['Roughness'].default_value = 0.3
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                cable.data.materials.append(cable_material)
                
                # Link to scene
                rooms_collection.objects.link(cable)
                
                room_objects.append(cable)
            
        elif room_name == "Communal_Hacking":
            # Create communal hacking space with workstations
            
            # Create central table
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            table = bpy.context.active_object
            table.name = "WireNest_Communal_Table"
            
            # Scale table
            table.scale.x = room_size[0] * 0.7
            table.scale.y = room_size[1] * 0.5
            table.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            table.data.materials.append(interior_materials["WireNest_Interior"])
            
            room_objects.append(table)
            
            # Create workstations around table
            station_count = 8
            for i in range(station_count):
                # Calculate position around table
                if i < 3:  # Front side
                    station_x = room_x - room_size[0] * 0.25 + i * room_size[0] * 0.25
                    station_y = room_y - room_size[1] * 0.2
                    rotation_z = 0
                elif i < 6:  # Back side
                    station_x = room_x - room_size[0] * 0.25 + (i-3) * room_size[0] * 0.25
                    station_y = room_y + room_size[1] * 0.2
                    rotation_z = math.radians(180)
                elif i == 6:  # Left side
                    station_x = room_x - room_size[0] * 0.3
                    station_y = room_y
                    rotation_z = math.radians(90)
                else:  # Right side
                    station_x = room_x + room_size[0] * 0.3
                    station_y = room_y
                    rotation_z = math.radians(270)
                
                # Create monitor
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(station_x, station_y, room_z + 1.0)
                )
                monitor = bpy.context.active_object
                monitor.name = f"WireNest_Monitor_{i}"
                
                # Scale monitor
                monitor.scale.x = 0.4
                monitor.scale.y = 0.05
                monitor.scale.z = 0.3
                
                # Rotate monitor
                monitor.rotation_euler.z = rotation_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Create monitor screen material
                monitor_material = bpy.data.materials.new(name=f"WireNest_MonitorMaterial_{i}")
                monitor_material.use_nodes = True
                nodes = monitor_material.node_tree.nodes
                links = monitor_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties with random color
                r = random.uniform(0.0, 0.3)
                g = random.uniform(0.3, 0.8)
                b = random.uniform(0.3, 0.8)
                emission.inputs['Color'].default_value = (r, g, b, 1.0)
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                monitor.data.materials.append(monitor_material)
                
                room_objects.append(monitor)
                
                # Create keyboard
                keyboard_y_offset = 0.2 if rotation_z < math.radians(90) else -0.2
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(station_x, station_y + keyboard_y_offset, room_z + 0.55)
                )
                keyboard = bpy.context.active_object
                keyboard.name = f"WireNest_Keyboard_{i}"
                
                # Scale keyboard
                keyboard.scale.x = 0.3
                keyboard.scale.y = 0.15
                keyboard.scale.z = 0.05
                
                # Rotate keyboard
                keyboard.rotation_euler.z = rotation_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                keyboard.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(keyboard)
                
                # Create chair
                chair_y_offset = 0.4 if rotation_z < math.radians(90) else -0.4
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(station_x, station_y + chair_y_offset, room_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"WireNest_Chair_{i}"
                
                # Scale chair
                chair.scale.x = 0.3
                chair.scale.y = 0.3
                chair.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                chair.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(chair)
            
            # Create screen walls
            for i in range(4):
                # Determine wall position
                if i == 0:  # Front wall
                    wall_x = room_x
                    wall_y = room_y - room_size[1]/2 + 0.1
                    wall_rot_z = 0
                    wall_width = room_size[0] * 0.8
                elif i == 1:  # Right wall
                    wall_x = room_x + room_size[0]/2 - 0.1
                    wall_y = room_y
                    wall_rot_z = math.radians(90)
                    wall_width = room_size[1] * 0.8
                elif i == 2:  # Back wall
                    wall_x = room_x
                    wall_y = room_y + room_size[1]/2 - 0.1
                    wall_rot_z = 0
                    wall_width = room_size[0] * 0.8
                else:  # Left wall
                    wall_x = room_x - room_size[0]/2 + 0.1
                    wall_y = room_y
                    wall_rot_z = math.radians(90)
                    wall_width = room_size[1] * 0.8
                
                # Create screen wall
                bpy.ops.mesh.primitive_plane_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(wall_x, wall_y, room_z + room_size[2]/2)
                )
                screen_wall = bpy.context.active_object
                screen_wall.name = f"WireNest_ScreenWall_{i}"
                
                # Scale screen wall
                screen_wall.scale.x = wall_width
                screen_wall.scale.y = room_size[2] * 0.8
                
                # Rotate screen wall
                screen_wall.rotation_euler.x = math.radians(90)
                screen_wall.rotation_euler.z = wall_rot_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Create screen wall material
                screen_material = bpy.data.materials.new(name=f"WireNest_ScreenMaterial_{i}")
                screen_material.use_nodes = True
                nodes = screen_material.node_tree.nodes
                links = screen_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties
                emission.inputs['Color'].default_value = (0.0, 0.1, 0.2, 1.0)  # Dark blue
                emission.inputs['Strength'].default_value = 0.5
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                screen_wall.data.materials.append(screen_material)
                
                room_objects.append(screen_wall)
            
        elif room_name == "Private_Booths":
            # Create private hacking booths
            
            # Create booths
            booth_count = 6
            for i in range(booth_count):
                # Calculate booth position
                if i < 3:  # Left side
                    booth_x = room_x - room_size[0] * 0.3
                    booth_y = room_y - room_size[1] * 0.3 + i * room_size[1] * 0.3
                    booth_rot_z = math.radians(90)
                else:  # Right side
                    booth_x = room_x + room_size[0] * 0.3
                    booth_y = room_y - room_size[1] * 0.3 + (i-3) * room_size[1] * 0.3
                    booth_rot_z = math.radians(270)
                
                # Create booth base
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(booth_x, booth_y, room_z + 0.5)
                )
                booth = bpy.context.active_object
                booth.name = f"WireNest_Booth_{i}"
                
                # Scale booth
                booth.scale.x = room_size[0] * 0.15
                booth.scale.y = room_size[1] * 0.15
                booth.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                booth.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(booth)
                
                # Create booth walls
                for j in range(3):
                    # Skip front wall
                    if j == 0:
                        continue
                    
                    # Determine wall position
                    if j == 1:  # Left wall
                        wall_x = booth_x - room_size[0] * 0.15
                        wall_y = booth_y
                        wall_rot_z = math.radians(90)
                        wall_width = room_size[1] * 0.15
                    elif j == 2:  # Right wall
                        wall_x = booth_x + room_size[0] * 0.15
                        wall_y = booth_y
                        wall_rot_z = math.radians(90)
                        wall_width = room_size[1] * 0.15
                    else:  # Back wall
                        wall_x = booth_x
                        wall_y = booth_y + room_size[1] * 0.15
                        wall_rot_z = 0
                        wall_width = room_size[0] * 0.15
                    
                    # Create wall
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=True,
                        align='WORLD',
                        location=(wall_x, wall_y, room_z + 1.5)
                    )
                    wall = bpy.context.active_object
                    wall.name = f"WireNest_Booth_Wall_{i}_{j}"
                    
                    # Edit the wall
                    bm = bmesh.from_edit_mesh(wall.data)
                    
                    # Scale wall
                    for v in bm.verts:
                        v.co.x *= wall_width
                        v.co.y *= 0.05
                        v.co.z *= 2.0
                    
                    # Update mesh
                    bmesh.update_edit_mesh(wall.data)
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                    # Rotate wall
                    wall.rotation_euler.z = wall_rot_z
                    
                    # Apply rotation
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                    
                    # Assign material
                    wall.data.materials.append(interior_materials["WireNest_Interior"])
                    
                    room_objects.append(wall)
                
                # Create monitor
                monitor_y_offset = -0.1 if i < 3 else 0.1
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(booth_x, booth_y + monitor_y_offset, room_z + 1.0)
                )
                monitor = bpy.context.active_object
                monitor.name = f"WireNest_Booth_Monitor_{i}"
                
                # Scale monitor
                monitor.scale.x = 0.3
                monitor.scale.y = 0.05
                monitor.scale.z = 0.2
                
                # Rotate monitor
                monitor.rotation_euler.z = booth_rot_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Create monitor screen material
                monitor_material = bpy.data.materials.new(name=f"WireNest_BoothMonitorMaterial_{i}")
                monitor_material.use_nodes = True
                nodes = monitor_material.node_tree.nodes
                links = monitor_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties with random color
                r = random.uniform(0.0, 0.3)
                g = random.uniform(0.3, 0.8)
                b = random.uniform(0.3, 0.8)
                emission.inputs['Color'].default_value = (r, g, b, 1.0)
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                monitor.data.materials.append(monitor_material)
                
                room_objects.append(monitor)
                
                # Create keyboard
                keyboard_y_offset = -0.2 if i < 3 else 0.2
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(booth_x, booth_y + keyboard_y_offset, room_z + 0.55)
                )
                keyboard = bpy.context.active_object
                keyboard.name = f"WireNest_Booth_Keyboard_{i}"
                
                # Scale keyboard
                keyboard.scale.x = 0.2
                keyboard.scale.y = 0.1
                keyboard.scale.z = 0.05
                
                # Rotate keyboard
                keyboard.rotation_euler.z = booth_rot_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                keyboard.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(keyboard)
                
                # Create chair
                chair_y_offset = -0.3 if i < 3 else 0.3
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(booth_x, booth_y + chair_y_offset, room_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"WireNest_Booth_Chair_{i}"
                
                # Scale chair
                chair.scale.x = 0.2
                chair.scale.y = 0.2
                chair.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                chair.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(chair)
            
        elif room_name == "Hardware_Workshop":
            # Create hardware workshop with workbenches and tools
            
            # Create workbenches
            bench_count = 3
            for i in range(bench_count):
                bench_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.3
                bench_y = room_y
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(bench_x, bench_y, room_z + 0.5)
                )
                bench = bpy.context.active_object
                bench.name = f"WireNest_Workbench_{i}"
                
                # Scale bench
                bench.scale.x = room_size[0] * 0.2
                bench.scale.y = room_size[1] * 0.6
                bench.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                bench.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(bench)
                
                # Create tools on bench
                tool_count = 5
                for j in range(tool_count):
                    tool_x = bench_x - room_size[0] * 0.1 + j * room_size[0] * 0.05
                    tool_y = bench_y - room_size[1] * 0.2 + j % 2 * room_size[1] * 0.4
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(tool_x, tool_y, room_z + 1.0)
                    )
                    tool = bpy.context.active_object
                    tool.name = f"WireNest_Tool_{i}_{j}"
                    
                    # Scale tool
                    tool.scale.x = 0.1
                    tool.scale.y = 0.1
                    tool.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create tool material with random color
                    tool_material = bpy.data.materials.new(name=f"WireNest_ToolMaterial_{i}_{j}")
                    tool_material.use_nodes = True
                    nodes = tool_material.node_tree.nodes
                    links = tool_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set random color
                    r = random.uniform(0.2, 0.8)
                    g = random.uniform(0.2, 0.8)
                    b = random.uniform(0.2, 0.8)
                    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                    principled.inputs['Metallic'].default_value = 0.7
                    principled.inputs['Roughness'].default_value = 0.3
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    tool.data.materials.append(tool_material)
                    
                    room_objects.append(tool)
            
            # Create parts storage shelves
            for i in range(2):
                shelf_x = room_x - room_size[0] * 0.45
                shelf_y = room_y - room_size[1] * 0.3 + i * room_size[1] * 0.6
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(shelf_x, shelf_y, room_z + 1.0)
                )
                shelf = bpy.context.active_object
                shelf.name = f"WireNest_Parts_Shelf_{i}"
                
                # Scale shelf
                shelf.scale.x = 0.2
                shelf.scale.y = room_size[1] * 0.2
                shelf.scale.z = 2.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                shelf.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(shelf)
                
                # Create parts bins on shelf
                for j in range(4):
                    for k in range(3):
                        bin_x = shelf_x
                        bin_y = shelf_y - room_size[1] * 0.1 + k * room_size[1] * 0.1
                        bin_z = room_z + 0.5 + j * 0.5
                        
                        bpy.ops.mesh.primitive_cube_add(
                            size=1.0,
                            enter_editmode=False,
                            align='WORLD',
                            location=(bin_x, bin_y, bin_z)
                        )
                        parts_bin = bpy.context.active_object
                        parts_bin.name = f"WireNest_Parts_Bin_{i}_{j}_{k}"
                        
                        # Scale bin
                        parts_bin.scale.x = 0.15
                        parts_bin.scale.y = 0.08
                        parts_bin.scale.z = 0.1
                        
                        # Apply scale
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        
                        # Create bin material with random color
                        bin_material = bpy.data.materials.new(name=f"WireNest_BinMaterial_{i}_{j}_{k}")
                        bin_material.use_nodes = True
                        nodes = bin_material.node_tree.nodes
                        links = bin_material.node_tree.links
                        
                        # Clear default nodes
                        for node in nodes:
                            nodes.remove(node)
                        
                        # Create nodes
                        output = nodes.new(type='ShaderNodeOutputMaterial')
                        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                        
                        # Set random color
                        r = random.uniform(0.2, 0.8)
                        g = random.uniform(0.2, 0.8)
                        b = random.uniform(0.2, 0.8)
                        principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                        principled.inputs['Roughness'].default_value = 0.9
                        
                        # Connect nodes
                        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                        
                        # Assign material
                        parts_bin.data.materials.append(bin_material)
                        
                        room_objects.append(parts_bin)
            
            # Create soldering station
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x + room_size[0] * 0.4, room_y, room_z + 0.5)
            )
            solder_station = bpy.context.active_object
            solder_station.name = "WireNest_Soldering_Station"
            
            # Scale station
            solder_station.scale.x = room_size[0] * 0.1
            solder_station.scale.y = room_size[1] * 0.3
            solder_station.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            solder_station.data.materials.append(interior_materials["WireNest_Interior"])
            
            room_objects.append(solder_station)
            
            # Create soldering iron
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.03,
                depth=0.3,
                enter_editmode=False,
                align='WORLD',
                location=(room_x + room_size[0] * 0.4, room_y, room_z + 1.0)
            )
            solder_iron = bpy.context.active_object
            solder_iron.name = "WireNest_Soldering_Iron"
            
            # Rotate iron
            solder_iron.rotation_euler.x = math.radians(45)
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Create iron material
            iron_material = bpy.data.materials.new(name="WireNest_IronMaterial")
            iron_material.use_nodes = True
            nodes = iron_material.node_tree.nodes
            links = iron_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
            principled.inputs['Metallic'].default_value = 0.8
            principled.inputs['Roughness'].default_value = 0.2
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            solder_iron.data.materials.append(iron_material)
            
            room_objects.append(solder_iron)
            
        elif room_name == "Relaxation_Area":
            # Create relaxation area with seating and entertainment
            
            # Create central seating area
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=room_size[0] * 0.2,
                depth=0.3,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.15)
            )
            seating = bpy.context.active_object
            seating.name = "WireNest_Seating_Area"
            
            # Create seating material
            seating_material = bpy.data.materials.new(name="WireNest_SeatingMaterial")
            seating_material.use_nodes = True
            nodes = seating_material.node_tree.nodes
            links = seating_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.4, 1.0)  # Dark blue-gray
            principled.inputs['Roughness'].default_value = 0.9
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            seating.data.materials.append(seating_material)
            
            room_objects.append(seating)
            
            # Create cushions on seating
            cushion_count = 6
            for i in range(cushion_count):
                angle = i * (2 * math.pi / cushion_count)
                cushion_x = room_x + room_size[0] * 0.15 * math.cos(angle)
                cushion_y = room_y + room_size[1] * 0.15 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(cushion_x, cushion_y, room_z + 0.35)
                )
                cushion = bpy.context.active_object
                cushion.name = f"WireNest_Cushion_{i}"
                
                # Scale cushion
                cushion.scale.x = 0.2
                cushion.scale.y = 0.2
                cushion.scale.z = 0.1
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create cushion material with random color
                cushion_material = bpy.data.materials.new(name=f"WireNest_CushionMaterial_{i}")
                cushion_material.use_nodes = True
                nodes = cushion_material.node_tree.nodes
                links = cushion_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set random color
                r = random.uniform(0.2, 0.8)
                g = random.uniform(0.2, 0.8)
                b = random.uniform(0.2, 0.8)
                principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                cushion.data.materials.append(cushion_material)
                
                room_objects.append(cushion)
            
            # Create entertainment screen
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y + room_size[1] * 0.45, room_z + 1.5)
            )
            screen = bpy.context.active_object
            screen.name = "WireNest_Entertainment_Screen"
            
            # Scale screen
            screen.scale.x = room_size[0] * 0.4
            screen.scale.y = 0.05
            screen.scale.z = room_size[2] * 0.4
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create screen material
            screen_material = bpy.data.materials.new(name="WireNest_ScreenMaterial")
            screen_material.use_nodes = True
            nodes = screen_material.node_tree.nodes
            links = screen_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            emission = nodes.new(type='ShaderNodeEmission')
            
            # Set properties
            emission.inputs['Color'].default_value = (0.1, 0.2, 0.4, 1.0)  # Blue
            emission.inputs['Strength'].default_value = 1.0
            
            # Connect nodes
            links.new(emission.outputs['Emission'], output.inputs['Surface'])
            
            # Assign material
            screen.data.materials.append(screen_material)
            
            room_objects.append(screen)
            
            # Create small tables
            table_count = 3
            for i in range(table_count):
                angle = i * (2 * math.pi / table_count) + math.pi/6
                table_x = room_x + room_size[0] * 0.3 * math.cos(angle)
                table_y = room_y + room_size[1] * 0.3 * math.sin(angle)
                
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=0.2,
                    depth=0.5,
                    enter_editmode=False,
                    align='WORLD',
                    location=(table_x, table_y, room_z + 0.25)
                )
                table = bpy.context.active_object
                table.name = f"WireNest_Table_{i}"
                
                # Assign material
                table.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(table)
                
                # Create items on table
                item_count = random.randint(1, 3)
                for j in range(item_count):
                    item_x = table_x + random.uniform(-0.1, 0.1)
                    item_y = table_y + random.uniform(-0.1, 0.1)
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(item_x, item_y, room_z + 0.55)
                    )
                    item = bpy.context.active_object
                    item.name = f"WireNest_Table_Item_{i}_{j}"
                    
                    # Scale item
                    item.scale.x = 0.1
                    item.scale.y = 0.1
                    item.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create item material with random color
                    item_material = bpy.data.materials.new(name=f"WireNest_ItemMaterial_{i}_{j}")
                    item_material.use_nodes = True
                    nodes = item_material.node_tree.nodes
                    links = item_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set random color
                    r = random.uniform(0.2, 0.8)
                    g = random.uniform(0.2, 0.8)
                    b = random.uniform(0.2, 0.8)
                    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                    principled.inputs['Roughness'].default_value = 0.5
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    item.data.materials.append(item_material)
                    
                    room_objects.append(item)
    
    # Create connecting corridors between rooms
    corridor_data = [
        {
            "start": "Server_Room",
            "end": "Communal_Hacking",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Server_Room",
            "end": "Private_Booths",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Server_Room",
            "end": "Hardware_Workshop",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2,
            "vertical": True
        },
        {
            "start": "Server_Room",
            "end": "Relaxation_Area",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2,
            "vertical": True
        }
    ]
    
    # Find room positions
    room_positions = {}
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.4
        
        room_positions[room_name] = (room_x, room_y, room_z)
    
    # Create corridors
    for corridor in corridor_data:
        start_name = corridor["start"]
        end_name = corridor["end"]
        corridor_width = corridor["width"]
        corridor_height = corridor["height"]
        vertical = corridor.get("vertical", False)
        
        if start_name in room_positions and end_name in room_positions:
            start_pos = room_positions[start_name]
            end_pos = room_positions[end_name]
            
            if vertical:
                # Create vertical corridor (stairwell or ladder)
                corridor_x = (start_pos[0] + end_pos[0]) / 2
                corridor_y = (start_pos[1] + end_pos[1]) / 2
                corridor_z = (start_pos[2] + end_pos[2]) / 2
                corridor_height = abs(end_pos[2] - start_pos[2])
                
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=corridor_width,
                    depth=corridor_height,
                    enter_editmode=False,
                    align='WORLD',
                    location=(corridor_x, corridor_y, corridor_z)
                )
                corridor_obj = bpy.context.active_object
                corridor_obj.name = f"WireNest_Vertical_Corridor_{start_name}_to_{end_name}"
                
                # Assign material
                corridor_obj.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(corridor_obj)
                
                # Create ladder or stairs
                if random.random() > 0.5:  # Create ladder
                    # Create ladder rungs
                    rung_count = int(corridor_height / 0.3)
                    for i in range(rung_count):
                        rung_z = corridor_z - corridor_height/2 + i * corridor_height / rung_count
                        
                        bpy.ops.mesh.primitive_cylinder_add(
                            vertices=8,
                            radius=corridor_width * 0.8,
                            depth=0.05,
                            enter_editmode=False,
                            align='WORLD',
                            location=(corridor_x, corridor_y, rung_z)
                        )
                        rung = bpy.context.active_object
                        rung.name = f"WireNest_Ladder_Rung_{start_name}_to_{end_name}_{i}"
                        
                        # Assign material
                        rung.data.materials.append(interior_materials["WireNest_Interior"])
                        
                        room_objects.append(rung)
                else:  # Create spiral stairs
                    # Create spiral stair steps
                    step_count = int(corridor_height / 0.2)
                    for i in range(step_count):
                        angle = i * (2 * math.pi / (step_count / 2))
                        step_x = corridor_x + corridor_width * 0.6 * math.cos(angle)
                        step_y = corridor_y + corridor_width * 0.6 * math.sin(angle)
                        step_z = corridor_z - corridor_height/2 + i * corridor_height / step_count
                        
                        bpy.ops.mesh.primitive_cube_add(
                            size=1.0,
                            enter_editmode=False,
                            align='WORLD',
                            location=(step_x, step_y, step_z)
                        )
                        step = bpy.context.active_object
                        step.name = f"WireNest_Stair_Step_{start_name}_to_{end_name}_{i}"
                        
                        # Scale step
                        step.scale.x = corridor_width * 0.4
                        step.scale.y = corridor_width * 0.4
                        step.scale.z = 0.05
                        
                        # Apply scale
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        
                        # Assign material
                        step.data.materials.append(interior_materials["WireNest_Interior"])
                        
                        room_objects.append(step)
            else:
                # Calculate corridor direction and length
                direction = Vector((end_pos[0], end_pos[1], 0)) - Vector((start_pos[0], start_pos[1], 0))
                length = direction.length
                direction.normalize()
                
                # Create corridor
                corridor_x = (start_pos[0] + end_pos[0]) / 2
                corridor_y = (start_pos[1] + end_pos[1]) / 2
                corridor_z = start_pos[2]  # Use start room's z position
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(corridor_x, corridor_y, corridor_z + corridor_height/2)
                )
                corridor_obj = bpy.context.active_object
                corridor_obj.name = f"WireNest_Corridor_{start_name}_to_{end_name}"
                
                # Edit the corridor
                bm = bmesh.from_edit_mesh(corridor_obj.data)
                
                # Scale corridor
                for v in bm.verts:
                    v.co.x *= length
                    v.co.y *= corridor_width
                    v.co.z *= corridor_height
                
                # Update mesh
                bmesh.update_edit_mesh(corridor_obj.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate corridor to point from start to end
                corridor_obj.rotation_euler.z = math.atan2(direction.y, direction.x)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                corridor_obj.data.materials.append(interior_materials["WireNest_Interior"])
                
                room_objects.append(corridor_obj)
    
    # Move all objects to the rooms collection
    for obj in room_objects:
        if obj.name not in rooms_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
    
    return rooms_collection


def create_rust_vault_rooms(rust_vault_objects, materials, interior_materials):
    """Create rooms for Rust Vault (Lower Tier hacker den)
	Neon Crucible - Rust Vault Rooms Implementation
	Blender 4.2 Python Script for generating rooms per floor for the Rust Vault building
	in the Neon Crucible cyberpunk world.
	"""
    # Extract objects from the rust_vault_objects dictionary
    building = rust_vault_objects.get("building")
    collection = rust_vault_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Rust Vault objects")
        return None
    
    # Create a subcollection for room objects
    if "RustVault_Rooms" not in bpy.data.collections:
        rooms_collection = bpy.data.collections.new("RustVault_Rooms")
        collection.children.link(rooms_collection)
    else:
        rooms_collection = bpy.data.collections["RustVault_Rooms"]
    
    room_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Define room positions relative to building center
    rooms_data = [
        {
            "name": "Main_Room",
            "position": (0, 0, 0),
            "size": (building_size.x * 0.7, building_size.y * 0.7, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Server_Farm",
            "position": (building_size.x * 0.3, 0, 0),
            "size": (building_size.x * 0.3, building_size.y * 0.4, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Sleeping_Area",
            "position": (-building_size.x * 0.3, 0, 0),
            "size": (building_size.x * 0.3, building_size.y * 0.4, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Faraday_Cage",
            "position": (0, building_size.y * 0.3, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.3, building_size.z * 0.3),
            "floor_level": 0
        },
        {
            "name": "Kitchen",
            "position": (0, -building_size.y * 0.3, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.3, building_size.z * 0.3),
            "floor_level": 0
        }
    ]
    
    # Create each room
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        room_size = room_data["size"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.3
        
        # Create room floor
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(room_x, room_y, room_z)
        )
        floor = bpy.context.active_object
        floor.name = f"RustVault_{room_name}_Floor"
        
        # Edit the floor to make it look worn and rusty
        bm = bmesh.from_edit_mesh(floor.data)
        
        # Scale floor
        for v in bm.verts:
            v.co.x *= room_size[0]
            v.co.y *= room_size[1]
            v.co.z *= 0.1
        
        # Distort vertices slightly for worn look
        for v in bm.verts:
            if v.co.z > 0 and random.random() > 0.6:
                v.co.z += random.uniform(-0.05, 0.05)
        
        # Update mesh
        bmesh.update_edit_mesh(floor.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        floor.data.materials.append(interior_materials["RustVault_Interior"])
        
        room_objects.append(floor)
        
        # Create room ceiling
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(room_x, room_y, room_z + room_size[2])
        )
        ceiling = bpy.context.active_object
        ceiling.name = f"RustVault_{room_name}_Ceiling"
        
        # Edit the ceiling to make it look worn and rusty
        bm = bmesh.from_edit_mesh(ceiling.data)
        
        # Scale ceiling
        for v in bm.verts:
            v.co.x *= room_size[0]
            v.co.y *= room_size[1]
            v.co.z *= 0.1
        
        # Distort vertices slightly for worn look
        for v in bm.verts:
            if v.co.z < 0 and random.random() > 0.6:
                v.co.z += random.uniform(-0.05, 0.05)
        
        # Update mesh
        bmesh.update_edit_mesh(ceiling.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Assign material
        ceiling.data.materials.append(interior_materials["RustVault_Interior"])
        
        room_objects.append(ceiling)
        
        # Create room walls
        for wall_idx in range(4):
            # Determine wall position
            if wall_idx == 0:  # Front wall
                wall_x = room_x
                wall_y = room_y - room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            elif wall_idx == 1:  # Right wall
                wall_x = room_x + room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            elif wall_idx == 2:  # Back wall
                wall_x = room_x
                wall_y = room_y + room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            else:  # Left wall
                wall_x = room_x - room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            
            # Create wall
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(wall_x, wall_y, room_z + room_size[2]/2)
            )
            wall = bpy.context.active_object
            wall.name = f"RustVault_{room_name}_Wall_{wall_idx}"
            
            # Edit the wall to make it look worn and rusty
            bm = bmesh.from_edit_mesh(wall.data)
            
            # Scale wall
            for v in bm.verts:
                v.co.x *= wall_width
                v.co.y *= 0.1
                v.co.z *= room_size[2]
            
            # Distort vertices slightly for worn look
            for v in bm.verts:
                if random.random() > 0.8:
                    v.co.x += random.uniform(-0.05, 0.05)
                    v.co.z += random.uniform(-0.05, 0.05)
            
            # Update mesh
            bmesh.update_edit_mesh(wall.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Rotate wall
            wall.rotation_euler.z = wall_rot_z
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            wall.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(wall)
        
        # Add room-specific elements
        if room_name == "Main_Room":
            # Create workstations in the main room
            
            # Create central table with workstations
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            table = bpy.context.active_object
            table.name = "RustVault_Central_Table"
            
            # Scale table
            table.scale.x = room_size[0] * 0.6
            table.scale.y = room_size[1] * 0.4
            table.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create rusty table material
            table_material = bpy.data.materials.new(name="RustVault_TableMaterial")
            table_material.use_nodes = True
            nodes = table_material.node_tree.nodes
            links = table_material.node_tree.links
            
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
            
            # Setup color ramp for rust effect
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
            table.data.materials.append(table_material)
            
            room_objects.append(table)
            
            # Create workstations around table
            station_count = 8
            for i in range(station_count):
                # Calculate position around table
                if i < 3:  # Front side
                    station_x = room_x - room_size[0] * 0.25 + i * room_size[0] * 0.25
                    station_y = room_y - room_size[1] * 0.15
                    rotation_z = 0
                elif i < 6:  # Back side
                    station_x = room_x - room_size[0] * 0.25 + (i-3) * room_size[0] * 0.25
                    station_y = room_y + room_size[1] * 0.15
                    rotation_z = math.radians(180)
                elif i == 6:  # Left side
                    station_x = room_x - room_size[0] * 0.3
                    station_y = room_y
                    rotation_z = math.radians(90)
                else:  # Right side
                    station_x = room_x + room_size[0] * 0.3
                    station_y = room_y
                    rotation_z = math.radians(270)
                
                # Create monitor
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(station_x, station_y, room_z + 1.0)
                )
                monitor = bpy.context.active_object
                monitor.name = f"RustVault_Monitor_{i}"
                
                # Edit the monitor to make it look old and worn
                bm = bmesh.from_edit_mesh(monitor.data)
                
                # Scale monitor
                for v in bm.verts:
                    v.co.x *= 0.4
                    v.co.y *= 0.05
                    v.co.z *= 0.3
                
                # Distort vertices slightly for worn look
                for v in bm.verts:
                    if random.random() > 0.8:
                        v.co.x += random.uniform(-0.02, 0.02)
                        v.co.z += random.uniform(-0.02, 0.02)
                
                # Update mesh
                bmesh.update_edit_mesh(monitor.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate monitor
                monitor.rotation_euler.z = rotation_z
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Create monitor screen material
                monitor_material = bpy.data.materials.new(name=f"RustVault_MonitorMaterial_{i}")
                monitor_material.use_nodes = True
                nodes = monitor_material.node_tree.nodes
                links = monitor_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties with random color
                r = random.uniform(0.0, 0.3)
                g = random.uniform(0.3, 0.8)
                b = random.uniform(0.0, 0.3)
                emission.inputs['Color'].default_value = (r, g, b, 1.0)
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                monitor.data.materials.append(monitor_material)
                
                room_objects.append(monitor)
                
                # Create keyboard
                keyboard_y_offset = 0.2 if rotation_z < math.radians(90) else -0.2
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(station_x, station_y + keyboard_y_offset, room_z + 0.55)
                )
                keyboard = bpy.context.active_object
                keyboard.name = f"RustVault_Keyboard_{i}"
                
                # Edit the keyboard to make it look worn
                bm = bmesh.from_edit_mesh(keyboard.data)
                
                # Scale keyboard
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.15
                    v.co.z *= 0.05
                
                # Distort vertices slightly for worn look
                for v in bm.verts:
                    if random.random() > 0.8:
                        v.co.x += random.uniform(-0.01, 0.01)
                        v.co.y += random.uniform(-0.01, 0.01)
                
                # Update mesh
                bmesh.update_edit_mesh(keyboard.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Rotate keyboard
                keyboard.rotation_euler.z = rotation_z
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                keyboard.data.materials.append(interior_materials["RustVault_Interior"])
                
                room_objects.append(keyboard)
                
                # Create chair (repurposed furniture)
                chair_y_offset = 0.4 if rotation_z < math.radians(90) else -0.4
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(station_x, station_y + chair_y_offset, room_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"RustVault_Chair_{i}"
                
                # Edit the chair to make it look makeshift and repurposed
                bm = bmesh.from_edit_mesh(chair.data)
                
                # Scale chair
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.3
                    v.co.z *= 0.3
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.6:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(chair.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Create chair material
                chair_material = bpy.data.materials.new(name=f"RustVault_ChairMaterial_{i}")
                chair_material.use_nodes = True
                nodes = chair_material.node_tree.nodes
                links = chair_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                chair.data.materials.append(chair_material)
                
                room_objects.append(chair)
            
            # Create cooling system pipes
            pipe_count = 8
            for i in range(pipe_count):
                # Calculate pipe position
                angle = i * (2 * math.pi / pipe_count)
                pipe_x = room_x + room_size[0] * 0.45 * math.cos(angle)
                pipe_y = room_y + room_size[1] * 0.45 * math.sin(angle)
                
                # Create pipe
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=0.1,
                    depth=room_size[2],
                    enter_editmode=False,
                    align='WORLD',
                    location=(pipe_x, pipe_y, room_z + room_size[2]/2)
                )
                pipe = bpy.context.active_object
                pipe.name = f"RustVault_Cooling_Pipe_{i}"
                
                # Create pipe material
                pipe_material = bpy.data.materials.new(name=f"RustVault_PipeMaterial_{i}")
                pipe_material.use_nodes = True
                nodes = pipe_material.node_tree.nodes
                links = pipe_material.node_tree.links
                
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
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.6
                
                noise.inputs['Scale'].default_value = 10.0
                noise.inputs['Detail'].default_value = 8.0
                noise.inputs['Roughness'].default_value = 0.6
                
                # Setup color ramp for rust effect
                colorramp.color_ramp.elements[0].position = 0.4
                colorramp.color_ramp.elements[0].color = (0.35, 0.2, 0.1, 1.0)  # Rust color
                colorramp.color_ramp.elements[1].position = 0.6
                colorramp.color_ramp.elements[1].color = (0.6, 0.6, 0.6, 1.0)  # Metal color
                
                # Connect nodes
                links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
                links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
                links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
                links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                pipe.data.materials.append(pipe_material)
                
                room_objects.append(pipe)
            
        elif room_name == "Server_Farm":
            # Create server farm with old repurposed servers
            
            # Create server racks
            rack_count = 6
            for i in range(rack_count):
                # Calculate rack position
                if i < 3:  # Left side
                    rack_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.3
                    rack_y = room_y - room_size[1] * 0.2
                else:  # Right side
                    rack_x = room_x - room_size[0] * 0.3 + (i-3) * room_size[0] * 0.3
                    rack_y = room_y + room_size[1] * 0.2
                
                # Create server rack
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(rack_x, rack_y, room_z + room_size[2]/2)
                )
                rack = bpy.context.active_object
                rack.name = f"RustVault_Server_Rack_{i}"
                
                # Edit the rack to make it look worn and repurposed
                bm = bmesh.from_edit_mesh(rack.data)
                
                # Scale rack
                for v in bm.verts:
                    v.co.x *= 0.5
                    v.co.y *= 0.5
                    v.co.z *= room_size[2] * 0.9
                
                # Distort vertices for worn look
                for v in bm.verts:
                    if random.random() > 0.8:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(rack.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Create rack material
                rack_material = bpy.data.materials.new(name=f"RustVault_RackMaterial_{i}")
                rack_material.use_nodes = True
                nodes = rack_material.node_tree.nodes
                links = rack_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
                principled.inputs['Metallic'].default_value = 0.7
                principled.inputs['Roughness'].default_value = 0.8
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                rack.data.materials.append(rack_material)
                
                room_objects.append(rack)
                
                # Create server units in rack
                unit_count = 8
                for j in range(unit_count):
                    unit_z = room_z + 0.2 + j * (room_size[2] * 0.8 / unit_count)
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=True,
                        align='WORLD',
                        location=(rack_x, rack_y, unit_z)
                    )
                    server = bpy.context.active_object
                    server.name = f"RustVault_Server_{i}_{j}"
                    
                    # Edit the server to make it look worn and repurposed
                    bm = bmesh.from_edit_mesh(server.data)
                    
                    # Scale server
                    for v in bm.verts:
                        v.co.x *= 0.45
                        v.co.y *= 0.45
                        v.co.z *= 0.1
                    
                    # Distort vertices for worn look
                    for v in bm.verts:
                        if random.random() > 0.8:
                            v.co.x += random.uniform(-0.02, 0.02)
                            v.co.y += random.uniform(-0.02, 0.02)
                    
                    # Update mesh
                    bmesh.update_edit_mesh(server.data)
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                    # Create server material
                    server_material = bpy.data.materials.new(name=f"RustVault_ServerMaterial_{i}_{j}")
                    server_material.use_nodes = True
                    nodes = server_material.node_tree.nodes
                    links = server_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set properties
                    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
                    principled.inputs['Metallic'].default_value = 0.5
                    principled.inputs['Roughness'].default_value = 0.7
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    server.data.materials.append(server_material)
                    
                    room_objects.append(server)
                    
                    # Create server lights
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(rack_x + 0.2, rack_y, unit_z)
                    )
                    light = bpy.context.active_object
                    light.name = f"RustVault_Server_Light_{i}_{j}"
                    
                    # Scale light
                    light.scale.x = 0.02
                    light.scale.y = 0.02
                    light.scale.z = 0.02
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create light material with random color
                    light_material = bpy.data.materials.new(name=f"RustVault_ServerLight_Material_{i}_{j}")
                    light_material.use_nodes = True
                    nodes = light_material.node_tree.nodes
                    links = light_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    emission = nodes.new(type='ShaderNodeEmission')
                    
                    # Set properties with random color
                    r = random.choice([0.0, 0.0, 1.0, 0.0])
                    g = random.choice([0.0, 1.0, 0.0, 0.0])
                    b = random.choice([1.0, 0.0, 0.0, 1.0])
                    emission.inputs['Color'].default_value = (r, g, b, 1.0)
                    emission.inputs['Strength'].default_value = 3.0
                    
                    # Connect nodes
                    links.new(emission.outputs['Emission'], output.inputs['Surface'])
                    
                    # Assign material
                    light.data.materials.append(light_material)
                    
                    room_objects.append(light)
            
            # Create cooling system
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.3)
            )
            cooling = bpy.context.active_object
            cooling.name = "RustVault_Cooling_System"
            
            # Scale cooling system
            cooling.scale.x = room_size[0] * 0.8
            cooling.scale.y = room_size[1] * 0.1
            cooling.scale.z = 0.2
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create cooling system material
            cooling_material = bpy.data.materials.new(name="RustVault_CoolingMaterial")
            cooling_material.use_nodes = True
            nodes = cooling_material.node_tree.nodes
            links = cooling_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
            principled.inputs['Metallic'].default_value = 0.8
            principled.inputs['Roughness'].default_value = 0.6
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            cooling.data.materials.append(cooling_material)
            
            room_objects.append(cooling)
            
            # Create cooling fans
            fan_count = 4
            for i in range(fan_count):
                fan_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.2
                
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.15,
                    depth=0.05,
                    enter_editmode=False,
                    align='WORLD',
                    location=(fan_x, room_y, room_z + 0.4)
                )
                fan = bpy.context.active_object
                fan.name = f"RustVault_Cooling_Fan_{i}"
                
                # Rotate fan to face upward
                fan.rotation_euler.x = math.radians(90)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                fan.data.materials.append(interior_materials["RustVault_Interior"])
                
                room_objects.append(fan)
                
                # Create fan blades
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=3,
                    radius=0.14,
                    depth=0.02,
                    enter_editmode=False,
                    align='WORLD',
                    location=(fan_x, room_y, room_z + 0.41)
                )
                blades = bpy.context.active_object
                blades.name = f"RustVault_Fan_Blades_{i}"
                
                # Rotate blades to face upward
                blades.rotation_euler.x = math.radians(90)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Create blades material
                blades_material = bpy.data.materials.new(name=f"RustVault_BladesMaterial_{i}")
                blades_material.use_nodes = True
                nodes = blades_material.node_tree.nodes
                links = blades_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
                principled.inputs['Metallic'].default_value = 0.5
                principled.inputs['Roughness'].default_value = 0.7
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                blades.data.materials.append(blades_material)
                
                room_objects.append(blades)
            
        elif room_name == "Sleeping_Area":
            # Create sleeping area with makeshift beds
            
            # Create beds
            bed_count = 6
            for i in range(bed_count):
                # Calculate bed position
                if i < 3:  # Left side
                    bed_x = room_x - room_size[0] * 0.3
                    bed_y = room_y - room_size[1] * 0.3 + i * room_size[1] * 0.3
                else:  # Right side
                    bed_x = room_x + room_size[0] * 0.3
                    bed_y = room_y - room_size[1] * 0.3 + (i-3) * room_size[1] * 0.3
                
                # Create bed base
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(bed_x, bed_y, room_z + 0.3)
                )
                bed = bpy.context.active_object
                bed.name = f"RustVault_Bed_{i}"
                
                # Edit the bed to make it look makeshift
                bm = bmesh.from_edit_mesh(bed.data)
                
                # Scale bed
                for v in bm.verts:
                    v.co.x *= 0.5
                    v.co.y *= 1.8
                    v.co.z *= 0.2
                
                # Distort vertices for makeshift look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.02, 0.02)
                
                # Update mesh
                bmesh.update_edit_mesh(bed.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Create bed material
                bed_material = bpy.data.materials.new(name=f"RustVault_BedMaterial_{i}")
                bed_material.use_nodes = True
                nodes = bed_material.node_tree.nodes
                links = bed_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.3, 1.0)  # Dark blue-gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                bed.data.materials.append(bed_material)
                
                room_objects.append(bed)
                
                # Create pillow
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(bed_x, bed_y + 0.7, room_z + 0.4)
                )
                pillow = bpy.context.active_object
                pillow.name = f"RustVault_Pillow_{i}"
                
                # Edit the pillow to make it look worn
                bm = bmesh.from_edit_mesh(pillow.data)
                
                # Scale pillow
                for v in bm.verts:
                    v.co.x *= 0.4
                    v.co.y *= 0.3
                    v.co.z *= 0.1
                
                # Distort vertices for worn look
                for v in bm.verts:
                    if random.random() > 0.5:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.02, 0.02)
                
                # Update mesh
                bmesh.update_edit_mesh(pillow.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Create pillow material
                pillow_material = bpy.data.materials.new(name=f"RustVault_PillowMaterial_{i}")
                pillow_material.use_nodes = True
                nodes = pillow_material.node_tree.nodes
                links = pillow_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.4, 1.0)  # Dark blue-gray
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                pillow.data.materials.append(pillow_material)
                
                room_objects.append(pillow)
                
                # Create blanket
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(bed_x, bed_y - 0.2, room_z + 0.35)
                )
                blanket = bpy.context.active_object
                blanket.name = f"RustVault_Blanket_{i}"
                
                # Edit the blanket to make it look worn and rumpled
                bm = bmesh.from_edit_mesh(blanket.data)
                
                # Scale blanket
                for v in bm.verts:
                    v.co.x *= 0.45
                    v.co.y *= 1.2
                    v.co.z *= 0.05
                
                # Distort vertices for rumpled look
                for v in bm.verts:
                    if random.random() > 0.3:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.03, 0.03)
                
                # Update mesh
                bmesh.update_edit_mesh(blanket.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Create blanket material with random color
                blanket_material = bpy.data.materials.new(name=f"RustVault_BlanketMaterial_{i}")
                blanket_material.use_nodes = True
                nodes = blanket_material.node_tree.nodes
                links = blanket_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set random color
                r = random.uniform(0.2, 0.4)
                g = random.uniform(0.2, 0.4)
                b = random.uniform(0.2, 0.4)
                principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                blanket.data.materials.append(blanket_material)
                
                room_objects.append(blanket)
                
                # Create personal storage box
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(bed_x, bed_y - 0.8, room_z + 0.2)
                )
                box = bpy.context.active_object
                box.name = f"RustVault_Storage_Box_{i}"
                
                # Edit the box to make it look worn
                bm = bmesh.from_edit_mesh(box.data)
                
                # Scale box
                for v in bm.verts:
                    v.co.x *= 0.4
                    v.co.y *= 0.4
                    v.co.z *= 0.2
                
                # Distort vertices for worn look
                for v in bm.verts:
                    if random.random() > 0.7:
                        v.co.x += random.uniform(-0.02, 0.02)
                        v.co.y += random.uniform(-0.02, 0.02)
                        v.co.z += random.uniform(-0.02, 0.02)
                
                # Update mesh
                bmesh.update_edit_mesh(box.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Assign material
                box.data.materials.append(interior_materials["RustVault_Interior"])
                
                room_objects.append(box)
            
            # Create central heating unit
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.3,
                depth=room_size[2] * 0.8,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + room_size[2]/2)
            )
            heater = bpy.context.active_object
            heater.name = "RustVault_Heating_Unit"
            
            # Create heater material
            heater_material = bpy.data.materials.new(name="RustVault_HeaterMaterial")
            heater_material.use_nodes = True
            nodes = heater_material.node_tree.nodes
            links = heater_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.3, 0.2, 0.2, 1.0)  # Rusty red-brown
            principled.inputs['Metallic'].default_value = 0.7
            principled.inputs['Roughness'].default_value = 0.8
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            heater.data.materials.append(heater_material)
            
            room_objects.append(heater)
            
        elif room_name == "Faraday_Cage":
            # Create Faraday cage room with metal mesh walls
            
            # Create central workstation
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            workstation = bpy.context.active_object
            workstation.name = "RustVault_Faraday_Workstation"
            
            # Scale workstation
            workstation.scale.x = room_size[0] * 0.5
            workstation.scale.y = room_size[1] * 0.5
            workstation.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            workstation.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(workstation)
            
            # Create secure terminal
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 1.0)
            )
            terminal = bpy.context.active_object
            terminal.name = "RustVault_Secure_Terminal"
            
            # Scale terminal
            terminal.scale.x = 0.5
            terminal.scale.y = 0.3
            terminal.scale.z = 0.4
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create terminal material
            terminal_material = bpy.data.materials.new(name="RustVault_TerminalMaterial")
            terminal_material.use_nodes = True
            nodes = terminal_material.node_tree.nodes
            links = terminal_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
            principled.inputs['Metallic'].default_value = 0.5
            principled.inputs['Roughness'].default_value = 0.7
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            terminal.data.materials.append(terminal_material)
            
            room_objects.append(terminal)
            
            # Create terminal screen
            bpy.ops.mesh.primitive_plane_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y - 0.15, room_z + 1.0)
            )
            screen = bpy.context.active_object
            screen.name = "RustVault_Terminal_Screen"
            
            # Scale screen
            screen.scale.x = 0.4
            screen.scale.y = 0.3
            
            # Rotate screen to face forward
            screen.rotation_euler.x = math.radians(90)
            
            # Apply transformations
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            # Create screen material
            screen_material = bpy.data.materials.new(name="RustVault_ScreenMaterial")
            screen_material.use_nodes = True
            nodes = screen_material.node_tree.nodes
            links = screen_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            emission = nodes.new(type='ShaderNodeEmission')
            
            # Set properties
            emission.inputs['Color'].default_value = (0.0, 0.5, 0.1, 1.0)  # Green
            emission.inputs['Strength'].default_value = 1.0
            
            # Connect nodes
            links.new(emission.outputs['Emission'], output.inputs['Surface'])
            
            # Assign material
            screen.data.materials.append(screen_material)
            
            room_objects.append(screen)
            
            # Create chair
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(room_x, room_y + 0.5, room_z + 0.3)
            )
            chair = bpy.context.active_object
            chair.name = "RustVault_Faraday_Chair"
            
            # Edit the chair to make it look makeshift
            bm = bmesh.from_edit_mesh(chair.data)
            
            # Scale chair
            for v in bm.verts:
                v.co.x *= 0.3
                v.co.y *= 0.3
                v.co.z *= 0.3
            
            # Distort vertices for makeshift look
            for v in bm.verts:
                if random.random() > 0.7:
                    v.co.x += random.uniform(-0.05, 0.05)
                    v.co.y += random.uniform(-0.05, 0.05)
                    v.co.z += random.uniform(-0.05, 0.05)
            
            # Update mesh
            bmesh.update_edit_mesh(chair.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Assign material
            chair.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(chair)
            
            # Create metal mesh walls (Faraday cage)
            for wall_idx in range(4):
                # Determine wall position
                if wall_idx == 0:  # Front wall
                    wall_x = room_x
                    wall_y = room_y - room_size[1]/2 + 0.05
                    wall_rot_z = 0
                    wall_width = room_size[0] * 0.9
                elif wall_idx == 1:  # Right wall
                    wall_x = room_x + room_size[0]/2 - 0.05
                    wall_y = room_y
                    wall_rot_z = math.radians(90)
                    wall_width = room_size[1] * 0.9
                elif wall_idx == 2:  # Back wall
                    wall_x = room_x
                    wall_y = room_y + room_size[1]/2 - 0.05
                    wall_rot_z = 0
                    wall_width = room_size[0] * 0.9
                else:  # Left wall
                    wall_x = room_x - room_size[0]/2 + 0.05
                    wall_y = room_y
                    wall_rot_z = math.radians(90)
                    wall_width = room_size[1] * 0.9
                
                # Create mesh wall
                bpy.ops.mesh.primitive_grid_add(
                    x_subdivisions=20,
                    y_subdivisions=20,
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(wall_x, wall_y, room_z + room_size[2]/2)
                )
                mesh_wall = bpy.context.active_object
                mesh_wall.name = f"RustVault_Faraday_Mesh_{wall_idx}"
                
                # Scale mesh wall
                mesh_wall.scale.x = wall_width
                mesh_wall.scale.y = room_size[2] * 0.9
                
                # Rotate mesh wall
                mesh_wall.rotation_euler.x = math.radians(90)
                mesh_wall.rotation_euler.z = wall_rot_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Create mesh material
                mesh_material = bpy.data.materials.new(name=f"RustVault_MeshMaterial_{wall_idx}")
                mesh_material.use_nodes = True
                nodes = mesh_material.node_tree.nodes
                links = mesh_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Light gray
                principled.inputs['Metallic'].default_value = 1.0
                principled.inputs['Roughness'].default_value = 0.3
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                mesh_wall.data.materials.append(mesh_material)
                
                room_objects.append(mesh_wall)
            
            # Create secure storage containers
            container_count = 3
            for i in range(container_count):
                container_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.3
                container_y = room_y - room_size[1] * 0.3
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(container_x, container_y, room_z + 0.3)
                )
                container = bpy.context.active_object
                container.name = f"RustVault_Secure_Container_{i}"
                
                # Scale container
                container.scale.x = 0.3
                container.scale.y = 0.3
                container.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create container material
                container_material = bpy.data.materials.new(name=f"RustVault_ContainerMaterial_{i}")
                container_material.use_nodes = True
                nodes = container_material.node_tree.nodes
                links = container_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
                principled.inputs['Metallic'].default_value = 0.9
                principled.inputs['Roughness'].default_value = 0.2
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                container.data.materials.append(container_material)
                
                room_objects.append(container)
                
                # Create keypad on container
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(container_x, container_y - 0.15, room_z + 0.3)
                )
                keypad = bpy.context.active_object
                keypad.name = f"RustVault_Container_Keypad_{i}"
                
                # Scale keypad
                keypad.scale.x = 0.1
                keypad.scale.y = 0.02
                keypad.scale.z = 0.1
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create keypad material
                keypad_material = bpy.data.materials.new(name=f"RustVault_KeypadMaterial_{i}")
                keypad_material.use_nodes = True
                nodes = keypad_material.node_tree.nodes
                links = keypad_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
                principled.inputs['Metallic'].default_value = 0.5
                principled.inputs['Roughness'].default_value = 0.7
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                keypad.data.materials.append(keypad_material)
                
                room_objects.append(keypad)
            
        elif room_name == "Kitchen":
            # Create kitchen/common area with repurposed furniture
            
            # Create central table
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            table = bpy.context.active_object
            table.name = "RustVault_Kitchen_Table"
            
            # Edit the table to make it look repurposed
            bm = bmesh.from_edit_mesh(table.data)
            
            # Scale table
            for v in bm.verts:
                v.co.x *= room_size[0] * 0.5
                v.co.y *= room_size[1] * 0.4
                v.co.z *= 1.0
            
            # Distort vertices for repurposed look
            for v in bm.verts:
                if random.random() > 0.7:
                    v.co.x += random.uniform(-0.05, 0.05)
                    v.co.y += random.uniform(-0.05, 0.05)
                    v.co.z += random.uniform(-0.05, 0.05)
            
            # Update mesh
            bmesh.update_edit_mesh(table.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Assign material
            table.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(table)
            
            # Create chairs around table
            chair_count = 6
            for i in range(chair_count):
                # Calculate chair position
                if i < 3:  # Front side
                    chair_x = room_x - room_size[0] * 0.2 + i * room_size[0] * 0.2
                    chair_y = room_y - room_size[1] * 0.25
                else:  # Back side
                    chair_x = room_x - room_size[0] * 0.2 + (i-3) * room_size[0] * 0.2
                    chair_y = room_y + room_size[1] * 0.25
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=True,
                    align='WORLD',
                    location=(chair_x, chair_y, room_z + 0.3)
                )
                chair = bpy.context.active_object
                chair.name = f"RustVault_Kitchen_Chair_{i}"
                
                # Edit the chair to make it look repurposed
                bm = bmesh.from_edit_mesh(chair.data)
                
                # Scale chair
                for v in bm.verts:
                    v.co.x *= 0.3
                    v.co.y *= 0.3
                    v.co.z *= 0.3
                
                # Distort vertices for repurposed look
                for v in bm.verts:
                    if random.random() > 0.6:
                        v.co.x += random.uniform(-0.05, 0.05)
                        v.co.y += random.uniform(-0.05, 0.05)
                        v.co.z += random.uniform(-0.05, 0.05)
                
                # Update mesh
                bmesh.update_edit_mesh(chair.data)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Create chair material with random color
                chair_material = bpy.data.materials.new(name=f"RustVault_ChairMaterial_{i}")
                chair_material.use_nodes = True
                nodes = chair_material.node_tree.nodes
                links = chair_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set random color
                r = random.uniform(0.2, 0.4)
                g = random.uniform(0.2, 0.4)
                b = random.uniform(0.2, 0.4)
                principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                chair.data.materials.append(chair_material)
                
                room_objects.append(chair)
            
            # Create kitchen counter
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x - room_size[0] * 0.3, room_y, room_z + 0.5)
            )
            counter = bpy.context.active_object
            counter.name = "RustVault_Kitchen_Counter"
            
            # Scale counter
            counter.scale.x = room_size[0] * 0.2
            counter.scale.y = room_size[1] * 0.7
            counter.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            counter.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(counter)
            
            # Create sink
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(room_x - room_size[0] * 0.3, room_y - room_size[1] * 0.2, room_z + 1.0)
            )
            sink = bpy.context.active_object
            sink.name = "RustVault_Sink"
            
            # Edit the sink
            bm = bmesh.from_edit_mesh(sink.data)
            
            # Scale sink
            for v in bm.verts:
                v.co.x *= 0.15
                v.co.y *= 0.15
                v.co.z *= 0.1
            
            # Update mesh
            bmesh.update_edit_mesh(sink.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Create sink material
            sink_material = bpy.data.materials.new(name="RustVault_SinkMaterial")
            sink_material.use_nodes = True
            nodes = sink_material.node_tree.nodes
            links = sink_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Light gray
            principled.inputs['Metallic'].default_value = 0.9
            principled.inputs['Roughness'].default_value = 0.4
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            sink.data.materials.append(sink_material)
            
            room_objects.append(sink)
            
            # Create faucet
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.02,
                depth=0.2,
                enter_editmode=False,
                align='WORLD',
                location=(room_x - room_size[0] * 0.3, room_y - room_size[1] * 0.2, room_z + 1.15)
            )
            faucet = bpy.context.active_object
            faucet.name = "RustVault_Faucet"
            
            # Rotate faucet
            faucet.rotation_euler.x = math.radians(90)
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            faucet.data.materials.append(sink_material)
            
            room_objects.append(faucet)
            
            # Create cooking equipment
            for i in range(3):
                equipment_x = room_x - room_size[0] * 0.3
                equipment_y = room_y + room_size[1] * (0.1 + i * 0.15)
                
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.15,
                    depth=0.1,
                    enter_editmode=False,
                    align='WORLD',
                    location=(equipment_x, equipment_y, room_z + 1.0)
                )
                equipment = bpy.context.active_object
                equipment.name = f"RustVault_Cooking_Equipment_{i}"
                
                # Create equipment material
                equipment_material = bpy.data.materials.new(name=f"RustVault_EquipmentMaterial_{i}")
                equipment_material.use_nodes = True
                nodes = equipment_material.node_tree.nodes
                links = equipment_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.4
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                equipment.data.materials.append(equipment_material)
                
                room_objects.append(equipment)
            
            # Create food storage shelves
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x + room_size[0] * 0.3, room_y, room_z + 1.0)
            )
            shelves = bpy.context.active_object
            shelves.name = "RustVault_Food_Shelves"
            
            # Scale shelves
            shelves.scale.x = room_size[0] * 0.2
            shelves.scale.y = room_size[1] * 0.7
            shelves.scale.z = 2.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            shelves.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(shelves)
            
            # Create food containers on shelves
            container_count = 12
            for i in range(container_count):
                shelf_level = i // 4
                shelf_position = i % 4
                
                container_x = room_x + room_size[0] * 0.3
                container_y = room_y - room_size[1] * 0.3 + shelf_position * room_size[1] * 0.2
                container_z = room_z + 0.3 + shelf_level * 0.6
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(container_x, container_y, container_z)
                )
                container = bpy.context.active_object
                container.name = f"RustVault_Food_Container_{i}"
                
                # Scale container
                container.scale.x = 0.15
                container.scale.y = 0.15
                container.scale.z = 0.15
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create container material with random color
                container_material = bpy.data.materials.new(name=f"RustVault_ContainerMaterial_{i}")
                container_material.use_nodes = True
                nodes = container_material.node_tree.nodes
                links = container_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set random color
                r = random.uniform(0.2, 0.8)
                g = random.uniform(0.2, 0.8)
                b = random.uniform(0.2, 0.8)
                principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                container.data.materials.append(container_material)
                
                room_objects.append(container)
    
    # Create connecting corridors between rooms
    corridor_data = [
        {
            "start": "Main_Room",
            "end": "Server_Farm",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Main_Room",
            "end": "Sleeping_Area",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Main_Room",
            "end": "Faraday_Cage",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        },
        {
            "start": "Main_Room",
            "end": "Kitchen",
            "width": building_size.x * 0.1,
            "height": building_size.z * 0.2
        }
    ]
    
    # Find room positions
    room_positions = {}
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.3
        
        room_positions[room_name] = (room_x, room_y, room_z)
    
    # Create corridors
    for corridor in corridor_data:
        start_name = corridor["start"]
        end_name = corridor["end"]
        corridor_width = corridor["width"]
        corridor_height = corridor["height"]
        
        if start_name in room_positions and end_name in room_positions:
            start_pos = room_positions[start_name]
            end_pos = room_positions[end_name]
            
            # Calculate corridor direction and length
            direction = Vector((end_pos[0], end_pos[1], 0)) - Vector((start_pos[0], start_pos[1], 0))
            length = direction.length
            direction.normalize()
            
            # Create corridor
            corridor_x = (start_pos[0] + end_pos[0]) / 2
            corridor_y = (start_pos[1] + end_pos[1]) / 2
            corridor_z = start_pos[2]  # Use start room's z position
            
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=True,
                align='WORLD',
                location=(corridor_x, corridor_y, corridor_z + corridor_height/2)
            )
            corridor_obj = bpy.context.active_object
            corridor_obj.name = f"RustVault_Corridor_{start_name}_to_{end_name}"
            
            # Edit the corridor to make it look worn
            bm = bmesh.from_edit_mesh(corridor_obj.data)
            
            # Scale corridor
            for v in bm.verts:
                v.co.x *= length
                v.co.y *= corridor_width
                v.co.z *= corridor_height
            
            # Distort vertices for worn look
            for v in bm.verts:
                if random.random() > 0.8:
                    v.co.y += random.uniform(-0.05, 0.05)
                    v.co.z += random.uniform(-0.05, 0.05)
            
            # Update mesh
            bmesh.update_edit_mesh(corridor_obj.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Rotate corridor to point from start to end
            corridor_obj.rotation_euler.z = math.atan2(direction.y, direction.x)
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            corridor_obj.data.materials.append(interior_materials["RustVault_Interior"])
            
            room_objects.append(corridor_obj)
    
    # Move all objects to the rooms collection
    for obj in room_objects:
        if obj.name not in rooms_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
    
    return rooms_collection


def create_militech_armory_rooms(militech_objects, materials, interior_materials):
    """Create rooms for Militech Armory (Upper Tier corporate weapons manufacturer)
	Neon Crucible - Militech Armory Rooms Implementation
	Blender 4.2 Python Script for generating rooms per floor for the Militech Armory building
	in the Neon Crucible cyberpunk world.
	"""
    # Extract objects from the militech_objects dictionary
    building = militech_objects.get("building")
    collection = militech_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Militech Armory objects")
        return None
    
    # Create a subcollection for room objects
    if "MilitechArmory_Rooms" not in bpy.data.collections:
        rooms_collection = bpy.data.collections.new("MilitechArmory_Rooms")
        collection.children.link(rooms_collection)
    else:
        rooms_collection = bpy.data.collections["MilitechArmory_Rooms"]
    
    room_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Define room positions relative to building center
    rooms_data = [
        {
            "name": "Security_Lobby",
            "position": (0, 0, 0),
            "size": (building_size.x * 0.7, building_size.y * 0.7, building_size.z * 0.15),
            "floor_level": 0
        },
        {
            "name": "Showroom",
            "position": (0, 0, 0),
            "size": (building_size.x * 0.7, building_size.y * 0.7, building_size.z * 0.15),
            "floor_level": 1
        },
        {
            "name": "Testing_Range",
            "position": (building_size.x * 0.3, 0, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.8, building_size.z * 0.15),
            "floor_level": 2
        },
        {
            "name": "RD_Lab",
            "position": (-building_size.x * 0.3, 0, 0),
            "size": (building_size.x * 0.4, building_size.y * 0.8, building_size.z * 0.15),
            "floor_level": 2
        },
        {
            "name": "Secure_Vault",
            "position": (0, -building_size.y * 0.3, 0),
            "size": (building_size.x * 0.5, building_size.y * 0.4, building_size.z * 0.15),
            "floor_level": 3
        },
        {
            "name": "Executive_Office",
            "position": (0, building_size.y * 0.3, 0),
            "size": (building_size.x * 0.5, building_size.y * 0.4, building_size.z * 0.15),
            "floor_level": 3
        }
    ]
    
    # Create each room
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        room_size = room_data["size"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.2
        
        # Create room floor
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(room_x, room_y, room_z)
        )
        floor = bpy.context.active_object
        floor.name = f"MilitechArmory_{room_name}_Floor"
        
        # Scale floor
        floor.scale.x = room_size[0]
        floor.scale.y = room_size[1]
        floor.scale.z = 0.1
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        floor.data.materials.append(interior_materials["Militech_Interior"])
        
        room_objects.append(floor)
        
        # Create room ceiling
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(room_x, room_y, room_z + room_size[2])
        )
        ceiling = bpy.context.active_object
        ceiling.name = f"MilitechArmory_{room_name}_Ceiling"
        
        # Scale ceiling
        ceiling.scale.x = room_size[0]
        ceiling.scale.y = room_size[1]
        ceiling.scale.z = 0.1
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        ceiling.data.materials.append(interior_materials["Militech_Interior"])
        
        room_objects.append(ceiling)
        
        # Create room walls
        for wall_idx in range(4):
            # Determine wall position
            if wall_idx == 0:  # Front wall
                wall_x = room_x
                wall_y = room_y - room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            elif wall_idx == 1:  # Right wall
                wall_x = room_x + room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            elif wall_idx == 2:  # Back wall
                wall_x = room_x
                wall_y = room_y + room_size[1]/2
                wall_rot_z = 0
                wall_width = room_size[0]
            else:  # Left wall
                wall_x = room_x - room_size[0]/2
                wall_y = room_y
                wall_rot_z = math.radians(90)
                wall_width = room_size[1]
            
            # Create wall
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(wall_x, wall_y, room_z + room_size[2]/2)
            )
            wall = bpy.context.active_object
            wall.name = f"MilitechArmory_{room_name}_Wall_{wall_idx}"
            
            # Scale wall
            wall.scale.x = wall_width
            wall.scale.y = 0.1
            wall.scale.z = room_size[2]
            
            # Rotate wall
            wall.rotation_euler.z = wall_rot_z
            
            # Apply transformations
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            # Assign material
            wall.data.materials.append(interior_materials["Militech_Interior"])
            
            room_objects.append(wall)
        
        # Add room-specific elements
        if room_name == "Security_Lobby":
            # Create reception desk
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y - room_size[1] * 0.2, room_z + 0.5)
            )
            desk = bpy.context.active_object
            desk.name = "MilitechArmory_Reception_Desk"
            
            # Scale desk
            desk.scale.x = room_size[0] * 0.4
            desk.scale.y = room_size[1] * 0.1
            desk.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            desk.data.materials.append(interior_materials["Militech_Interior"])
            
            room_objects.append(desk)
            
            # Create security scanners
            for i in range(2):
                scanner_x = room_x - room_size[0] * 0.15 + i * room_size[0] * 0.3
                scanner_y = room_y
                
                # Create scanner base
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(scanner_x, scanner_y, room_z + 0.1)
                )
                scanner_base = bpy.context.active_object
                scanner_base.name = f"MilitechArmory_Scanner_Base_{i}"
                
                # Scale scanner base
                scanner_base.scale.x = 0.5
                scanner_base.scale.y = 0.5
                scanner_base.scale.z = 0.1
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                scanner_base.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(scanner_base)
                
                # Create scanner arch
                bpy.ops.mesh.primitive_torus_add(
                    major_radius=1.0,
                    minor_radius=0.1,
                    major_segments=16,
                    minor_segments=8,
                    align='WORLD',
                    location=(scanner_x, scanner_y, room_z + 1.5)
                )
                scanner_arch = bpy.context.active_object
                scanner_arch.name = f"MilitechArmory_Scanner_Arch_{i}"
                
                # Scale scanner arch
                scanner_arch.scale.x = 0.5
                scanner_arch.scale.y = 0.5
                scanner_arch.scale.z = 1.5
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create scanner material
                scanner_material = bpy.data.materials.new(name=f"MilitechArmory_ScannerMaterial_{i}")
                scanner_material.use_nodes = True
                nodes = scanner_material.node_tree.nodes
                links = scanner_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.2
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                scanner_arch.data.materials.append(scanner_material)
                
                room_objects.append(scanner_arch)
            
            # Create security guards
            for i in range(2):
                guard_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.6
                guard_y = room_y - room_size[1] * 0.3
                
                # Create guard body
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(guard_x, guard_y, room_z + 1.0)
                )
                guard = bpy.context.active_object
                guard.name = f"MilitechArmory_Guard_{i}"
                
                # Scale guard
                guard.scale.x = 0.4
                guard.scale.y = 0.4
                guard.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create guard material
                guard_material = bpy.data.materials.new(name=f"MilitechArmory_GuardMaterial_{i}")
                guard_material.use_nodes = True
                nodes = guard_material.node_tree.nodes
                links = guard_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Black
                principled.inputs['Roughness'].default_value = 0.7
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                guard.data.materials.append(guard_material)
                
                room_objects.append(guard)
                
                # Create guard head
                bpy.ops.mesh.primitive_uv_sphere_add(
                    radius=0.2,
                    align='WORLD',
                    location=(guard_x, guard_y, room_z + 1.8)
                )
                head = bpy.context.active_object
                head.name = f"MilitechArmory_Guard_Head_{i}"
                
                # Assign material
                head.data.materials.append(guard_material)
                
                room_objects.append(head)
            
            # Create security cameras
            for i in range(4):
                angle = i * (math.pi / 2)
                camera_x = room_x + room_size[0] * 0.45 * math.cos(angle)
                camera_y = room_y + room_size[1] * 0.45 * math.sin(angle)
                
                # Create camera base
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=0.1,
                    depth=0.2,
                    align='WORLD',
                    location=(camera_x, camera_y, room_z + room_size[2] - 0.1)
                )
                camera_base = bpy.context.active_object
                camera_base.name = f"MilitechArmory_Camera_Base_{i}"
                
                # Assign material
                camera_base.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(camera_base)
                
                # Create camera body
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=0.05,
                    depth=0.3,
                    align='WORLD',
                    location=(camera_x, camera_y, room_z + room_size[2] - 0.25)
                )
                camera_body = bpy.context.active_object
                camera_body.name = f"MilitechArmory_Camera_Body_{i}"
                
                # Rotate camera to point toward center
                direction = Vector((room_x, room_y, 0)) - Vector((camera_x, camera_y, 0))
                rot_angle = math.atan2(direction.y, direction.x)
                camera_body.rotation_euler.z = rot_angle
                camera_body.rotation_euler.x = math.radians(45)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                camera_body.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(camera_body)
                
                # Create camera lens
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.03,
                    depth=0.05,
                    align='WORLD',
                    location=(camera_x + 0.15 * math.cos(rot_angle), 
                              camera_y + 0.15 * math.sin(rot_angle), 
                              room_z + room_size[2] - 0.35)
                )
                camera_lens = bpy.context.active_object
                camera_lens.name = f"MilitechArmory_Camera_Lens_{i}"
                
                # Rotate lens to match body
                camera_lens.rotation_euler.z = rot_angle
                camera_lens.rotation_euler.x = math.radians(45)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Create lens material
                lens_material = bpy.data.materials.new(name=f"MilitechArmory_LensMaterial_{i}")
                lens_material.use_nodes = True
                nodes = lens_material.node_tree.nodes
                links = lens_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)  # Black
                principled.inputs['Metallic'].default_value = 0.0
                principled.inputs['Roughness'].default_value = 0.0
                principled.inputs['IOR'].default_value = 2.0
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                camera_lens.data.materials.append(lens_material)
                
                room_objects.append(camera_lens)
            
            # Create waiting area
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x + room_size[0] * 0.3, room_y + room_size[1] * 0.3, room_z + 0.3)
            )
            waiting_area = bpy.context.active_object
            waiting_area.name = "MilitechArmory_Waiting_Area"
            
            # Scale waiting area
            waiting_area.scale.x = room_size[0] * 0.2
            waiting_area.scale.y = room_size[1] * 0.2
            waiting_area.scale.z = 0.3
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            waiting_area.data.materials.append(interior_materials["Militech_Interior"])
            
            room_objects.append(waiting_area)
            
            # Create chairs in waiting area
            for i in range(4):
                chair_x = room_x + room_size[0] * (0.25 + (i % 2) * 0.1)
                chair_y = room_y + room_size[1] * (0.25 + (i // 2) * 0.1)
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(chair_x, chair_y, room_z + 0.5)
                )
                chair = bpy.context.active_object
                chair.name = f"MilitechArmory_Waiting_Chair_{i}"
                
                # Scale chair
                chair.scale.x = 0.3
                chair.scale.y = 0.3
                chair.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                chair.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(chair)
            
        elif room_name == "Showroom":
            # Create central display platform
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=32,
                radius=room_size[0] * 0.2,
                depth=0.5,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.25)
            )
            platform = bpy.context.active_object
            platform.name = "MilitechArmory_Display_Platform"
            
            # Create platform material
            platform_material = bpy.data.materials.new(name="MilitechArmory_PlatformMaterial")
            platform_material.use_nodes = True
            nodes = platform_material.node_tree.nodes
            links = platform_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
            principled.inputs['Metallic'].default_value = 0.8
            principled.inputs['Roughness'].default_value = 0.2
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            platform.data.materials.append(platform_material)
            
            room_objects.append(platform)
            
            # Create featured weapon on platform
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 1.0)
            )
            featured_weapon = bpy.context.active_object
            featured_weapon.name = "MilitechArmory_Featured_Weapon"
            
            # Scale weapon
            featured_weapon.scale.x = 1.5
            featured_weapon.scale.y = 0.3
            featured_weapon.scale.z = 0.3
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create weapon material
            weapon_material = bpy.data.materials.new(name="MilitechArmory_WeaponMaterial")
            weapon_material.use_nodes = True
            nodes = weapon_material.node_tree.nodes
            links = weapon_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Black
            principled.inputs['Metallic'].default_value = 0.9
            principled.inputs['Roughness'].default_value = 0.1
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            featured_weapon.data.materials.append(weapon_material)
            
            room_objects.append(featured_weapon)
            
            # Create weapon details
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=0.1,
                depth=1.0,
                align='WORLD',
                location=(room_x - 0.5, room_y, room_z + 1.0)
            )
            weapon_barrel = bpy.context.active_object
            weapon_barrel.name = "MilitechArmory_Weapon_Barrel"
            
            # Rotate barrel
            weapon_barrel.rotation_euler.x = math.radians(90)
            
            # Apply rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            
            # Assign material
            weapon_barrel.data.materials.append(weapon_material)
            
            room_objects.append(weapon_barrel)
            
            # Create weapon display cases around the room
            case_count = 8
            for i in range(case_count):
                angle = i * (2 * math.pi / case_count)
                case_x = room_x + room_size[0] * 0.4 * math.cos(angle)
                case_y = room_y + room_size[1] * 0.4 * math.sin(angle)
                
                # Create display case
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(case_x, case_y, room_z + 0.5)
                )
                case = bpy.context.active_object
                case.name = f"MilitechArmory_Display_Case_{i}"
                
                # Scale case
                case.scale.x = 0.8
                case.scale.y = 0.8
                case.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create case material
                case_material = bpy.data.materials.new(name=f"MilitechArmory_CaseMaterial_{i}")
                case_material.use_nodes = True
                nodes = case_material.node_tree.nodes
                links = case_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.2
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                case.data.materials.append(case_material)
                
                room_objects.append(case)
                
                # Create weapon in case
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(case_x, case_y, room_z + 1.0)
                )
                weapon = bpy.context.active_object
                weapon.name = f"MilitechArmory_Weapon_{i}"
                
                # Scale weapon
                weapon.scale.x = 0.7
                weapon.scale.y = 0.2
                weapon.scale.z = 0.2
                
                # Rotate weapon to face center
                direction = Vector((room_x, room_y, 0)) - Vector((case_x, case_y, 0))
                rot_angle = math.atan2(direction.y, direction.x)
                weapon.rotation_euler.z = rot_angle
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                weapon.data.materials.append(weapon_material)
                
                room_objects.append(weapon)
            
            # Create holographic displays
            for i in range(4):
                holo_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.2
                holo_y = room_y - room_size[1] * 0.4
                
                bpy.ops.mesh.primitive_plane_add(
                    size=1.0,
                    align='WORLD',
                    location=(holo_x, holo_y, room_z + 1.5)
                )
                holo = bpy.context.active_object
                holo.name = f"MilitechArmory_Holographic_Display_{i}"
                
                # Scale hologram
                holo.scale.x = 0.5
                holo.scale.y = 1.0
                
                # Rotate hologram to be vertical
                holo.rotation_euler.x = math.radians(90)
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Create hologram material
                holo_material = bpy.data.materials.new(name=f"MilitechArmory_HoloMaterial_{i}")
                holo_material.use_nodes = True
                nodes = holo_material.node_tree.nodes
                links = holo_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties
                emission.inputs['Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                holo.data.materials.append(holo_material)
                
                room_objects.append(holo)
            
        elif room_name == "Testing_Range":
            # Create shooting lanes
            lane_count = 5
            for i in range(lane_count):
                lane_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.15
                lane_y = room_y
                
                # Create lane divider
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(lane_x, lane_y, room_z + room_size[2]/2)
                )
                divider = bpy.context.active_object
                divider.name = f"MilitechArmory_Lane_Divider_{i}"
                
                # Scale divider
                divider.scale.x = 0.1
                divider.scale.y = room_size[1] * 0.8
                divider.scale.z = room_size[2] * 0.8
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                divider.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(divider)
                
                # Create shooting position
                if i < lane_count - 1:
                    position_x = lane_x + room_size[0] * 0.075
                    position_y = room_y - room_size[1] * 0.35
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(position_x, position_y, room_z + 0.5)
                    )
                    position = bpy.context.active_object
                    position.name = f"MilitechArmory_Shooting_Position_{i}"
                    
                    # Scale position
                    position.scale.x = room_size[0] * 0.07
                    position.scale.y = room_size[1] * 0.05
                    position.scale.z = 0.5
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    position.data.materials.append(interior_materials["Militech_Interior"])
                    
                    room_objects.append(position)
                    
                    # Create weapon rest
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(position_x, position_y - 0.3, room_z + 1.0)
                    )
                    rest = bpy.context.active_object
                    rest.name = f"MilitechArmory_Weapon_Rest_{i}"
                    
                    # Scale rest
                    rest.scale.x = room_size[0] * 0.05
                    rest.scale.y = room_size[1] * 0.02
                    rest.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    rest.data.materials.append(interior_materials["Militech_Interior"])
                    
                    room_objects.append(rest)
                    
                    # Create test weapon
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(position_x, position_y - 0.3, room_z + 1.1)
                    )
                    weapon = bpy.context.active_object
                    weapon.name = f"MilitechArmory_Test_Weapon_{i}"
                    
                    # Scale weapon
                    weapon.scale.x = 0.7
                    weapon.scale.y = 0.2
                    weapon.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create weapon material
                    weapon_material = bpy.data.materials.new(name=f"MilitechArmory_TestWeaponMaterial_{i}")
                    weapon_material.use_nodes = True
                    nodes = weapon_material.node_tree.nodes
                    links = weapon_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set properties
                    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Black
                    principled.inputs['Metallic'].default_value = 0.9
                    principled.inputs['Roughness'].default_value = 0.1
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    weapon.data.materials.append(weapon_material)
                    
                    room_objects.append(weapon)
            
            # Create targets at the end of the range
            for i in range(lane_count - 1):
                target_x = room_x - room_size[0] * 0.225 + i * room_size[0] * 0.15
                target_y = room_y + room_size[1] * 0.35
                
                # Create target base
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(target_x, target_y, room_z + 0.5)
                )
                target_base = bpy.context.active_object
                target_base.name = f"MilitechArmory_Target_Base_{i}"
                
                # Scale target base
                target_base.scale.x = 0.1
                target_base.scale.y = 0.1
                target_base.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                target_base.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(target_base)
                
                # Create target
                bpy.ops.mesh.primitive_circle_add(
                    vertices=32,
                    radius=0.5,
                    fill_type='NGON',
                    align='WORLD',
                    location=(target_x, target_y, room_z + 1.5)
                )
                target = bpy.context.active_object
                target.name = f"MilitechArmory_Target_{i}"
                
                # Create target material
                target_material = bpy.data.materials.new(name=f"MilitechArmory_TargetMaterial_{i}")
                target_material.use_nodes = True
                nodes = target_material.node_tree.nodes
                links = target_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                target.data.materials.append(target_material)
                
                room_objects.append(target)
                
                # Create target rings
                for j in range(3):
                    ring_radius = 0.4 - j * 0.1
                    
                    bpy.ops.mesh.primitive_circle_add(
                        vertices=32,
                        radius=ring_radius,
                        fill_type='NGON',
                        align='WORLD',
                        location=(target_x, target_y, room_z + 1.51)
                    )
                    ring = bpy.context.active_object
                    ring.name = f"MilitechArmory_Target_Ring_{i}_{j}"
                    
                    # Create ring material
                    ring_material = bpy.data.materials.new(name=f"MilitechArmory_RingMaterial_{i}_{j}")
                    ring_material.use_nodes = True
                    nodes = ring_material.node_tree.nodes
                    links = ring_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set properties
                    if j % 2 == 0:
                        principled.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)  # Black
                    else:
                        principled.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # White
                    principled.inputs['Roughness'].default_value = 0.9
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    ring.data.materials.append(ring_material)
                    
                    room_objects.append(ring)
            
            # Create control room
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y - room_size[1] * 0.45, room_z + room_size[2]/2)
            )
            control_room = bpy.context.active_object
            control_room.name = "MilitechArmory_Control_Room"
            
            # Scale control room
            control_room.scale.x = room_size[0] * 0.3
            control_room.scale.y = room_size[1] * 0.05
            control_room.scale.z = room_size[2] * 0.8
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            control_room.data.materials.append(interior_materials["Militech_Interior"])
            
            room_objects.append(control_room)
            
            # Create control room window
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y - room_size[1] * 0.4, room_z + room_size[2]/2)
            )
            window = bpy.context.active_object
            window.name = "MilitechArmory_Control_Window"
            
            # Scale window
            window.scale.x = room_size[0] * 0.28
            window.scale.y = 0.05
            window.scale.z = room_size[2] * 0.4
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create window material
            window_material = bpy.data.materials.new(name="MilitechArmory_WindowMaterial")
            window_material.use_nodes = True
            nodes = window_material.node_tree.nodes
            links = window_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 0.2)  # Red tint
            principled.inputs['Metallic'].default_value = 0.0
            principled.inputs['Roughness'].default_value = 0.0
            principled.inputs['IOR'].default_value = 1.45
            principled.inputs['Transmission'].default_value = 0.9
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            window.data.materials.append(window_material)
            
            room_objects.append(window)
            
        elif room_name == "RD_Lab":
            # Create central workbench
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            workbench = bpy.context.active_object
            workbench.name = "MilitechArmory_RD_Workbench"
            
            # Scale workbench
            workbench.scale.x = room_size[0] * 0.7
            workbench.scale.y = room_size[1] * 0.4
            workbench.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            workbench.data.materials.append(interior_materials["Militech_Interior"])
            
            room_objects.append(workbench)
            
            # Create prototype weapons on workbench
            for i in range(3):
                prototype_x = room_x - room_size[0] * 0.2 + i * room_size[0] * 0.2
                prototype_y = room_y
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(prototype_x, prototype_y, room_z + 1.0)
                )
                prototype = bpy.context.active_object
                prototype.name = f"MilitechArmory_Prototype_{i}"
                
                # Scale prototype
                prototype.scale.x = 0.8
                prototype.scale.y = 0.3
                prototype.scale.z = 0.2
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create prototype material
                prototype_material = bpy.data.materials.new(name=f"MilitechArmory_PrototypeMaterial_{i}")
                prototype_material.use_nodes = True
                nodes = prototype_material.node_tree.nodes
                links = prototype_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Light gray
                principled.inputs['Metallic'].default_value = 0.9
                principled.inputs['Roughness'].default_value = 0.1
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                prototype.data.materials.append(prototype_material)
                
                room_objects.append(prototype)
                
                # Create prototype parts
                parts_count = random.randint(3, 5)
                for j in range(parts_count):
                    part_x = prototype_x + random.uniform(-0.4, 0.4)
                    part_y = prototype_y + random.uniform(-0.2, 0.2)
                    
                    # Randomize part shape
                    if random.random() > 0.5:
                        bpy.ops.mesh.primitive_cube_add(
                            size=random.uniform(0.1, 0.2),
                            align='WORLD',
                            location=(part_x, part_y, room_z + 1.1)
                        )
                    else:
                        bpy.ops.mesh.primitive_cylinder_add(
                            vertices=8,
                            radius=random.uniform(0.05, 0.1),
                            depth=random.uniform(0.1, 0.3),
                            align='WORLD',
                            location=(part_x, part_y, room_z + 1.1)
                        )
                    
                    part = bpy.context.active_object
                    part.name = f"MilitechArmory_Prototype_Part_{i}_{j}"
                    
                    # Assign material
                    part.data.materials.append(prototype_material)
                    
                    room_objects.append(part)
            
            # Create equipment around the lab
            equipment_types = ["3D_Printer", "Scanner", "Computer", "Testing_Rig"]
            for i, eq_type in enumerate(equipment_types):
                if i < 2:
                    eq_x = room_x - room_size[0] * 0.3
                    eq_y = room_y - room_size[1] * 0.3 + i * room_size[1] * 0.6
                else:
                    eq_x = room_x + room_size[0] * 0.3
                    eq_y = room_y - room_size[1] * 0.3 + (i-2) * room_size[1] * 0.6
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(eq_x, eq_y, room_z + 0.5)
                )
                equipment = bpy.context.active_object
                equipment.name = f"MilitechArmory_{eq_type}"
                
                # Scale equipment
                equipment.scale.x = 0.8
                equipment.scale.y = 0.8
                equipment.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create equipment material
                equipment_material = bpy.data.materials.new(name=f"MilitechArmory_{eq_type}Material")
                equipment_material.use_nodes = True
                nodes = equipment_material.node_tree.nodes
                links = equipment_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.2
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                equipment.data.materials.append(equipment_material)
                
                room_objects.append(equipment)
                
                # Create equipment details
                if eq_type == "3D_Printer":
                    # Create printer head
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(eq_x, eq_y, room_z + 1.0)
                    )
                    printer_head = bpy.context.active_object
                    printer_head.name = "MilitechArmory_Printer_Head"
                    
                    # Scale printer head
                    printer_head.scale.x = 0.2
                    printer_head.scale.y = 0.2
                    printer_head.scale.z = 0.2
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    printer_head.data.materials.append(equipment_material)
                    
                    room_objects.append(printer_head)
                    
                    # Create printing platform
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(eq_x, eq_y, room_z + 0.7)
                    )
                    platform = bpy.context.active_object
                    platform.name = "MilitechArmory_Printing_Platform"
                    
                    # Scale platform
                    platform.scale.x = 0.6
                    platform.scale.y = 0.6
                    platform.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    platform.data.materials.append(equipment_material)
                    
                    room_objects.append(platform)
                
                elif eq_type == "Scanner":
                    # Create scanner arm
                    bpy.ops.mesh.primitive_cylinder_add(
                        vertices=8,
                        radius=0.1,
                        depth=1.0,
                        align='WORLD',
                        location=(eq_x, eq_y, room_z + 1.0)
                    )
                    scanner_arm = bpy.context.active_object
                    scanner_arm.name = "MilitechArmory_Scanner_Arm"
                    
                    # Rotate arm
                    scanner_arm.rotation_euler.x = math.radians(90)
                    
                    # Apply rotation
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                    
                    # Assign material
                    scanner_arm.data.materials.append(equipment_material)
                    
                    room_objects.append(scanner_arm)
                    
                    # Create scanner head
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(eq_x, eq_y + 0.5, room_z + 1.0)
                    )
                    scanner_head = bpy.context.active_object
                    scanner_head.name = "MilitechArmory_Scanner_Head"
                    
                    # Scale scanner head
                    scanner_head.scale.x = 0.3
                    scanner_head.scale.y = 0.1
                    scanner_head.scale.z = 0.2
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    scanner_head.data.materials.append(equipment_material)
                    
                    room_objects.append(scanner_head)
                
                elif eq_type == "Computer":
                    # Create monitor
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(eq_x, eq_y, room_z + 1.0)
                    )
                    monitor = bpy.context.active_object
                    monitor.name = "MilitechArmory_Computer_Monitor"
                    
                    # Scale monitor
                    monitor.scale.x = 0.6
                    monitor.scale.y = 0.1
                    monitor.scale.z = 0.4
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create monitor screen material
                    screen_material = bpy.data.materials.new(name="MilitechArmory_ScreenMaterial")
                    screen_material.use_nodes = True
                    nodes = screen_material.node_tree.nodes
                    links = screen_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    emission = nodes.new(type='ShaderNodeEmission')
                    
                    # Set properties
                    emission.inputs['Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
                    emission.inputs['Strength'].default_value = 1.0
                    
                    # Connect nodes
                    links.new(emission.outputs['Emission'], output.inputs['Surface'])
                    
                    # Assign material
                    monitor.data.materials.append(screen_material)
                    
                    room_objects.append(monitor)
                    
                    # Create keyboard
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(eq_x, eq_y + 0.3, room_z + 0.6)
                    )
                    keyboard = bpy.context.active_object
                    keyboard.name = "MilitechArmory_Computer_Keyboard"
                    
                    # Scale keyboard
                    keyboard.scale.x = 0.4
                    keyboard.scale.y = 0.2
                    keyboard.scale.z = 0.05
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    keyboard.data.materials.append(equipment_material)
                    
                    room_objects.append(keyboard)
                
                elif eq_type == "Testing_Rig":
                    # Create testing platform
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(eq_x, eq_y, room_z + 0.7)
                    )
                    test_platform = bpy.context.active_object
                    test_platform.name = "MilitechArmory_Testing_Platform"
                    
                    # Scale platform
                    test_platform.scale.x = 0.6
                    test_platform.scale.y = 0.6
                    test_platform.scale.z = 0.1
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Assign material
                    test_platform.data.materials.append(equipment_material)
                    
                    room_objects.append(test_platform)
                    
                    # Create testing arms
                    for j in range(2):
                        arm_x = eq_x
                        arm_y = eq_y - 0.3 + j * 0.6
                        
                        bpy.ops.mesh.primitive_cylinder_add(
                            vertices=8,
                            radius=0.05,
                            depth=0.8,
                            align='WORLD',
                            location=(arm_x, arm_y, room_z + 1.1)
                        )
                        arm = bpy.context.active_object
                        arm.name = f"MilitechArmory_Testing_Arm_{j}"
                        
                        # Assign material
                        arm.data.materials.append(equipment_material)
                        
                        room_objects.append(arm)
                        
                        # Create arm tool
                        bpy.ops.mesh.primitive_cube_add(
                            size=1.0,
                            enter_editmode=False,
                            align='WORLD',
                            location=(arm_x, arm_y, room_z + 0.8)
                        )
                        tool = bpy.context.active_object
                        tool.name = f"MilitechArmory_Testing_Tool_{j}"
                        
                        # Scale tool
                        tool.scale.x = 0.1
                        tool.scale.y = 0.1
                        tool.scale.z = 0.1
                        
                        # Apply scale
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        
                        # Assign material
                        tool.data.materials.append(equipment_material)
                        
                        room_objects.append(tool)
            
            # Create scientists
            for i in range(2):
                scientist_x = room_x - room_size[0] * 0.2 + i * room_size[0] * 0.4
                scientist_y = room_y - room_size[1] * 0.1
                
                # Create scientist body
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(scientist_x, scientist_y, room_z + 1.0)
                )
                scientist = bpy.context.active_object
                scientist.name = f"MilitechArmory_Scientist_{i}"
                
                # Scale scientist
                scientist.scale.x = 0.3
                scientist.scale.y = 0.3
                scientist.scale.z = 0.8
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create scientist material
                scientist_material = bpy.data.materials.new(name=f"MilitechArmory_ScientistMaterial_{i}")
                scientist_material.use_nodes = True
                nodes = scientist_material.node_tree.nodes
                links = scientist_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # White lab coat
                principled.inputs['Roughness'].default_value = 0.9
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                scientist.data.materials.append(scientist_material)
                
                room_objects.append(scientist)
                
                # Create scientist head
                bpy.ops.mesh.primitive_uv_sphere_add(
                    radius=0.15,
                    align='WORLD',
                    location=(scientist_x, scientist_y, room_z + 1.8)
                )
                head = bpy.context.active_object
                head.name = f"MilitechArmory_Scientist_Head_{i}"
                
                # Create head material
                head_material = bpy.data.materials.new(name=f"MilitechArmory_HeadMaterial_{i}")
                head_material.use_nodes = True
                nodes = head_material.node_tree.nodes
                links = head_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.8, 0.6, 0.5, 1.0)  # Skin tone
                principled.inputs['Roughness'].default_value = 0.7
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                head.data.materials.append(head_material)
                
                room_objects.append(head)
            
        elif room_name == "Secure_Vault":
            # Create central weapon storage
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 1.0)
            )
            storage = bpy.context.active_object
            storage.name = "MilitechArmory_Secure_Storage"
            
            # Scale storage
            storage.scale.x = room_size[0] * 0.6
            storage.scale.y = room_size[1] * 0.6
            storage.scale.z = 2.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create storage material
            storage_material = bpy.data.materials.new(name="MilitechArmory_StorageMaterial")
            storage_material.use_nodes = True
            nodes = storage_material.node_tree.nodes
            links = storage_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
            principled.inputs['Metallic'].default_value = 0.9
            principled.inputs['Roughness'].default_value = 0.1
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            storage.data.materials.append(storage_material)
            
            room_objects.append(storage)
            
            # Create weapon racks
            for i in range(4):
                # Calculate rack position
                if i == 0:  # Front
                    rack_x = room_x
                    rack_y = room_y - room_size[1] * 0.3
                    rack_rot_z = 0
                elif i == 1:  # Right
                    rack_x = room_x + room_size[0] * 0.3
                    rack_y = room_y
                    rack_rot_z = math.radians(90)
                elif i == 2:  # Back
                    rack_x = room_x
                    rack_y = room_y + room_size[1] * 0.3
                    rack_rot_z = 0
                else:  # Left
                    rack_x = room_x - room_size[0] * 0.3
                    rack_y = room_y
                    rack_rot_z = math.radians(90)
                
                # Create rack
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(rack_x, rack_y, room_z + 1.0)
                )
                rack = bpy.context.active_object
                rack.name = f"MilitechArmory_Weapon_Rack_{i}"
                
                # Scale rack
                rack.scale.x = room_size[0] * 0.5
                rack.scale.y = 0.1
                rack.scale.z = 1.8
                
                # Rotate rack
                rack.rotation_euler.z = rack_rot_z
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                rack.data.materials.append(storage_material)
                
                room_objects.append(rack)
                
                # Create weapons on rack
                weapon_count = 5
                for j in range(weapon_count):
                    # Calculate weapon position
                    if i == 0 or i == 2:  # Front or back
                        weapon_x = rack_x - room_size[0] * 0.2 + j * room_size[0] * 0.1
                        weapon_y = rack_y
                        weapon_rot_z = 0
                    else:  # Left or right
                        weapon_x = rack_x
                        weapon_y = rack_y - room_size[1] * 0.2 + j * room_size[1] * 0.1
                        weapon_rot_z = math.radians(90)
                    
                    # Create weapon
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(weapon_x, weapon_y, room_z + 0.5 + j * 0.3)
                    )
                    weapon = bpy.context.active_object
                    weapon.name = f"MilitechArmory_Stored_Weapon_{i}_{j}"
                    
                    # Scale weapon
                    weapon.scale.x = 0.8
                    weapon.scale.y = 0.2
                    weapon.scale.z = 0.2
                    
                    # Rotate weapon
                    weapon.rotation_euler.z = weapon_rot_z
                    
                    # Apply transformations
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                    
                    # Create weapon material
                    weapon_material = bpy.data.materials.new(name=f"MilitechArmory_StoredWeaponMaterial_{i}_{j}")
                    weapon_material.use_nodes = True
                    nodes = weapon_material.node_tree.nodes
                    links = weapon_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set properties
                    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Black
                    principled.inputs['Metallic'].default_value = 0.9
                    principled.inputs['Roughness'].default_value = 0.1
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    weapon.data.materials.append(weapon_material)
                    
                    room_objects.append(weapon)
            
            # Create security scanners
            for i in range(2):
                scanner_x = room_x - room_size[0] * 0.2 + i * room_size[0] * 0.4
                scanner_y = room_y - room_size[1] * 0.4
                
                # Create scanner base
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.2,
                    depth=0.1,
                    align='WORLD',
                    location=(scanner_x, scanner_y, room_z + 0.05)
                )
                scanner_base = bpy.context.active_object
                scanner_base.name = f"MilitechArmory_Vault_Scanner_{i}"
                
                # Assign material
                scanner_base.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(scanner_base)
                
                # Create scanner beam
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.05,
                    depth=3.0,
                    align='WORLD',
                    location=(scanner_x, scanner_y, room_z + 1.5)
                )
                scanner_beam = bpy.context.active_object
                scanner_beam.name = f"MilitechArmory_Vault_Scanner_Beam_{i}"
                
                # Create beam material
                beam_material = bpy.data.materials.new(name=f"MilitechArmory_BeamMaterial_{i}")
                beam_material.use_nodes = True
                nodes = beam_material.node_tree.nodes
                links = beam_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                emission = nodes.new(type='ShaderNodeEmission')
                
                # Set properties
                emission.inputs['Color'].default_value = (0.8, 0.1, 0.1, 0.5)  # Red
                emission.inputs['Strength'].default_value = 1.0
                
                # Connect nodes
                links.new(emission.outputs['Emission'], output.inputs['Surface'])
                
                # Assign material
                scanner_beam.data.materials.append(beam_material)
                
                room_objects.append(scanner_beam)
            
            # Create security turrets
            for i in range(4):
                angle = i * (math.pi / 2) + math.pi / 4
                turret_x = room_x + room_size[0] * 0.4 * math.cos(angle)
                turret_y = room_y + room_size[1] * 0.4 * math.sin(angle)
                
                # Create turret base
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=16,
                    radius=0.2,
                    depth=0.2,
                    align='WORLD',
                    location=(turret_x, turret_y, room_z + room_size[2] - 0.1)
                )
                turret_base = bpy.context.active_object
                turret_base.name = f"MilitechArmory_Security_Turret_Base_{i}"
                
                # Assign material
                turret_base.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(turret_base)
                
                # Create turret body
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(turret_x, turret_y, room_z + room_size[2] - 0.3)
                )
                turret_body = bpy.context.active_object
                turret_body.name = f"MilitechArmory_Security_Turret_Body_{i}"
                
                # Scale turret body
                turret_body.scale.x = 0.3
                turret_body.scale.y = 0.3
                turret_body.scale.z = 0.2
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                turret_body.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(turret_body)
                
                # Create turret barrel
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=0.05,
                    depth=0.4,
                    align='WORLD',
                    location=(turret_x, turret_y, room_z + room_size[2] - 0.3)
                )
                turret_barrel = bpy.context.active_object
                turret_barrel.name = f"MilitechArmory_Security_Turret_Barrel_{i}"
                
                # Rotate barrel to point toward center
                direction = Vector((room_x, room_y, 0)) - Vector((turret_x, turret_y, 0))
                rot_angle = math.atan2(direction.y, direction.x)
                turret_barrel.rotation_euler.z = rot_angle
                turret_barrel.rotation_euler.x = math.radians(90)
                
                # Apply rotation
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                
                # Assign material
                turret_barrel.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(turret_barrel)
            
        elif room_name == "Executive_Office":
            # Create executive desk
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y, room_z + 0.5)
            )
            desk = bpy.context.active_object
            desk.name = "MilitechArmory_Executive_Desk"
            
            # Scale desk
            desk.scale.x = room_size[0] * 0.4
            desk.scale.y = room_size[1] * 0.2
            desk.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create desk material
            desk_material = bpy.data.materials.new(name="MilitechArmory_DeskMaterial")
            desk_material.use_nodes = True
            nodes = desk_material.node_tree.nodes
            links = desk_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)  # Very dark gray
            principled.inputs['Metallic'].default_value = 0.9
            principled.inputs['Roughness'].default_value = 0.1
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            desk.data.materials.append(desk_material)
            
            room_objects.append(desk)
            
            # Create executive chair
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y + room_size[1] * 0.1, room_z + 0.5)
            )
            chair = bpy.context.active_object
            chair.name = "MilitechArmory_Executive_Chair"
            
            # Scale chair
            chair.scale.x = 0.6
            chair.scale.y = 0.6
            chair.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create chair material
            chair_material = bpy.data.materials.new(name="MilitechArmory_ChairMaterial")
            chair_material.use_nodes = True
            nodes = chair_material.node_tree.nodes
            links = chair_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
            principled.inputs['Roughness'].default_value = 0.8
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            chair.data.materials.append(chair_material)
            
            room_objects.append(chair)
            
            # Create chair back
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y + room_size[1] * 0.15, room_z + 1.0)
            )
            chair_back = bpy.context.active_object
            chair_back.name = "MilitechArmory_Chair_Back"
            
            # Scale chair back
            chair_back.scale.x = 0.6
            chair_back.scale.y = 0.1
            chair_back.scale.z = 1.0
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Assign material
            chair_back.data.materials.append(chair_material)
            
            room_objects.append(chair_back)
            
            # Create computer on desk
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y - room_size[1] * 0.1, room_z + 1.0)
            )
            computer = bpy.context.active_object
            computer.name = "MilitechArmory_Executive_Computer"
            
            # Scale computer
            computer.scale.x = 0.6
            computer.scale.y = 0.1
            computer.scale.z = 0.4
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create computer screen material
            screen_material = bpy.data.materials.new(name="MilitechArmory_ComputerScreenMaterial")
            screen_material.use_nodes = True
            nodes = screen_material.node_tree.nodes
            links = screen_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            emission = nodes.new(type='ShaderNodeEmission')
            
            # Set properties
            emission.inputs['Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
            emission.inputs['Strength'].default_value = 1.0
            
            # Connect nodes
            links.new(emission.outputs['Emission'], output.inputs['Surface'])
            
            # Assign material
            computer.data.materials.append(screen_material)
            
            room_objects.append(computer)
            
            # Create weapon display cases
            for i in range(3):
                case_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.3
                case_y = room_y - room_size[1] * 0.4
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(case_x, case_y, room_z + 0.5)
                )
                case = bpy.context.active_object
                case.name = f"MilitechArmory_Trophy_Case_{i}"
                
                # Scale case
                case.scale.x = 0.4
                case.scale.y = 0.4
                case.scale.z = 1.0
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create case material
                case_material = bpy.data.materials.new(name=f"MilitechArmory_TrophyCaseMaterial_{i}")
                case_material.use_nodes = True
                nodes = case_material.node_tree.nodes
                links = case_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
                principled.inputs['Metallic'].default_value = 0.8
                principled.inputs['Roughness'].default_value = 0.2
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                case.data.materials.append(case_material)
                
                room_objects.append(case)
                
                # Create trophy weapon
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(case_x, case_y, room_z + 1.0)
                )
                trophy = bpy.context.active_object
                trophy.name = f"MilitechArmory_Trophy_Weapon_{i}"
                
                # Scale trophy
                trophy.scale.x = 0.3
                trophy.scale.y = 0.1
                trophy.scale.z = 0.1
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create trophy material
                trophy_material = bpy.data.materials.new(name=f"MilitechArmory_TrophyMaterial_{i}")
                trophy_material.use_nodes = True
                nodes = trophy_material.node_tree.nodes
                links = trophy_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.8, 0.7, 0.2, 1.0)  # Gold
                principled.inputs['Metallic'].default_value = 1.0
                principled.inputs['Roughness'].default_value = 0.1
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                trophy.data.materials.append(trophy_material)
                
                room_objects.append(trophy)
            
            # Create wall-mounted weapons
            for i in range(2):
                weapon_x = room_x - room_size[0] * 0.3 + i * room_size[0] * 0.6
                weapon_y = room_y + room_size[1] * 0.4
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(weapon_x, weapon_y, room_z + 1.5)
                )
                wall_weapon = bpy.context.active_object
                wall_weapon.name = f"MilitechArmory_Wall_Weapon_{i}"
                
                # Scale wall weapon
                wall_weapon.scale.x = 1.0
                wall_weapon.scale.y = 0.1
                wall_weapon.scale.z = 0.2
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Create wall weapon material
                wall_weapon_material = bpy.data.materials.new(name=f"MilitechArmory_WallWeaponMaterial_{i}")
                wall_weapon_material.use_nodes = True
                nodes = wall_weapon_material.node_tree.nodes
                links = wall_weapon_material.node_tree.links
                
                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)
                
                # Create nodes
                output = nodes.new(type='ShaderNodeOutputMaterial')
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                
                # Set properties
                principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Black
                principled.inputs['Metallic'].default_value = 0.9
                principled.inputs['Roughness'].default_value = 0.1
                
                # Connect nodes
                links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                
                # Assign material
                wall_weapon.data.materials.append(wall_weapon_material)
                
                room_objects.append(wall_weapon)
                
                # Create weapon mount
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(weapon_x, weapon_y - 0.05, room_z + 1.5)
                )
                mount = bpy.context.active_object
                mount.name = f"MilitechArmory_Weapon_Mount_{i}"
                
                # Scale mount
                mount.scale.x = 1.1
                mount.scale.y = 0.05
                mount.scale.z = 0.3
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                mount.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(mount)
            
            # Create executive
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                enter_editmode=False,
                align='WORLD',
                location=(room_x, room_y + room_size[1] * 0.1, room_z + 1.0)
            )
            executive = bpy.context.active_object
            executive.name = "MilitechArmory_Executive"
            
            # Scale executive
            executive.scale.x = 0.4
            executive.scale.y = 0.4
            executive.scale.z = 0.8
            
            # Apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            # Create executive material
            executive_material = bpy.data.materials.new(name="MilitechArmory_ExecutiveMaterial")
            executive_material.use_nodes = True
            nodes = executive_material.node_tree.nodes
            links = executive_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Black suit
            principled.inputs['Roughness'].default_value = 0.7
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            executive.data.materials.append(executive_material)
            
            room_objects.append(executive)
            
            # Create executive head
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.2,
                align='WORLD',
                location=(room_x, room_y + room_size[1] * 0.1, room_z + 1.8)
            )
            head = bpy.context.active_object
            head.name = "MilitechArmory_Executive_Head"
            
            # Create head material
            head_material = bpy.data.materials.new(name="MilitechArmory_HeadMaterial")
            head_material.use_nodes = True
            nodes = head_material.node_tree.nodes
            links = head_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.8, 0.6, 0.5, 1.0)  # Skin tone
            principled.inputs['Roughness'].default_value = 0.7
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            head.data.materials.append(head_material)
            
            room_objects.append(head)
    
    # Create connecting corridors between rooms
    corridor_data = [
        {
            "start": "Security_Lobby",
            "end": "Showroom",
            "width": building_size.x * 0.2,
            "height": building_size.z * 0.15,
            "vertical": True
        },
        {
            "start": "Showroom",
            "end": "Testing_Range",
            "width": building_size.x * 0.2,
            "height": building_size.z * 0.15,
            "vertical": True
        },
        {
            "start": "Showroom",
            "end": "RD_Lab",
            "width": building_size.x * 0.2,
            "height": building_size.z * 0.15,
            "vertical": True
        },
        {
            "start": "Testing_Range",
            "end": "Secure_Vault",
            "width": building_size.x * 0.2,
            "height": building_size.z * 0.15,
            "vertical": True
        },
        {
            "start": "RD_Lab",
            "end": "Executive_Office",
            "width": building_size.x * 0.2,
            "height": building_size.z * 0.15,
            "vertical": True
        }
    ]
    
    # Find room positions
    room_positions = {}
    for room_data in rooms_data:
        room_name = room_data["name"]
        room_pos = room_data["position"]
        floor_level = room_data["floor_level"]
        
        # Calculate absolute position
        room_x = building_loc[0] + room_pos[0]
        room_y = building_loc[1] + room_pos[1]
        room_z = building_loc[2] - building_size.z/2 + building_size.z * 0.1 + floor_level * building_size.z * 0.2
        
        room_positions[room_name] = (room_x, room_y, room_z)
    
    # Create corridors
    for corridor in corridor_data:
        start_name = corridor["start"]
        end_name = corridor["end"]
        corridor_width = corridor["width"]
        corridor_height = corridor["height"]
        vertical = corridor.get("vertical", False)
        
        if start_name in room_positions and end_name in room_positions:
            start_pos = room_positions[start_name]
            end_pos = room_positions[end_name]
            
            if vertical:
                # Create elevator shaft
                elevator_x = (start_pos[0] + end_pos[0]) / 2
                elevator_y = (start_pos[1] + end_pos[1]) / 2
                elevator_z = (start_pos[2] + end_pos[2]) / 2
                elevator_height = abs(end_pos[2] - start_pos[2])
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(elevator_x, elevator_y, elevator_z)
                )
                elevator = bpy.context.active_object
                elevator.name = f"MilitechArmory_Elevator_{start_name}_to_{end_name}"
                
                # Scale elevator
                elevator.scale.x = corridor_width
                elevator.scale.y = corridor_width
                elevator.scale.z = elevator_height
                
                # Apply scale
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Assign material
                elevator.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(elevator)
                
                # Create elevator doors
                for i, pos in enumerate([start_pos, end_pos]):
                    door_x = pos[0]
                    door_y = pos[1]
                    door_z = pos[2] + corridor_height/2
                    
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        enter_editmode=False,
                        align='WORLD',
                        location=(door_x, door_y, door_z)
                    )
                    door = bpy.context.active_object
                    door.name = f"MilitechArmory_Elevator_Door_{i}_{start_name}_to_{end_name}"
                    
                    # Scale door
                    door.scale.x = corridor_width * 0.8
                    door.scale.y = 0.05
                    door.scale.z = corridor_height * 0.8
                    
                    # Apply scale
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Create door material
                    door_material = bpy.data.materials.new(name=f"MilitechArmory_ElevatorDoorMaterial_{i}")
                    door_material.use_nodes = True
                    nodes = door_material.node_tree.nodes
                    links = door_material.node_tree.links
                    
                    # Clear default nodes
                    for node in nodes:
                        nodes.remove(node)
                    
                    # Create nodes
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                    
                    # Set properties
                    principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
                    principled.inputs['Metallic'].default_value = 0.9
                    principled.inputs['Roughness'].default_value = 0.1
                    
                    # Connect nodes
                    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
                    
                    # Assign material
                    door.data.materials.append(door_material)
                    
                    room_objects.append(door)
            else:
                # Create horizontal corridor
                corridor_x = (start_pos[0] + end_pos[0]) / 2
                corridor_y = (start_pos[1] + end_pos[1]) / 2
                corridor_z = start_pos[2]  # Use start room's z position
                
                # Calculate corridor direction and length
                direction = Vector((end_pos[0], end_pos[1], 0)) - Vector((start_pos[0], start_pos[1], 0))
                length = direction.length
                direction.normalize()
                
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    enter_editmode=False,
                    align='WORLD',
                    location=(corridor_x, corridor_y, corridor_z + corridor_height/2)
                )
                corridor_obj = bpy.context.active_object
                corridor_obj.name = f"MilitechArmory_Corridor_{start_name}_to_{end_name}"
                
                # Scale corridor
                corridor_obj.scale.x = length
                corridor_obj.scale.y = corridor_width
                corridor_obj.scale.z = corridor_height
                
                # Rotate corridor to point from start to end
                corridor_obj.rotation_euler.z = math.atan2(direction.y, direction.x)
                
                # Apply transformations
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Assign material
                corridor_obj.data.materials.append(interior_materials["Militech_Interior"])
                
                room_objects.append(corridor_obj)
    
    # Move all objects to the rooms collection
    for obj in room_objects:
        if obj.name not in rooms_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(rooms_collection.name))
    
    return rooms_collection



# Main function to implement rooms for all buildings
def implement_building_rooms(building_objects, materials, interior_materials):
    """Implement rooms per floor for all buildings"""
    # Implement rooms for each building
    rooms = {}
    
    # NeoTech Labs Tower
    if "neotech_tower" in building_objects:
        rooms["NeoTech_Rooms"] = create_neotech_rooms(
            building_objects["neotech_tower"],
            materials,
            interior_materials
        )
    
    # Specter Station
    if "specter_station" in building_objects:
        rooms["Specter_Rooms"] = create_specter_rooms(
            building_objects["specter_station"],
            materials,
            interior_materials
        )
    
	# Black Nexus
    if "black_nexus" in building_objects:
        rooms["BlackNexus_Rooms"] = create_black_nexus_rooms(
            building_objects["black_nexus"],
            materials,
            interior_materials
        )
	
	# Wire Nest
    if "wire_nest" in building_objects:
        rooms["WireNest_Rooms"] = create_wire_nest_rooms(
            building_objects["wire_nest"],
            materials,
            interior_materials
        )

	# Rust Vault
    if "rust_vault" in building_objects:
        rooms["RustVault_Rooms"] = create_rust_vault_rooms(
            building_objects["rust_vault"],
            materials,
            interior_materials
        )
	
	# Militech Armory
    if "militech_armory" in building_objects:
        rooms["MilitechArmory_Rooms"] = create_militech_armory_rooms(
            building_objects["militech_armory"],
            materials,
            interior_materials
        )

    return rooms
