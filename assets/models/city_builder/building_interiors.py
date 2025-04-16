"""
Neon Crucible - Building Interiors Implementation
Blender 4.2 Python Script for generating interior spaces, entrances, doors, and windows
for buildings in the Neon Crucible cyberpunk world.

This script implements detailed interior spaces for key locations including:
- NeoTech Labs Tower (Upper Tier)
- Specter Station (Mid Tier)
- Black Nexus (ShadowRunner's Hidden Hub, Lower Tier)
- Wire Nest (Mid Tier hacker den)
- Rust Vault (Lower Tier hacker den)
- Militech Armory (Upper Tier)
- Biotechnica Spire (Upper Tier)
"""

import bpy
import bmesh
import random
import math
import os
from mathutils import Vector, Matrix

# Import city generation script functions if available
# Assuming city_generation.py is in the same directory
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from city_generation import create_materials, clear_scene, create_collections
except ImportError:
    print("Warning: Could not import from city_generation.py")

# Create interior materials
def create_interior_materials():
    """Create materials for interior spaces of buildings"""
    materials = {}
    
    # NeoTech Labs Interior - Sleek and corporate
    neotech_interior = bpy.data.materials.new(name="NeoTech_Interior")
    neotech_interior.use_nodes = True
    nodes = neotech_interior.node_tree.nodes
    links = neotech_interior.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.05, 0.05, 0.07, 1.0)  # Dark blue-gray
    principled.inputs['Metallic'].default_value = 0.7
    principled.inputs['Roughness'].default_value = 0.2
    #principled.inputs['Specular'].default_value = 0.8
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["NeoTech_Interior"] = neotech_interior
    
    # NeoTech Labs Floor - Polished
    neotech_floor = bpy.data.materials.new(name="NeoTech_Floor")
    neotech_floor.use_nodes = True
    nodes = neotech_floor.node_tree.nodes
    links = neotech_floor.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.02, 0.02, 0.03, 1.0)  # Almost black
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.1
    #principled.inputs['Specular'].default_value = 1.0
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["NeoTech_Floor"] = neotech_floor
    
    # NeoTech Labs Glass - Transparent
    neotech_glass = bpy.data.materials.new(name="NeoTech_Glass")
    neotech_glass.use_nodes = True
    nodes = neotech_glass.node_tree.nodes
    links = neotech_glass.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.9, 1.0)  # Light blue tint
    principled.inputs['Metallic'].default_value = 0.1
    principled.inputs['Roughness'].default_value = 0.05
    #principled.inputs['Transmission'].default_value = 0.95  # Almost fully transparent
    principled.inputs['IOR'].default_value = 1.45
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["NeoTech_Glass"] = neotech_glass
    
    # Specter Station Interior - Derelict
    specter_interior = bpy.data.materials.new(name="Specter_Interior")
    specter_interior.use_nodes = True
    nodes = specter_interior.node_tree.nodes
    links = specter_interior.node_tree.links
    
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
    principled.inputs['Base Color'].default_value = (0.25, 0.23, 0.2, 1.0)  # Dirty beige
    principled.inputs['Metallic'].default_value = 0.1
    principled.inputs['Roughness'].default_value = 0.8
    
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.6
    
    # Setup color ramp for dirt/wear effect
    colorramp.color_ramp.elements[0].position = 0.4
    colorramp.color_ramp.elements[0].color = (0.15, 0.13, 0.1, 1.0)  # Darker dirt
    colorramp.color_ramp.elements[1].position = 0.7
    colorramp.color_ramp.elements[1].color = (0.3, 0.28, 0.25, 1.0)  # Lighter areas
    
    # Connect nodes
    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(colorramp.outputs['Color'], principled.inputs['Roughness'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["Specter_Interior"] = specter_interior
    
    # Black Nexus Interior - Concrete bunker
    black_nexus_interior = bpy.data.materials.new(name="BlackNexus_Interior")
    black_nexus_interior.use_nodes = True
    nodes = black_nexus_interior.node_tree.nodes
    links = black_nexus_interior.node_tree.links
    
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
    principled.inputs['Base Color'].default_value = (0.15, 0.15, 0.15, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.9
    
    noise.inputs['Scale'].default_value = 10.0
    noise.inputs['Detail'].default_value = 6.0
    noise.inputs['Roughness'].default_value = 0.7
    
    # Connect nodes
    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], principled.inputs['Roughness'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["BlackNexus_Interior"] = black_nexus_interior
    
    # Wire Nest Interior - Tech-filled
    wire_nest_interior = bpy.data.materials.new(name="WireNest_Interior")
    wire_nest_interior.use_nodes = True
    nodes = wire_nest_interior.node_tree.nodes
    links = wire_nest_interior.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.25, 1.0)  # Dark blue-gray
    principled.inputs['Metallic'].default_value = 0.4
    principled.inputs['Roughness'].default_value = 0.6
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["WireNest_Interior"] = wire_nest_interior
    
    # Rust Vault Interior - Industrial
    rust_vault_interior = bpy.data.materials.new(name="RustVault_Interior")
    rust_vault_interior.use_nodes = True
    nodes = rust_vault_interior.node_tree.nodes
    links = rust_vault_interior.node_tree.links
    
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
    principled.inputs['Base Color'].default_value = (0.3, 0.25, 0.2, 1.0)  # Rusty brown
    principled.inputs['Metallic'].default_value = 0.3
    principled.inputs['Roughness'].default_value = 0.8
    
    noise.inputs['Scale'].default_value = 8.0
    noise.inputs['Detail'].default_value = 12.0
    noise.inputs['Roughness'].default_value = 0.7
    
    # Setup color ramp for rust effect
    colorramp.color_ramp.elements[0].position = 0.3
    colorramp.color_ramp.elements[0].color = (0.4, 0.15, 0.05, 1.0)  # Rust color
    colorramp.color_ramp.elements[1].position = 0.7
    colorramp.color_ramp.elements[1].color = (0.25, 0.2, 0.15, 1.0)  # Metal color
    
    # Connect nodes
    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["RustVault_Interior"] = rust_vault_interior
    
    # Militech Armory Interior - Military grade
    militech_interior = bpy.data.materials.new(name="Militech_Interior")
    militech_interior.use_nodes = True
    nodes = militech_interior.node_tree.nodes
    links = militech_interior.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.6
    principled.inputs['Roughness'].default_value = 0.3
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["Militech_Interior"] = militech_interior
    
    # Biotechnica Spire Interior - Clinical
    biotechnica_interior = bpy.data.materials.new(name="Biotechnica_Interior")
    biotechnica_interior.use_nodes = True
    nodes = biotechnica_interior.node_tree.nodes
    links = biotechnica_interior.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # Almost white
    principled.inputs['Metallic'].default_value = 0.1
    principled.inputs['Roughness'].default_value = 0.2
    #principled.inputs['Clearcoat'].default_value = 0.5
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    materials["Biotechnica_Interior"] = biotechnica_interior
    
    # Hologram material
    hologram = bpy.data.materials.new(name="Hologram")
    hologram.use_nodes = True
    nodes = hologram.node_tree.nodes
    links = hologram.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set properties
    emission.inputs['Color'].default_value = (0.0, 0.8, 1.0, 1.0)  # Cyan
    emission.inputs['Strength'].default_value = 3.0
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    materials["Hologram"] = hologram
    
    # Neon light material
    neon_light = bpy.data.materials.new(name="Neon_Light")
    neon_light.use_nodes = True
    nodes = neon_light.node_tree.nodes
    links = neon_light.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set properties
    emission.inputs['Color'].default_value = (1.0, 0.2, 0.8, 1.0)  # Pink
    emission.inputs['Strength'].default_value = 5.0
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    materials["Neon_Light"] = neon_light
    
    return materials

# Modular interior component functions
def create_floor(name, location, size, height, material):
    """Create a floor with given parameters"""
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] - height/2)
    )
    floor = bpy.context.active_object
    floor.name = name
    
    # Scale to size
    floor.scale.x = size[0]
    floor.scale.y = size[1]
    floor.scale.z = height
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    if material:
        floor.data.materials.append(material)
    
    return floor

def create_ceiling(name, location, size, height, material):
    """Create a ceiling with given parameters"""
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + height/2)
    )
    ceiling = bpy.context.active_object
    ceiling.name = name
    
    # Scale to size
    ceiling.scale.x = size[0]
    ceiling.scale.y = size[1]
    ceiling.scale.z = height
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    if material:
        ceiling.data.materials.append(material)
    
    return ceiling

def create_wall(name, start, end, height, thickness, material, with_window=False, window_height=1.5, window_width=2.0):
    """Create a wall between two points with given height and thickness"""
    # Calculate center point and dimensions
    center_x = (start[0] + end[0]) / 2
    center_y = (start[1] + end[1]) / 2
    center_z = start[2] + height / 2
    
    length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    
    # Calculate rotation angle
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    
    # Create wall
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(center_x, center_y, center_z)
    )
    wall = bpy.context.active_object
    wall.name = name
    
    # Scale to size
    wall.scale.x = length
    wall.scale.y = thickness
    wall.scale.z = height
    
    # Rotate
    wall.rotation_euler.z = angle
    
    # Apply transformations
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # Assign material
    if material:
        wall.data.materials.append(material)
    
    # Add window if requested
    if with_window:
        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(wall.data)
        
        # Create window cutout
        window_z = height / 2  # Center of wall height
        window_height_half = window_height / 2
        window_width_half = window_width / 2
        
        # Define window vertices in local coordinates
        verts = [
            (-window_width_half, -thickness/2 - 0.01, window_z - window_height_half),
            (window_width_half, -thickness/2 - 0.01, window_z - window_height_half),
            (window_width_half, -thickness/2 - 0.01, window_z + window_height_half),
            (-window_width_half, -thickness/2 - 0.01, window_z + window_height_half),
            (-window_width_half, thickness/2 + 0.01, window_z - window_height_half),
            (window_width_half, thickness/2 + 0.01, window_z - window_height_half),
            (window_width_half, thickness/2 + 0.01, window_z + window_height_half),
            (-window_width_half, thickness/2 + 0.01, window_z + window_height_half)
        ]
        
        # Create window cutout
        bmesh.ops.create_cube(bm)
        for v in bm.verts:
            v.co.x *= window_width
            v.co.y *= thickness + 0.02  # Slightly larger than wall thickness
            v.co.z *= window_height
            v.co.z += window_z  # Position at window height
        
        # Boolean difference
        bmesh.ops.delete(bm, geom=bm.faces, context='FACES')
        
        # Update mesh and exit edit mode
        bmesh.update_edit_mesh(wall.data)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    return wall

# --- In building_interiors.py ---

def create_door(name, location, width, height, thickness, material, is_open=False, open_angle=90):
    """Create a door with given parameters"""
    # Door frame
    frame_width = width + 0.2
    frame_height = height + 0.1

    # Create door frame (outer part)
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=True, # Start in edit mode
        align='WORLD',
        location=(location[0], location[1], location[2] + height/2)
    )
    frame = bpy.context.active_object
    frame.name = f"{name}_Frame"

    # Edit the frame to make it hollow
    bm = bmesh.from_edit_mesh(frame.data)

    # --- Ensure table is valid before accessing verts ---
    bm.verts.ensure_lookup_table()

    # Scale outer frame
    for v in bm.verts: # Iterating is usually safe without ensure_lookup_table *here*
        v.co.x *= frame_width
        v.co.y *= thickness
        v.co.z *= frame_height

    # --- Ensure table is valid AGAIN before accessing by index [i] ---
    bm.verts.ensure_lookup_table() # <<< --- THE FIX ---

    # Create inner cutout vertices based on original scaled vertices
    inner_verts_coords = []
    if len(bm.verts) >= 8: # Make sure we actually have the 8 cube verts
        for i in range(8):
             # Store coordinates first, don't modify bmesh while iterating by index
             inner_verts_coords.append(Vector((
                0.9 * bm.verts[i].co.x,
                1.1 * bm.verts[i].co.y, # Make it go through the frame
                0.9 * bm.verts[i].co.z
             )))
    else:
         print(f"Warning: Expected 8 vertices for door frame '{name}', found {len(bm.verts)}. Skipping inner cutout.")
         # Handle the case where the initial cube wasn't created as expected
         inner_verts_coords = [] # Ensure list is empty if verts aren't there

    # Now create the new vertices from the stored coordinates
    inner_verts_bmesh = []
    for coord in inner_verts_coords:
        inner_verts_bmesh.append(bm.verts.new(coord))

    # Create faces for inner cutout using the newly created bmesh vertices
    if len(inner_verts_bmesh) == 8:
        # Ensure face winding order is correct (counter-clockwise usually)
        # Order might need adjustment depending on cube creation/scaling
        face_indices = [
            (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6),
            (3, 0, 4, 7), (4, 5, 6, 7), (0, 3, 2, 1) # Top and bottom faces might need reversed winding
        ]
        for indices in face_indices:
            try:
                # Try creating faces, handle potential errors (e.g., degenerate faces)
                 bm.faces.new(tuple(inner_verts_bmesh[i] for i in indices))
            except ValueError as e:
                 print(f"Warning: Could not create inner face for door frame '{name}' with indices {indices}: {e}")
    else:
         print(f"Warning: Could not create inner faces for door frame '{name}' due to incorrect number of inner vertices.")


    # Update mesh data from bmesh
    bmesh.update_edit_mesh(frame.data)
    # No need for free() if using from_edit_mesh/update_edit_mesh pair
    # bm.free() # Only needed if creating a totally new bmesh not linked to object data

    bpy.ops.object.mode_set(mode='OBJECT') # Exit Edit mode

    # Assign material
    if material:
        # Ensure material slot exists, add if not
        if not frame.data.materials:
             frame.data.materials.append(material)
        else:
             frame.data.materials[0] = material # Assign to first slot


    # --- Create Door Panel ---
    # (This part seemed okay, but added cursor management for robustness)
    # Store current cursor location
    saved_cursor_location = bpy.context.scene.cursor.location.copy()

    # Set cursor for door pivot
    bpy.context.scene.cursor.location = (location[0] - width/2, location[1], location[2]) # Pivot on edge

    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False, # Create in object mode
        align='WORLD',
        location=(location[0], location[1], location[2] + height/2) # Create at center first
    )
    door = bpy.context.active_object
    door.name = name

    # Scale door
    # Note: Scaling in object mode affects origin unless applied
    door.scale = (width * 0.9, thickness * 0.5, height * 0.95)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) # Apply scale AFTER setting it

    # Move door so pivot edge aligns with cursor
    # We know the width and the pivot location
    door.location = (location[0] - (width * 0.9 / 2), location[1], location[2] + height/2) # Adjust location based on scale

    # Set origin to cursor location (which is the pivot point)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Open door if requested
    if is_open:
        door.rotation_euler.z = math.radians(open_angle)

    # Assign material
    if material:
         if not door.data.materials:
              door.data.materials.append(material)
         else:
              door.data.materials[0] = material

    # Restore cursor location
    bpy.context.scene.cursor.location = saved_cursor_location

    return {"frame": frame, "door": door}

def create_window(name, location, width, height, thickness, material):
    """Create a window with given parameters"""
    # Window frame
    frame_width = width + 0.1
    frame_height = height + 0.1
    
    # Create window frame
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=True,
        align='WORLD',
        location=(location[0], location[1], location[2] + height/2)
    )
    frame = bpy.context.active_object
    frame.name = f"{name}_Frame"
    
    # Edit the frame to make it hollow
    bm = bmesh.from_edit_mesh(frame.data)
    
    # Scale outer frame
    for v in bm.verts:
        v.co.x *= frame_width
        v.co.y *= thickness
        v.co.z *= frame_height
    
    # Create inner cutout
    inner_verts = []
    for i in range(8):
        inner_vert = bm.verts.new((
            0.9 * bm.verts[i].co.x,
            1.1 * bm.verts[i].co.y,  # Make it go through the frame
            0.9 * bm.verts[i].co.z
        ))
        inner_verts.append(inner_vert)
    
    # Create faces for inner cutout
    for i in range(4):
        bm.faces.new([inner_verts[i], inner_verts[(i+1)%4], inner_verts[(i+1)%4+4], inner_verts[i+4]])
    
    # Update mesh
    bmesh.update_edit_mesh(frame.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Assign material
    if material:
        frame.data.materials.append(material)
    
    # Create glass
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + height/2)
    )
    glass = bpy.context.active_object
    glass.name = f"{name}_Glass"
    
    # Scale glass
    glass.scale.x = width * 0.85
    glass.scale.y = thickness * 0.2
    glass.scale.z = height * 0.85
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign glass material
    if "NeoTech_Glass" in bpy.data.materials:
        glass.data.materials.append(bpy.data.materials["NeoTech_Glass"])
    
    return {"frame": frame, "glass": glass}

def create_desk(name, location, width, depth, height, material):
    """Create a desk with given parameters"""
    # Create desk top
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + height)
    )
    desk_top = bpy.context.active_object
    desk_top.name = f"{name}_Top"
    
    # Scale desk top
    desk_top.scale.x = width
    desk_top.scale.y = depth
    desk_top.scale.z = 0.05 * height
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create desk legs
    legs = []
    leg_positions = [
        (location[0] - width/2 + 0.1, location[1] - depth/2 + 0.1, location[2] + height/2),
        (location[0] + width/2 - 0.1, location[1] - depth/2 + 0.1, location[2] + height/2),
        (location[0] - width/2 + 0.1, location[1] + depth/2 - 0.1, location[2] + height/2),
        (location[0] + width/2 - 0.1, location[1] + depth/2 - 0.1, location[2] + height/2)
    ]
    
    for i, pos in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=pos
        )
        leg = bpy.context.active_object
        leg.name = f"{name}_Leg_{i}"
        
        # Scale leg
        leg.scale.x = 0.05 * width
        leg.scale.y = 0.05 * depth
        leg.scale.z = height
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        if material:
            leg.data.materials.append(material)
        
        legs.append(leg)
    
    # Assign material to desk top
    if material:
        desk_top.data.materials.append(material)
    
    # Group all objects
    all_objects = [desk_top] + legs
    
    return all_objects

def create_chair(name, location, material):
    """Create a simple chair"""
    # Create seat
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 0.4)
    )
    seat = bpy.context.active_object
    seat.name = f"{name}_Seat"
    
    # Scale seat
    seat.scale.x = 0.4
    seat.scale.y = 0.4
    seat.scale.z = 0.05
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create backrest
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] + 0.2, location[2] + 0.7)
    )
    backrest = bpy.context.active_object
    backrest.name = f"{name}_Backrest"
    
    # Scale backrest
    backrest.scale.x = 0.4
    backrest.scale.y = 0.05
    backrest.scale.z = 0.6
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create legs
    legs = []
    leg_positions = [
        (location[0] - 0.15, location[1] - 0.15, location[2] + 0.2),
        (location[0] + 0.15, location[1] - 0.15, location[2] + 0.2),
        (location[0] - 0.15, location[1] + 0.15, location[2] + 0.2),
        (location[0] + 0.15, location[1] + 0.15, location[2] + 0.2)
    ]
    
    for i, pos in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=pos
        )
        leg = bpy.context.active_object
        leg.name = f"{name}_Leg_{i}"
        
        # Scale leg
        leg.scale.x = 0.05
        leg.scale.y = 0.05
        leg.scale.z = 0.4
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        if material:
            leg.data.materials.append(material)
        
        legs.append(leg)
    
    # Assign material
    if material:
        seat.data.materials.append(material)
        backrest.data.materials.append(material)
    
    # Group all objects
    all_objects = [seat, backrest] + legs
    
    return all_objects

def create_computer(name, location, material, screen_material):
    """Create a computer with monitor and keyboard"""
    # Create monitor base
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 0.05)
    )
    base = bpy.context.active_object
    base.name = f"{name}_Base"
    
    # Scale base
    base.scale.x = 0.3
    base.scale.y = 0.2
    base.scale.z = 0.05
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create monitor stand
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] - 0.05, location[2] + 0.25)
    )
    stand = bpy.context.active_object
    stand.name = f"{name}_Stand"
    
    # Scale stand
    stand.scale.x = 0.05
    stand.scale.y = 0.05
    stand.scale.z = 0.4
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create monitor screen
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] - 0.1, location[2] + 0.5)
    )
    screen = bpy.context.active_object
    screen.name = f"{name}_Screen"
    
    # Scale screen
    screen.scale.x = 0.5
    screen.scale.y = 0.05
    screen.scale.z = 0.3
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create keyboard
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] + 0.1, location[2] + 0.02)
    )
    keyboard = bpy.context.active_object
    keyboard.name = f"{name}_Keyboard"
    
    # Scale keyboard
    keyboard.scale.x = 0.4
    keyboard.scale.y = 0.15
    keyboard.scale.z = 0.02
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign materials
    if material:
        base.data.materials.append(material)
        stand.data.materials.append(material)
        keyboard.data.materials.append(material)
    
    if screen_material:
        screen.data.materials.append(screen_material)
    
    # Group all objects
    all_objects = [base, stand, screen, keyboard]
    
    return all_objects

def create_server_rack(name, location, material, light_material):
    """Create a server rack with blinking lights"""
    # Create rack
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 1.0)
    )
    rack = bpy.context.active_object
    rack.name = f"{name}_Rack"
    
    # Scale rack
    rack.scale.x = 0.6
    rack.scale.y = 0.8
    rack.scale.z = 2.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create server units
    servers = []
    for i in range(5):
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(location[0], location[1] - 0.41, location[2] + 0.4 + i * 0.3)
        )
        server = bpy.context.active_object
        server.name = f"{name}_Server_{i}"
        
        # Scale server
        server.scale.x = 0.55
        server.scale.y = 0.02
        server.scale.z = 0.12
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        if material:
            server.data.materials.append(material)
        
        servers.append(server)
    
    # Create lights
    lights = []
    for i in range(10):
        x_pos = random.uniform(-0.25, 0.25)
        z_pos = random.uniform(0.2, 1.8)
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(location[0] + x_pos, location[1] - 0.41, location[2] + z_pos)
        )
        light = bpy.context.active_object
        light.name = f"{name}_Light_{i}"
        
        # Scale light
        light.scale.x = 0.02
        light.scale.y = 0.02
        light.scale.z = 0.02
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign material
        if light_material:
            light.data.materials.append(light_material)
        
        lights.append(light)
    
    # Assign material to rack
    if material:
        rack.data.materials.append(material)
    
    # Group all objects
    all_objects = [rack] + servers + lights
    
    return all_objects

def create_hologram(name, location, size, material):
    """Create a holographic display"""
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    hologram = bpy.context.active_object
    hologram.name = name
    
    # Scale hologram
    hologram.scale.x = size[0]
    hologram.scale.y = size[1]
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    if material:
        hologram.data.materials.append(material)
    
    return hologram

# Building-specific interior implementation functions
def create_neotech_tower_interior(neotech_objects, materials, interior_materials):
    """Create interior spaces for NeoTech Labs Tower"""
    tower = neotech_objects["tower"]
    base = neotech_objects["base"]
    collection = neotech_objects["collection"]
    
    # Create a subcollection for interior objects
    if "NeoTech_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("NeoTech_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["NeoTech_Interior"]
    
    interior_objects = []
    
    # Get base location and dimensions
    base_loc = base.location
    base_radius = base.dimensions.x / 2
    
    # Create lobby floor
    lobby_floor = create_floor(
        "NeoTech_LobbyFloor",
        (base_loc[0], base_loc[1], base_loc[2]),
        (base_radius * 1.8, base_radius * 1.8, 0.2),
        0.1,
        interior_materials["NeoTech_Floor"]
    )
    interior_objects.append(lobby_floor)
    
    # Create lobby ceiling
    lobby_ceiling = create_ceiling(
        "NeoTech_LobbyCeiling",
        (base_loc[0], base_loc[1], base_loc[2] + 5),
        (base_radius * 1.8, base_radius * 1.8, 0.2),
        0.1,
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.append(lobby_ceiling)
    
    # Create circular walls for lobby
    wall_segments = 8
    for i in range(wall_segments):
        angle1 = i * (2 * math.pi / wall_segments)
        angle2 = ((i + 1) % wall_segments) * (2 * math.pi / wall_segments)
        
        x1 = base_loc[0] + base_radius * 0.9 * math.cos(angle1)
        y1 = base_loc[1] + base_radius * 0.9 * math.sin(angle1)
        x2 = base_loc[0] + base_radius * 0.9 * math.cos(angle2)
        y2 = base_loc[1] + base_radius * 0.9 * math.sin(angle2)
        
        # Add windows to alternating wall segments
        with_window = (i % 2 == 0)
        
        wall = create_wall(
            f"NeoTech_LobbyWall_{i}",
            (x1, y1, base_loc[2]),
            (x2, y2, base_loc[2]),
            5.0,
            0.2,
            interior_materials["NeoTech_Interior"],
            with_window=with_window
        )
        interior_objects.append(wall)
    
    # Create entrance (glass revolving door)
    entrance_x = base_loc[0]
    entrance_y = base_loc[1] - base_radius * 0.9
    entrance_z = base_loc[2]
    
    # Create door frame
    door_frame = create_door(
        "NeoTech_EntranceDoor",
        (entrance_x, entrance_y, entrance_z),
        3.0,
        4.0,
        0.3,
        interior_materials["NeoTech_Interior"],
        is_open=True,
        open_angle=0
    )
    interior_objects.append(door_frame["frame"])
    interior_objects.append(door_frame["door"])
    
    # Create revolving door segments (glass panels)
    revolving_segments = 4
    for i in range(revolving_segments):
        angle = i * (2 * math.pi / revolving_segments)
        
        bpy.ops.mesh.primitive_plane_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x, entrance_y, entrance_z + 2.0)
        )
        panel = bpy.context.active_object
        panel.name = f"NeoTech_RevolvingPanel_{i}"
        
        # Scale panel
        panel.scale.x = 1.2
        panel.scale.y = 0.05
        panel.scale.z = 3.8
        
        # Rotate panel
        panel.rotation_euler.z = angle
        panel.rotation_euler.x = math.radians(90)
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Assign glass material
        panel.data.materials.append(interior_materials["NeoTech_Glass"])
        
        interior_objects.append(panel)
    
    # Create central revolving axis
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.2,
        depth=4.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 2.0)
    )
    axis = bpy.context.active_object
    axis.name = "NeoTech_RevolvingAxis"
    
    # Assign material
    axis.data.materials.append(interior_materials["NeoTech_Interior"])
    
    interior_objects.append(axis)
    
    # Create security scanner archways
    for i in range(2):
        offset = 1.5 * (i - 0.5)
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x + offset, entrance_y + 3.0, entrance_z + 2.0)
        )
        scanner = bpy.context.active_object
        scanner.name = f"NeoTech_SecurityScanner_{i}"
        
        # Scale scanner
        scanner.scale.x = 0.2
        scanner.scale.y = 0.2
        scanner.scale.z = 4.0
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create scanner top
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x, entrance_y + 3.0, entrance_z + 4.0)
        )
        scanner_top = bpy.context.active_object
        scanner_top.name = f"NeoTech_SecurityScannerTop_{i}"
        
        # Scale scanner top
        scanner_top.scale.x = 3.0
        scanner_top.scale.y = 0.2
        scanner_top.scale.z = 0.2
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Assign materials
        scanner.data.materials.append(interior_materials["NeoTech_Interior"])
        scanner_top.data.materials.append(interior_materials["NeoTech_Interior"])
        
        interior_objects.append(scanner)
        interior_objects.append(scanner_top)
    
    # Create laser grid for security
    bpy.ops.mesh.primitive_grid_add(
        x_subdivisions=10,
        y_subdivisions=10,
        size=3.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y + 3.0, entrance_z + 0.1)
    )
    laser_grid = bpy.context.active_object
    laser_grid.name = "NeoTech_LaserGrid"
    
    # Assign material
    if "Militech_Accent" in materials:
        laser_grid.data.materials.append(materials["Militech_Accent"])
    
    interior_objects.append(laser_grid)
    
    # Create reception desk
    desk_objects = create_desk(
        "NeoTech_ReceptionDesk",
        (entrance_x, entrance_y + 6.0, entrance_z),
        4.0,
        1.5,
        1.0,
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.extend(desk_objects)
    
    # Create holographic AI assistant at reception
    hologram = create_hologram(
        "NeoTech_AIAssistant",
        (entrance_x, entrance_y + 6.0, entrance_z + 2.0),
        (1.0, 2.0),
        interior_materials["Hologram"]
    )
    interior_objects.append(hologram)
    
    # Create elevator shaft
    elevator_x = base_loc[0]
    elevator_y = base_loc[1] + base_radius * 0.5
    elevator_z = base_loc[2]
    
    # Create elevator shaft (glass cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=2.0,
        depth=tower.dimensions.z * 0.9,
        enter_editmode=False,
        align='WORLD',
        location=(elevator_x, elevator_y, elevator_z + tower.dimensions.z * 0.45)
    )
    elevator_shaft = bpy.context.active_object
    elevator_shaft.name = "NeoTech_ElevatorShaft"
    
    # Assign glass material
    elevator_shaft.data.materials.append(interior_materials["NeoTech_Glass"])
    
    interior_objects.append(elevator_shaft)
    
    # Create elevator platform
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=1.8,
        depth=0.2,
        enter_editmode=False,
        align='WORLD',
        location=(elevator_x, elevator_y, elevator_z + 1.0)
    )
    elevator_platform = bpy.context.active_object
    elevator_platform.name = "NeoTech_ElevatorPlatform"
    
    # Assign material
    elevator_platform.data.materials.append(interior_materials["NeoTech_Interior"])
    
    interior_objects.append(elevator_platform)
    
    # Create research lab (upper floor)
    lab_z = base_loc[2] + tower.dimensions.z * 0.3
    
    # Create lab floor
    lab_floor = create_floor(
        "NeoTech_LabFloor",
        (base_loc[0], base_loc[1], lab_z),
        (tower.dimensions.x * 0.8, tower.dimensions.y * 0.8, 0.2),
        0.1,
        interior_materials["NeoTech_Floor"]
    )
    interior_objects.append(lab_floor)
    
    # Create lab ceiling
    lab_ceiling = create_ceiling(
        "NeoTech_LabCeiling",
        (base_loc[0], base_loc[1], lab_z + 4.0),
        (tower.dimensions.x * 0.8, tower.dimensions.y * 0.8, 0.2),
        0.1,
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.append(lab_ceiling)
    
    # Create lab equipment
    for i in range(4):
        angle = i * (2 * math.pi / 4)
        equip_x = base_loc[0] + (tower.dimensions.x * 0.3) * math.cos(angle)
        equip_y = base_loc[1] + (tower.dimensions.y * 0.3) * math.sin(angle)
        
        # Create lab table
        table_objects = create_desk(
            f"NeoTech_LabTable_{i}",
            (equip_x, equip_y, lab_z),
            2.0,
            1.0,
            0.8,
            interior_materials["NeoTech_Interior"]
        )
        interior_objects.extend(table_objects)
        
        # Create computer on table
        computer_objects = create_computer(
            f"NeoTech_LabComputer_{i}",
            (equip_x, equip_y, lab_z + 0.8),
            interior_materials["NeoTech_Interior"],
            interior_materials["Hologram"]
        )
        interior_objects.extend(computer_objects)
    
    # Create server room (another upper floor)
    server_z = base_loc[2] + tower.dimensions.z * 0.6
    
    # Create server room floor
    server_floor = create_floor(
        "NeoTech_ServerFloor",
        (base_loc[0], base_loc[1], server_z),
        (tower.dimensions.x * 0.7, tower.dimensions.y * 0.7, 0.2),
        0.1,
        interior_materials["NeoTech_Floor"]
    )
    interior_objects.append(server_floor)
    
    # Create server room ceiling
    server_ceiling = create_ceiling(
        "NeoTech_ServerCeiling",
        (base_loc[0], base_loc[1], server_z + 4.0),
        (tower.dimensions.x * 0.7, tower.dimensions.y * 0.7, 0.2),
        0.1,
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.append(server_ceiling)
    
    # Create server racks
    for i in range(6):
        angle = i * (2 * math.pi / 6)
        rack_x = base_loc[0] + (tower.dimensions.x * 0.25) * math.cos(angle)
        rack_y = base_loc[1] + (tower.dimensions.y * 0.25) * math.sin(angle)
        
        rack_objects = create_server_rack(
            f"NeoTech_ServerRack_{i}",
            (rack_x, rack_y, server_z),
            interior_materials["NeoTech_Interior"],
            interior_materials["Neon_Light"]
        )
        interior_objects.extend(rack_objects)
    
    # Create data visualization in center
    data_vis = create_hologram(
        "NeoTech_DataVisualization",
        (base_loc[0], base_loc[1], server_z + 2.0),
        (3.0, 3.0),
        interior_materials["Hologram"]
    )
    # Rotate to horizontal position
    data_vis.rotation_euler.x = math.radians(90)
    interior_objects.append(data_vis)
    
    # Create executive office (top floor)
    office_z = base_loc[2] + tower.dimensions.z * 0.85
    
    # Create office floor
    office_floor = create_floor(
        "NeoTech_OfficeFloor",
        (base_loc[0], base_loc[1], office_z),
        (tower.dimensions.x * 0.6, tower.dimensions.y * 0.6, 0.2),
        0.1,
        interior_materials["NeoTech_Floor"]
    )
    interior_objects.append(office_floor)
    
    # Create office ceiling
    office_ceiling = create_ceiling(
        "NeoTech_OfficeCeiling",
        (base_loc[0], base_loc[1], office_z + 4.0),
        (tower.dimensions.x * 0.6, tower.dimensions.y * 0.6, 0.2),
        0.1,
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.append(office_ceiling)
    
    # Create executive desk
    desk_objects = create_desk(
        "NeoTech_ExecutiveDesk",
        (base_loc[0], base_loc[1], office_z),
        3.0,
        1.5,
        0.8,
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.extend(desk_objects)
    
    # Create executive chair
    chair_objects = create_chair(
        "NeoTech_ExecutiveChair",
        (base_loc[0], base_loc[1] + 1.0, office_z),
        interior_materials["NeoTech_Interior"]
    )
    interior_objects.extend(chair_objects)
    
    # Create computer on desk
    computer_objects = create_computer(
        "NeoTech_ExecutiveComputer",
        (base_loc[0], base_loc[1] - 0.5, office_z + 0.8),
        interior_materials["NeoTech_Interior"],
        interior_materials["Hologram"]
    )
    interior_objects.extend(computer_objects)
    
    # Create panoramic windows around the office
    window_segments = 8
    for i in range(window_segments):
        angle = i * (2 * math.pi / window_segments)
        window_x = base_loc[0] + (tower.dimensions.x * 0.3) * math.cos(angle)
        window_y = base_loc[1] + (tower.dimensions.y * 0.3) * math.sin(angle)
        
        # Calculate position for next segment
        next_angle = ((i + 1) % window_segments) * (2 * math.pi / window_segments)
        next_x = base_loc[0] + (tower.dimensions.x * 0.3) * math.cos(next_angle)
        next_y = base_loc[1] + (tower.dimensions.y * 0.3) * math.sin(next_angle)
        
        # Create window wall
        wall = create_wall(
            f"NeoTech_OfficeWall_{i}",
            (window_x, window_y, office_z),
            (next_x, next_y, office_z),
            4.0,
            0.2,
            interior_materials["NeoTech_Interior"],
            with_window=True,
            window_height=2.5,
            window_width=3.0
        )
        interior_objects.append(wall)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection

def create_specter_station_interior(specter_objects, materials, interior_materials):
    """Create interior spaces for Specter Station"""
    tower = specter_objects["tower"]
    collection = specter_objects["collection"]
    
    # Create a subcollection for interior objects
    if "Specter_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("Specter_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["Specter_Interior"]
    
    interior_objects = []
    
    # Get tower location
    tower_loc = tower.location
    tower_radius = tower.dimensions.x / 2
    
    # Create main concourse floor
    concourse_floor = create_floor(
        "Specter_ConcourseFloor",
        (tower_loc[0], tower_loc[1], tower_loc[2] - tower.dimensions.z / 2),
        (tower_radius * 4, tower_radius * 4, 0.2),
        0.1,
        interior_materials["Specter_Interior"]
    )
    interior_objects.append(concourse_floor)
    
    # Create concourse ceiling
    concourse_ceiling = create_ceiling(
        "Specter_ConcourseCeiling",
        (tower_loc[0], tower_loc[1], tower_loc[2] - tower.dimensions.z / 2 + 5),
        (tower_radius * 4, tower_radius * 4, 0.2),
        0.1,
        interior_materials["Specter_Interior"]
    )
    interior_objects.append(concourse_ceiling)
    
    # Create rusted sliding doors (entrance)
    entrance_x = tower_loc[0]
    entrance_y = tower_loc[1] - tower_radius * 2
    entrance_z = tower_loc[2] - tower.dimensions.z / 2
    
    # Create door frame
    door_frame = create_door(
        "Specter_EntranceDoor",
        (entrance_x, entrance_y, entrance_z),
        4.0,
        3.5,
        0.3,
        interior_materials["Specter_Interior"],
        is_open=True,
        open_angle=90
    )
    interior_objects.append(door_frame["frame"])
    interior_objects.append(door_frame["door"])
    
    # Create broken security scanner
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x + 2.0, entrance_y + 2.0, entrance_z + 1.5)
    )
    scanner = bpy.context.active_object
    scanner.name = "Specter_BrokenScanner"
    
    # Edit the scanner to make it look broken
    bm = bmesh.from_edit_mesh(scanner.data)
    
    # Scale scanner
    for v in bm.verts:
        v.co.x *= 0.5
        v.co.y *= 0.5
        v.co.z *= 3.0
    
    # Tilt it slightly
    for v in bm.verts:
        v.co.x += v.co.z * 0.1
    
    # Update mesh
    bmesh.update_edit_mesh(scanner.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Assign material
    scanner.data.materials.append(interior_materials["Specter_Interior"])
    
    interior_objects.append(scanner)
    
    # Create flickering neon sign above entrance
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 4.0)
    )
    neon_sign = bpy.context.active_object
    neon_sign.name = "Specter_NeonSign"
    
    # Scale sign
    neon_sign.scale.x = 3.0
    neon_sign.scale.y = 0.8
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign neon material
    neon_sign.data.materials.append(interior_materials["Neon_Light"])
    
    interior_objects.append(neon_sign)
    
    # Create market stalls in concourse
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
            location=(stall_x, stall_y, entrance_z + 0.5)
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
            location=(stall_x, stall_y, entrance_z + 1.5)
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
        
        # Update mesh
        bmesh.update_edit_mesh(canopy.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rotate to face center
        canopy.rotation_euler = stall.rotation_euler
        
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
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set random color
        r = random.uniform(0.2, 0.8)
        g = random.uniform(0.2, 0.8)
        b = random.uniform(0.2, 0.8)
        principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
        principled.inputs['Roughness'].default_value = 0.8
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        canopy.data.materials.append(canopy_material)
        
        interior_objects.append(stall)
        interior_objects.append(canopy)
    
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
        tunnel_entrance = create_door(
            f"Specter_TunnelEntrance_{i}",
            (tunnel_x, tunnel_y, entrance_z),
            2.0,
            3.0,
            0.3,
            interior_materials["Specter_Interior"],
            is_open=False
        )
        interior_objects.append(tunnel_entrance["frame"])
        interior_objects.append(tunnel_entrance["door"])
        
        # Create tunnel interior (just a short section)
        tunnel_length = 5.0
        tunnel_end_x = tunnel_x + direction.x * tunnel_length
        tunnel_end_y = tunnel_y + direction.y * tunnel_length
        
        # Create tunnel walls
        left_wall = create_wall(
            f"Specter_TunnelLeftWall_{i}",
            (tunnel_x, tunnel_y, entrance_z),
            (tunnel_end_x, tunnel_end_y, entrance_z),
            3.0,
            0.2,
            interior_materials["Specter_Interior"],
            with_window=False
        )
        interior_objects.append(left_wall)
        
        right_wall = create_wall(
            f"Specter_TunnelRightWall_{i}",
            (tunnel_x, tunnel_y, entrance_z),
            (tunnel_end_x, tunnel_end_y, entrance_z),
            3.0,
            0.2,
            interior_materials["Specter_Interior"],
            with_window=False
        )
        # Offset right wall
        right_wall.location.x += direction.y * 2.0
        right_wall.location.y -= direction.x * 2.0
        interior_objects.append(right_wall)
        
        # Create tunnel ceiling
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=((tunnel_x + tunnel_end_x) / 2, (tunnel_y + tunnel_end_y) / 2, entrance_z + 1.5)
        )
        ceiling = bpy.context.active_object
        ceiling.name = f"Specter_TunnelCeiling_{i}"
        
        # Scale ceiling
        ceiling.scale.x = tunnel_length
        ceiling.scale.y = 2.0
        ceiling.scale.z = 0.1
        
        # Rotate to align with tunnel
        ceiling.rotation_euler.z = math.atan2(direction.y, direction.x)
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Assign material
        ceiling.data.materials.append(interior_materials["Specter_Interior"])
        
        interior_objects.append(ceiling)
        
        # Create some living quarter items in the tunnel
        # Bed
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(tunnel_end_x - direction.x, tunnel_end_y - direction.y, entrance_z + 0.3)
        )
        bed = bpy.context.active_object
        bed.name = f"Specter_Bed_{i}"
        
        # Scale bed
        bed.scale.x = 2.0
        bed.scale.y = 1.0
        bed.scale.z = 0.3
        
        # Rotate to align with tunnel
        bed.rotation_euler.z = math.atan2(direction.y, direction.x) + math.radians(90)
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Assign material
        bed_material = bpy.data.materials.new(name=f"BedMaterial_{i}")
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
        principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.4, 1.0)
        principled.inputs['Roughness'].default_value = 0.9
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        bed.data.materials.append(bed_material)
        
        interior_objects.append(bed)
    
    # Create command center in former station control room
    command_x = tower_loc[0]
    command_y = tower_loc[1]
    command_z = entrance_z + 6.0  # Upper level
    
    # Create command center floor
    command_floor = create_floor(
        "Specter_CommandFloor",
        (command_x, command_y, command_z),
        (tower_radius * 1.5, tower_radius * 1.5, 0.2),
        0.1,
        interior_materials["Specter_Interior"]
    )
    interior_objects.append(command_floor)
    
    # Create command center ceiling
    command_ceiling = create_ceiling(
        "Specter_CommandCeiling",
        (command_x, command_y, command_z + 4.0),
        (tower_radius * 1.5, tower_radius * 1.5, 0.2),
        0.1,
        interior_materials["Specter_Interior"]
    )
    interior_objects.append(command_ceiling)
    
    # Create circular walls for command center
    wall_segments = 8
    for i in range(wall_segments):
        angle1 = i * (2 * math.pi / wall_segments)
        angle2 = ((i + 1) % wall_segments) * (2 * math.pi / wall_segments)
        
        x1 = command_x + tower_radius * 0.75 * math.cos(angle1)
        y1 = command_y + tower_radius * 0.75 * math.sin(angle1)
        x2 = command_x + tower_radius * 0.75 * math.cos(angle2)
        y2 = command_y + tower_radius * 0.75 * math.sin(angle2)
        
        # Add windows to alternating wall segments
        with_window = (i % 2 == 0)
        
        wall = create_wall(
            f"Specter_CommandWall_{i}",
            (x1, y1, command_z),
            (x2, y2, command_z),
            4.0,
            0.2,
            interior_materials["Specter_Interior"],
            with_window=with_window
        )
        interior_objects.append(wall)
    
    # Create command center equipment
    # Central table
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=2.0,
        depth=0.2,
        enter_editmode=False,
        align='WORLD',
        location=(command_x, command_y, command_z + 1.0)
    )
    table = bpy.context.active_object
    table.name = "Specter_CommandTable"
    
    # Assign material
    table.data.materials.append(interior_materials["Specter_Interior"])
    
    interior_objects.append(table)
    
    # Create holographic display on table
    hologram = create_hologram(
        "Specter_CommandHologram",
        (command_x, command_y, command_z + 1.5),
        (3.0, 3.0),
        interior_materials["Hologram"]
    )
    # Rotate to horizontal position
    hologram.rotation_euler.x = math.radians(90)
    interior_objects.append(hologram)
    
    # Create chairs around table
    chair_count = 6
    for i in range(chair_count):
        angle = i * (2 * math.pi / chair_count)
        chair_x = command_x + 3.0 * math.cos(angle)
        chair_y = command_y + 3.0 * math.sin(angle)
        
        chair_objects = create_chair(
            f"Specter_CommandChair_{i}",
            (chair_x, chair_y, command_z),
            interior_materials["Specter_Interior"]
        )
        
        # Rotate to face center
        for obj in chair_objects:
            direction = Vector((command_x, command_y, 0)) - Vector((chair_x, chair_y, 0))
            rot_quat = direction.to_track_quat('Y', 'Z')
            obj.rotation_euler = rot_quat.to_euler()
        
        interior_objects.extend(chair_objects)
    
    # Create hidden storage areas behind false walls
    storage_x = command_x + tower_radius * 0.75
    storage_y = command_y
    
    # Create false wall
    false_wall = create_wall(
        "Specter_FalseWall",
        (storage_x - 1.0, storage_y - 1.0, command_z),
        (storage_x - 1.0, storage_y + 1.0, command_z),
        4.0,
        0.2,
        interior_materials["Specter_Interior"],
        with_window=False
    )
    interior_objects.append(false_wall)
    
    # Create storage area behind false wall
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(storage_x + 1.0, storage_y, command_z + 1.0)
    )
    storage = bpy.context.active_object
    storage.name = "Specter_HiddenStorage"
    
    # Scale storage
    storage.scale.x = 2.0
    storage.scale.y = 2.0
    storage.scale.z = 2.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    storage.data.materials.append(interior_materials["Specter_Interior"])
    
    interior_objects.append(storage)
    
    # Add graffiti on walls (just a plane with texture)
    for i in range(4):
        angle = i * (math.pi / 2)
        graffiti_x = entrance_x + 8.0 * math.cos(angle)
        graffiti_y = entrance_y + 8.0 * math.sin(angle)
        
        bpy.ops.mesh.primitive_plane_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(graffiti_x, graffiti_y, entrance_z + 2.0)
        )
        graffiti = bpy.context.active_object
        graffiti.name = f"Specter_Graffiti_{i}"
        
        # Scale graffiti
        graffiti.scale.x = 3.0
        graffiti.scale.y = 2.0
        
        # Rotate to face center
        direction = Vector((entrance_x, entrance_y, 0)) - Vector((graffiti_x, graffiti_y, 0))
        rot_quat = direction.to_track_quat('Z', 'Y')
        graffiti.rotation_euler = rot_quat.to_euler()
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Create graffiti material
        graffiti_material = bpy.data.materials.new(name=f"Graffiti_{i}")
        graffiti_material.use_nodes = True
        nodes = graffiti_material.node_tree.nodes
        links = graffiti_material.node_tree.links
        
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
        
        graffiti.data.materials.append(graffiti_material)
        
        interior_objects.append(graffiti)
    
    # Create flickering lights
    for i in range(10):
        light_x = entrance_x + random.uniform(-10.0, 10.0)
        light_y = entrance_y + random.uniform(-10.0, 10.0)
        light_z = entrance_z + 4.8
        
        bpy.ops.mesh.primitive_plane_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(light_x, light_y, light_z)
        )
        light = bpy.context.active_object
        light.name = f"Specter_FlickeringLight_{i}"
        
        # Scale light
        light.scale.x = 0.5
        light.scale.y = 0.5
        
        # Rotate to face down
        light.rotation_euler.x = math.radians(180)
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Create light material
        light_material = bpy.data.materials.new(name=f"FlickeringLight_{i}")
        light_material.use_nodes = True
        nodes = light_material.node_tree.nodes
        links = light_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties
        emission.inputs['Color'].default_value = (1.0, 0.9, 0.7, 1.0)  # Warm light
        emission.inputs['Strength'].default_value = 3.0
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        light.data.materials.append(light_material)
        
        interior_objects.append(light)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection



def create_biotechnica_spire_interior(biotechnica_objects, materials, interior_materials):
    """	Create interior spaces for Biotechnica Spire (Upper Tier)
		Neon Crucible - Biotechnica Spire Interior Implementation
		Blender 4.2 Python Script for generating interior spaces, entrances, doors, and windows
		for the Biotechnica Spire building in the Neon Crucible cyberpunk world.
	"""
    # Extract objects from the biotechnica_objects dictionary
    building = biotechnica_objects.get("tower")
    dome = biotechnica_objects.get("dome") # Get dome too if needed
    collection = biotechnica_objects.get("collection")
    
    if not building or not dome or not collection:
        print("Error: Missing required Biotechnica Spire objects")
        return None
    
    # Create a subcollection for interior objects
    if "Biotechnica_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("Biotechnica_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["Biotechnica_Interior"]
    
    interior_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create organic-looking sliding doors resembling cell division
    entrance_x = building_loc[0]
    entrance_y = building_loc[1] - building_size.y/2
    entrance_z = building_loc[2]
    
    # Create door frame with organic shape
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=2.0,
        depth=0.5,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 2.0)
    )
    door_frame = bpy.context.active_object
    door_frame.name = "Biotechnica_DoorFrame"
    
    # Edit the door frame to make it organic
    bm = bmesh.from_edit_mesh(door_frame.data)
    
    # Rotate to face outward
    for v in bm.verts:
        temp = v.co.y
        v.co.y = v.co.z
        v.co.z = temp
    
    # Make it slightly irregular for organic look
    for v in bm.verts:
        angle = math.atan2(v.co.x, v.co.z)
        radius = math.sqrt(v.co.x**2 + v.co.z**2)
        # Add sine wave variation to radius
        new_radius = radius * (1.0 + 0.1 * math.sin(8 * angle))
        v.co.x = new_radius * math.sin(angle)
        v.co.z = new_radius * math.cos(angle)
    
    # Update mesh
    bmesh.update_edit_mesh(door_frame.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create door frame material
    frame_material = bpy.data.materials.new(name="Biotechnica_FrameMaterial")
    frame_material.use_nodes = True
    nodes = frame_material.node_tree.nodes
    links = frame_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.2, 1.0)  # Green-tinted
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.2
    #principled.inputs['Clearcoat'].default_value = 0.5
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    door_frame.data.materials.append(frame_material)
    
    interior_objects.append(door_frame)
    
    # Create sliding door panels (resembling cell division)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=1.8,
            depth=0.2,
            enter_editmode=True,
            align='WORLD',
            location=(entrance_x + side * 0.9, entrance_y - 0.1, entrance_z + 2.0)
        )
        door_panel = bpy.context.active_object
        door_panel.name = f"Biotechnica_DoorPanel_{side}"
        
        # Edit the door panel to make it organic and half-circle
        bm = bmesh.from_edit_mesh(door_panel.data)
        
        # Rotate to face outward
        for v in bm.verts:
            temp = v.co.y
            v.co.y = v.co.z
            v.co.z = temp
        
        # Make it a half-circle
        for v in bm.verts:
            if (side < 0 and v.co.x > 0) or (side > 0 and v.co.x < 0):
                v.co.x = 0
        
        # Make it slightly irregular for organic look
        for v in bm.verts:
            angle = math.atan2(v.co.x, v.co.z)
            radius = math.sqrt(v.co.x**2 + v.co.z**2)
            # Add sine wave variation to radius
            new_radius = radius * (1.0 + 0.1 * math.sin(6 * angle))
            v.co.x = new_radius * math.sin(angle)
            v.co.z = new_radius * math.cos(angle)
        
        # Update mesh
        bmesh.update_edit_mesh(door_panel.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Create door panel material
        panel_material = bpy.data.materials.new(name=f"Biotechnica_PanelMaterial_{side}")
        panel_material.use_nodes = True
        nodes = panel_material.node_tree.nodes
        links = panel_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.2, 1.0)  # Green-tinted
        principled.inputs['Metallic'].default_value = 0.3
        principled.inputs['Roughness'].default_value = 0.3
        #principled.inputs['Transmission'].default_value = 0.2  # Slightly transparent
        principled.inputs['IOR'].default_value = 1.45
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        door_panel.data.materials.append(panel_material)
        
        interior_objects.append(door_panel)
    
    # Create decontamination chamber airlock
    airlock_y = entrance_y - 3.0
    
    # Create airlock chamber
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=2.5,
        depth=4.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, airlock_y, entrance_z + 2.0)
    )
    airlock = bpy.context.active_object
    airlock.name = "Biotechnica_Airlock"
    
    # Rotate to align with entrance
    airlock.rotation_euler.x = math.radians(90)
    
    # Apply rotation
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Create airlock material
    airlock_material = bpy.data.materials.new(name="Biotechnica_AirlockMaterial")
    airlock_material.use_nodes = True
    nodes = airlock_material.node_tree.nodes
    links = airlock_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.3
    principled.inputs['Roughness'].default_value = 0.2
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    airlock.data.materials.append(airlock_material)
    
    interior_objects.append(airlock)
    
    # Create inner airlock door
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=2.0,
        depth=0.2,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, airlock_y - 2.0, entrance_z + 2.0)
    )
    inner_door = bpy.context.active_object
    inner_door.name = "Biotechnica_InnerDoor"
    
    # Rotate to align with entrance
    inner_door.rotation_euler.x = math.radians(90)
    
    # Apply rotation
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Create inner door material
    inner_door_material = bpy.data.materials.new(name="Biotechnica_InnerDoorMaterial")
    inner_door_material.use_nodes = True
    nodes = inner_door_material.node_tree.nodes
    links = inner_door_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.2, 1.0)  # Green-tinted
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.2
    #principled.inputs['Transmission'].default_value = 0.3  # Slightly transparent
    principled.inputs['IOR'].default_value = 1.45
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    inner_door.data.materials.append(inner_door_material)
    
    interior_objects.append(inner_door)
    
    # Create decontamination spray nozzles
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        nozzle_x = entrance_x + 2.0 * math.cos(angle)
        nozzle_y = airlock_y
        nozzle_z = entrance_z + 2.0 + 2.0 * math.sin(angle)
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.1,
            depth=0.3,
            enter_editmode=False,
            align='WORLD',
            location=(nozzle_x, nozzle_y, nozzle_z)
        )
        nozzle = bpy.context.active_object
        nozzle.name = f"Biotechnica_Nozzle_{i}"
        
        # Point toward center
        direction = Vector((entrance_x, airlock_y, entrance_z + 2.0)) - Vector((nozzle_x, nozzle_y, nozzle_z))
        rot_quat = direction.to_track_quat('Z', 'Y')
        nozzle.rotation_euler = rot_quat.to_euler()
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create nozzle material
        nozzle_material = bpy.data.materials.new(name=f"Biotechnica_NozzleMaterial_{i}")
        nozzle_material.use_nodes = True
        nodes = nozzle_material.node_tree.nodes
        links = nozzle_material.node_tree.links
        
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
        nozzle.data.materials.append(nozzle_material)
        
        interior_objects.append(nozzle)
    
    # Create green-tinted glass with corporate logo
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y + 0.1, entrance_z + 4.0)
    )
    logo_glass = bpy.context.active_object
    logo_glass.name = "Biotechnica_LogoGlass"
    
    # Scale logo glass
    logo_glass.scale.x = 3.0
    logo_glass.scale.y = 1.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create logo glass material
    logo_glass_material = bpy.data.materials.new(name="Biotechnica_LogoGlassMaterial")
    logo_glass_material.use_nodes = True
    nodes = logo_glass_material.node_tree.nodes
    links = logo_glass_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set properties
    emission.inputs['Color'].default_value = (0.1, 0.8, 0.3, 1.0)  # Green
    emission.inputs['Strength'].default_value = 1.5
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    logo_glass.data.materials.append(logo_glass_material)
    
    interior_objects.append(logo_glass)
    
    # Create atrium with plant wall
    atrium_y = airlock_y - 8.0
    atrium_height = 10.0
    atrium_width = building_size.x * 0.8
    atrium_depth = building_size.y * 0.4
    
    # Create atrium space
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, atrium_y, entrance_z + atrium_height/2)
    )
    atrium = bpy.context.active_object
    atrium.name = "Biotechnica_Atrium"
    
    # Scale atrium
    atrium.scale.x = atrium_width/2
    atrium.scale.y = atrium_depth/2
    atrium.scale.z = atrium_height/2
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create atrium material
    atrium_material = bpy.data.materials.new(name="Biotechnica_AtriumMaterial")
    atrium_material.use_nodes = True
    nodes = atrium_material.node_tree.nodes
    links = atrium_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.1
    principled.inputs['Roughness'].default_value = 0.2
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    atrium.data.materials.append(atrium_material)
    
    interior_objects.append(atrium)
    
    # Create living plant wall
    plant_wall_y = atrium_y + atrium_depth/2 - 0.1
    plant_wall_width = atrium_width * 0.9
    plant_wall_height = atrium_height * 0.8
    
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x, plant_wall_y, entrance_z + plant_wall_height/2)
    )
    plant_wall = bpy.context.active_object
    plant_wall.name = "Biotechnica_PlantWall"
    
    # Scale plant wall
    plant_wall.scale.x = plant_wall_width/2
    plant_wall.scale.z = plant_wall_height/2
    
    # Rotate to face inward
    plant_wall.rotation_euler.x = math.radians(90)
    
    # Apply transformations
    try:
	    if bpy.context.mode != 'OBJECT':
	        bpy.ops.object.mode_set(mode='OBJECT')
	    bpy.ops.object.select_all(action='DESELECT')
	    plant_wall.select_set(True)
	    bpy.context.view_layer.objects.active = plant_wall
	    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True) # Apply rotation and scale
    except RuntimeError as e:
	    print(f"ERROR applying transform to '{plant_wall.name}': {e}")
	    # Add context printing if needed
	# --- End Apply Transform ---
	
	
	# --- FIX: Switch to Edit Mode BEFORE bmesh operations ---
    try:
	    # Ensure the correct object is active
	    bpy.ops.object.select_all(action='DESELECT')
	    plant_wall.select_set(True)
	    bpy.context.view_layer.objects.active = plant_wall
	    # Switch to Edit Mode
	    bpy.ops.object.mode_set(mode='EDIT')
    except RuntimeError as e:
	    print(f"ERROR entering Edit Mode for '{plant_wall.name}': {e}")
	    # If we can't enter edit mode, we can't do the bmesh part
	    return None # Or handle differently

    # Add displacement to create plant-like surface
    bm = bmesh.from_edit_mesh(plant_wall.data)
    
    # Subdivide the plane for more detail
    for face in bm.faces:
        bmesh.ops.subdivide_edges(bm, edges=face.edges, cuts=20)
    
    # Add random displacement for plant-like appearance
    for v in bm.verts:
        v.co.y += random.uniform(0.0, 0.3)  # Random depth
    
    # Update mesh
    bmesh.update_edit_mesh(plant_wall.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create plant wall material
    plant_material = bpy.data.materials.new(name="Biotechnica_PlantMaterial")
    plant_material.use_nodes = True
    nodes = plant_material.node_tree.nodes
    links = plant_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    noise = nodes.new(type='ShaderNodeTexNoise')
    mapping = nodes.new(type='ShaderNodeMapping')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    
    # Set properties
    principled.inputs['Roughness'].default_value = 0.8
    #principled.inputs['Specular'].default_value = 0.1
    
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 8.0
    
    # Setup color ramp for different plant colors
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.0, 0.3, 0.0, 1.0)  # Dark green
    
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.2, 0.8, 0.2, 1.0)  # Light green
    
    # Add more color variations
    pos1 = color_ramp.color_ramp.elements.new(0.3)
    pos1.color = (0.1, 0.5, 0.1, 1.0)
    
    pos2 = color_ramp.color_ramp.elements.new(0.6)
    pos2.color = (0.15, 0.6, 0.15, 1.0)
    
    pos3 = color_ramp.color_ramp.elements.new(0.8)
    pos3.color = (0.3, 0.7, 0.2, 1.0)
    
    # Connect nodes
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    plant_wall.data.materials.append(plant_material)
    
    interior_objects.append(plant_wall)
    
    # Create water feature in atrium
    water_feature_radius = 3.0
    
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=water_feature_radius,
        depth=0.5,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, atrium_y, entrance_z + 0.25)
    )
    water_feature = bpy.context.active_object
    water_feature.name = "Biotechnica_WaterFeature"
    
    # Create water feature material
    water_material = bpy.data.materials.new(name="Biotechnica_WaterMaterial")
    water_material.use_nodes = True
    nodes = water_material.node_tree.nodes
    links = water_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties for water-like appearance
    principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.4, 1.0)  # Blue-green
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.1
    #SSprincipled.inputs['Transmission'].default_value = 0.8
    principled.inputs['IOR'].default_value = 1.33  # Water IOR
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    water_feature.data.materials.append(water_material)
    
    interior_objects.append(water_feature)
    
    # Create research labs
    lab_y = atrium_y - atrium_depth/2 - 5.0
    lab_width = 8.0
    lab_depth = 10.0
    lab_height = 4.0
    
    # Create multiple research labs
    for i in range(3):
        lab_x = entrance_x + (i - 1) * (lab_width + 2.0)
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(lab_x, lab_y, entrance_z + lab_height/2)
        )
        lab = bpy.context.active_object
        lab.name = f"Biotechnica_ResearchLab_{i}"
        
        # Scale lab
        lab.scale.x = lab_width/2
        lab.scale.y = lab_depth/2
        lab.scale.z = lab_height/2
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create lab material
        lab_material = bpy.data.materials.new(name=f"Biotechnica_LabMaterial_{i}")
        lab_material.use_nodes = True
        nodes = lab_material.node_tree.nodes
        links = lab_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # White
        principled.inputs['Metallic'].default_value = 0.2
        principled.inputs['Roughness'].default_value = 0.3
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        lab.data.materials.append(lab_material)
        
        interior_objects.append(lab)
        
        # Add lab equipment
        # Lab table
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(lab_x, lab_y, entrance_z + 1.0)
        )
        lab_table = bpy.context.active_object
        lab_table.name = f"Biotechnica_LabTable_{i}"
        
        # Scale table
        lab_table.scale.x = lab_width/2 - 1.0
        lab_table.scale.y = lab_depth/2 - 1.0
        lab_table.scale.z = 0.1
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create table material
        table_material = bpy.data.materials.new(name=f"Biotechnica_TableMaterial_{i}")
        table_material.use_nodes = True
        nodes = table_material.node_tree.nodes
        links = table_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
        principled.inputs['Metallic'].default_value = 0.5
        principled.inputs['Roughness'].default_value = 0.2
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        lab_table.data.materials.append(table_material)
        
        interior_objects.append(lab_table)
        
        # Add specimen containers
        for j in range(3):
            container_x = lab_x + (j - 1) * 1.5
            
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=0.4,
                depth=1.5,
                enter_editmode=False,
                align='WORLD',
                location=(container_x, lab_y, entrance_z + 1.85)
            )
            container = bpy.context.active_object
            container.name = f"Biotechnica_SpecimenContainer_{i}_{j}"
            
            # Create container material
            container_material = bpy.data.materials.new(name=f"Biotechnica_ContainerMaterial_{i}_{j}")
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
            principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
            principled.inputs['Metallic'].default_value = 0.0
            principled.inputs['Roughness'].default_value = 0.1
            #principled.inputs['Transmission'].default_value = 0.9
            principled.inputs['IOR'].default_value = 1.45
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            container.data.materials.append(container_material)
            
            interior_objects.append(container)
            
            # Add specimen inside container
            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=2,
                radius=0.3,
                enter_editmode=False,
                align='WORLD',
                location=(container_x, lab_y, entrance_z + 1.85)
            )
            specimen = bpy.context.active_object
            specimen.name = f"Biotechnica_Specimen_{i}_{j}"
            
            # Create specimen material
            specimen_material = bpy.data.materials.new(name=f"Biotechnica_SpecimenMaterial_{i}_{j}")
            specimen_material.use_nodes = True
            nodes = specimen_material.node_tree.nodes
            links = specimen_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            emission = nodes.new(type='ShaderNodeEmission')
            
            # Set properties - different colors for different specimens
            colors = [
                (0.1, 0.8, 0.3, 1.0),  # Green
                (0.3, 0.1, 0.8, 1.0),  # Purple
                (0.8, 0.3, 0.1, 1.0),  # Orange
            ]
            emission.inputs['Color'].default_value = colors[j]
            emission.inputs['Strength'].default_value = 0.5
            
            # Connect nodes
            links.new(emission.outputs['Emission'], output.inputs['Surface'])
            
            # Assign material
            specimen.data.materials.append(specimen_material)
            
            interior_objects.append(specimen)
    
    # Create hydroponic gardens
    garden_y = lab_y - lab_depth - 5.0
    garden_width = 20.0
    garden_depth = 15.0
    garden_height = 4.0
    
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, garden_y, entrance_z + garden_height/2)
    )
    garden = bpy.context.active_object
    garden.name = "Biotechnica_HydroponicGarden"
    
    # Scale garden
    garden.scale.x = garden_width/2
    garden.scale.y = garden_depth/2
    garden.scale.z = garden_height/2
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create garden material
    garden_material = bpy.data.materials.new(name="Biotechnica_GardenMaterial")
    garden_material.use_nodes = True
    nodes = garden_material.node_tree.nodes
    links = garden_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.2
    principled.inputs['Roughness'].default_value = 0.3
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    garden.data.materials.append(garden_material)
    
    interior_objects.append(garden)
    
    # Create hydroponic rows
    row_count = 5
    row_spacing = garden_width / (row_count + 1)
    
    for i in range(row_count):
        row_x = entrance_x - garden_width/2 + (i + 1) * row_spacing
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(row_x, garden_y, entrance_z + 1.0)
        )
        hydro_row = bpy.context.active_object
        hydro_row.name = f"Biotechnica_HydroponicRow_{i}"
        
        # Scale row
        hydro_row.scale.x = 0.5
        hydro_row.scale.y = garden_depth/2 - 1.0
        hydro_row.scale.z = 0.2
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create row material
        row_material = bpy.data.materials.new(name=f"Biotechnica_RowMaterial_{i}")
        row_material.use_nodes = True
        nodes = row_material.node_tree.nodes
        links = row_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Light gray
        principled.inputs['Metallic'].default_value = 0.8
        principled.inputs['Roughness'].default_value = 0.2
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        hydro_row.data.materials.append(row_material)
        
        interior_objects.append(hydro_row)
        
        # Create plants in hydroponic row
        plant_count = 10
        plant_spacing = (garden_depth - 2.0) / plant_count
        
        for j in range(plant_count):
            plant_y = garden_y - garden_depth/2 + 1.0 + j * plant_spacing
            
            # Create plant base
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8,
                radius=0.2,
                depth=0.3,
                enter_editmode=False,
                align='WORLD',
                location=(row_x, plant_y, entrance_z + 1.35)
            )
            plant_base = bpy.context.active_object
            plant_base.name = f"Biotechnica_PlantBase_{i}_{j}"
            
            # Create plant base material
            base_material = bpy.data.materials.new(name=f"Biotechnica_BaseMaterial_{i}_{j}")
            base_material.use_nodes = True
            nodes = base_material.node_tree.nodes
            links = base_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties
            principled.inputs['Base Color'].default_value = (0.3, 0.2, 0.1, 1.0)  # Brown
            principled.inputs['Roughness'].default_value = 0.8
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            plant_base.data.materials.append(base_material)
            
            interior_objects.append(plant_base)
            
            # Create plant
            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions=2,
                radius=0.4,
                enter_editmode=True,
                align='WORLD',
                location=(row_x, plant_y, entrance_z + 1.9)
            )
            plant = bpy.context.active_object
            plant.name = f"Biotechnica_Plant_{i}_{j}"
            
            # Deform plant to make it look more organic
            bm = bmesh.from_edit_mesh(plant.data)
            
            # Add random displacement for plant-like appearance
            for v in bm.verts:
                v.co.x += random.uniform(-0.1, 0.1)
                v.co.y += random.uniform(-0.1, 0.1)
                v.co.z += random.uniform(-0.1, 0.1)
            
            # Update mesh
            bmesh.update_edit_mesh(plant.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Create plant material
            plant_material = bpy.data.materials.new(name=f"Biotechnica_PlantMaterial_{i}_{j}")
            plant_material.use_nodes = True
            nodes = plant_material.node_tree.nodes
            links = plant_material.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Set properties - vary colors for different plants
            hue = (i * plant_count + j) / (row_count * plant_count)
            plant_color = (0.1 + 0.2 * hue, 0.5 - 0.2 * hue, 0.1, 1.0)
            principled.inputs['Base Color'].default_value = plant_color
            principled.inputs['Roughness'].default_value = 0.8
            #principled.inputs['Specular'].default_value = 0.1
            
            # Connect nodes
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            # Assign material
            plant.data.materials.append(plant_material)
            
            interior_objects.append(plant)
    
    # Create medical testing facilities
    medical_y = garden_y - garden_depth - 5.0
    medical_width = 15.0
    medical_depth = 12.0
    medical_height = 4.0
    
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, medical_y, entrance_z + medical_height/2)
    )
    medical = bpy.context.active_object
    medical.name = "Biotechnica_MedicalFacility"
    
    # Scale medical facility
    medical.scale.x = medical_width/2
    medical.scale.y = medical_depth/2
    medical.scale.z = medical_height/2
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create medical facility material
    medical_material = bpy.data.materials.new(name="Biotechnica_MedicalMaterial")
    medical_material.use_nodes = True
    nodes = medical_material.node_tree.nodes
    links = medical_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.1
    principled.inputs['Roughness'].default_value = 0.2
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    medical.data.materials.append(medical_material)
    
    interior_objects.append(medical)
    
    # Create medical equipment
    # Examination table
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, medical_y, entrance_z + 1.0)
    )
    exam_table = bpy.context.active_object
    exam_table.name = "Biotechnica_ExamTable"
    
    # Scale table
    exam_table.scale.x = 1.0
    exam_table.scale.y = 2.5
    exam_table.scale.z = 0.5
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create table material
    table_material = bpy.data.materials.new(name="Biotechnica_ExamTableMaterial")
    table_material.use_nodes = True
    nodes = table_material.node_tree.nodes
    links = table_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.3
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    exam_table.data.materials.append(table_material)
    
    interior_objects.append(exam_table)
    
    # Create medical scanner
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=2.0,
        depth=0.5,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, medical_y, entrance_z + 3.0)
    )
    scanner = bpy.context.active_object
    scanner.name = "Biotechnica_MedicalScanner"
    
    # Create scanner material
    scanner_material = bpy.data.materials.new(name="Biotechnica_ScannerMaterial")
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
    principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.7
    principled.inputs['Roughness'].default_value = 0.2
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    scanner.data.materials.append(scanner_material)
    
    interior_objects.append(scanner)
    
    # Create scanner light
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, medical_y, entrance_z + 2.7)
    )
    scanner_light = bpy.context.active_object
    scanner_light.name = "Biotechnica_ScannerLight"
    
    # Scale light
    scanner_light.scale.x = 1.8
    scanner_light.scale.y = 1.8
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create light material
    light_material = bpy.data.materials.new(name="Biotechnica_ScannerLightMaterial")
    light_material.use_nodes = True
    nodes = light_material.node_tree.nodes
    links = light_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set properties
    emission.inputs['Color'].default_value = (0.0, 0.8, 0.2, 1.0)  # Green
    emission.inputs['Strength'].default_value = 2.0
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    scanner_light.data.materials.append(light_material)
    
    interior_objects.append(scanner_light)
    
    # Create executive offices
    exec_y = medical_y - medical_depth - 5.0
    exec_width = 10.0
    exec_depth = 8.0
    exec_height = 4.0
    
    # Create multiple executive offices
    for i in range(3):
        exec_x = entrance_x + (i - 1) * (exec_width + 2.0)
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(exec_x, exec_y, entrance_z + exec_height/2)
        )
        exec_office = bpy.context.active_object
        exec_office.name = f"Biotechnica_ExecutiveOffice_{i}"
        
        # Scale office
        exec_office.scale.x = exec_width/2
        exec_office.scale.y = exec_depth/2
        exec_office.scale.z = exec_height/2
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create office material
        office_material = bpy.data.materials.new(name=f"Biotechnica_OfficeMaterial_{i}")
        office_material.use_nodes = True
        nodes = office_material.node_tree.nodes
        links = office_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
        principled.inputs['Metallic'].default_value = 0.1
        principled.inputs['Roughness'].default_value = 0.3
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        exec_office.data.materials.append(office_material)
        
        interior_objects.append(exec_office)
        
        # Create desk
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(exec_x, exec_y + exec_depth/4, entrance_z + 1.0)
        )
        desk = bpy.context.active_object
        desk.name = f"Biotechnica_ExecutiveDesk_{i}"
        
        # Scale desk
        desk.scale.x = exec_width/2 - 1.0
        desk.scale.y = 1.0
        desk.scale.z = 0.1
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create desk material
        desk_material = bpy.data.materials.new(name=f"Biotechnica_DeskMaterial_{i}")
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
        principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.2, 1.0)  # Green-tinted
        principled.inputs['Metallic'].default_value = 0.5
        principled.inputs['Roughness'].default_value = 0.2
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        desk.data.materials.append(desk_material)
        
        interior_objects.append(desk)
        
        # Create biometric scanner on desk
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.3,
            depth=0.2,
            enter_editmode=False,
            align='WORLD',
            location=(exec_x, exec_y + exec_depth/4 + 0.5, entrance_z + 1.15)
        )
        biometric = bpy.context.active_object
        biometric.name = f"Biotechnica_BiometricScanner_{i}"
        
        # Create biometric scanner material
        biometric_material = bpy.data.materials.new(name=f"Biotechnica_BiometricMaterial_{i}")
        biometric_material.use_nodes = True
        nodes = biometric_material.node_tree.nodes
        links = biometric_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties
        emission.inputs['Color'].default_value = (0.0, 0.8, 0.2, 1.0)  # Green
        emission.inputs['Strength'].default_value = 1.0
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Assign material
        biometric.data.materials.append(biometric_material)
        
        interior_objects.append(biometric)
    
    # Create secret research area
    secret_y = exec_y - exec_depth - 10.0
    secret_width = 15.0
    secret_depth = 15.0
    secret_height = 5.0
    
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, secret_y, entrance_z + secret_height/2)
    )
    secret_area = bpy.context.active_object
    secret_area.name = "Biotechnica_SecretResearch"
    
    # Scale secret area
    secret_area.scale.x = secret_width/2
    secret_area.scale.y = secret_depth/2
    secret_area.scale.z = secret_height/2
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create secret area material
    secret_material = bpy.data.materials.new(name="Biotechnica_SecretMaterial")
    secret_material.use_nodes = True
    nodes = secret_material.node_tree.nodes
    links = secret_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.3
    principled.inputs['Roughness'].default_value = 0.4
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    secret_area.data.materials.append(secret_material)
    
    interior_objects.append(secret_area)
    
    # Create large specimen containment in center
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=3.0,
        depth=4.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, secret_y, entrance_z + 2.5)
    )
    containment = bpy.context.active_object
    containment.name = "Biotechnica_SpecimenContainment"
    
    # Create containment material
    containment_material = bpy.data.materials.new(name="Biotechnica_ContainmentMaterial")
    containment_material.use_nodes = True
    nodes = containment_material.node_tree.nodes
    links = containment_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.1
    #principled.inputs['Transmission'].default_value = 0.9
    principled.inputs['IOR'].default_value = 1.45
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    containment.data.materials.append(containment_material)
    
    interior_objects.append(containment)
    
    # Create exotic specimen inside containment
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3,
        radius=2.0,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x, secret_y, entrance_z + 2.5)
    )
    exotic_specimen = bpy.context.active_object
    exotic_specimen.name = "Biotechnica_ExoticSpecimen"
    
    # Deform specimen to make it look alien
    bm = bmesh.from_edit_mesh(exotic_specimen.data)
    
    # Add random displacement for organic appearance
    for v in bm.verts:
        angle = math.atan2(v.co.x, v.co.y)
        radius = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
        # Add sine wave variation to radius
        new_radius = radius * (1.0 + 0.3 * math.sin(5 * angle))
        v.co.x = new_radius * math.sin(angle) * math.cos(v.co.z)
        v.co.y = new_radius * math.cos(angle) * math.cos(v.co.z)
        v.co.z = new_radius * math.sin(v.co.z)
    
    # Update mesh
    bmesh.update_edit_mesh(exotic_specimen.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create specimen material
    specimen_material = bpy.data.materials.new(name="Biotechnica_ExoticSpecimenMaterial")
    specimen_material.use_nodes = True
    nodes = specimen_material.node_tree.nodes
    links = specimen_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    noise = nodes.new(type='ShaderNodeTexNoise')
    mapping = nodes.new(type='ShaderNodeMapping')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    
    # Set properties
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 8.0
    
    # Setup color ramp for bioluminescent effect
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.0, 0.5, 0.2, 1.0)  # Dark green
    
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (0.0, 0.9, 0.4, 1.0)  # Bright green
    
    # Add more color variations
    pos1 = color_ramp.color_ramp.elements.new(0.3)
    pos1.color = (0.0, 0.6, 0.3, 1.0)
    
    pos2 = color_ramp.color_ramp.elements.new(0.7)
    pos2.color = (0.0, 0.8, 0.3, 1.0)
    
    emission.inputs['Strength'].default_value = 1.0
    
    # Connect nodes
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    exotic_specimen.data.materials.append(specimen_material)
    
    interior_objects.append(exotic_specimen)
    
    # Create workstations around containment
    for i in range(6):
        angle = i * (2 * math.pi / 6)
        station_x = entrance_x + 5.0 * math.cos(angle)
        station_y = secret_y + 5.0 * math.sin(angle)
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(station_x, station_y, entrance_z + 1.0)
        )
        workstation = bpy.context.active_object
        workstation.name = f"Biotechnica_SecretWorkstation_{i}"
        
        # Scale workstation
        workstation.scale.x = 1.0
        workstation.scale.y = 1.0
        workstation.scale.z = 0.1
        
        # Rotate to face center
        direction = Vector((entrance_x, secret_y, 0)) - Vector((station_x, station_y, 0))
        rot_quat = direction.to_track_quat('Y', 'Z')
        workstation.rotation_euler = rot_quat.to_euler()
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Create workstation material
        workstation_material = bpy.data.materials.new(name=f"Biotechnica_WorkstationMaterial_{i}")
        workstation_material.use_nodes = True
        nodes = workstation_material.node_tree.nodes
        links = workstation_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
        principled.inputs['Metallic'].default_value = 0.7
        principled.inputs['Roughness'].default_value = 0.2
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        workstation.data.materials.append(workstation_material)
        
        interior_objects.append(workstation)
        
        # Create holographic display
        bpy.ops.mesh.primitive_plane_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(station_x, station_y, entrance_z + 1.5)
        )
        holo_display = bpy.context.active_object
        holo_display.name = f"Biotechnica_HoloDisplay_{i}"
        
        # Scale display
        holo_display.scale.x = 0.8
        holo_display.scale.y = 0.5
        
        # Rotate to face center
        holo_display.rotation_euler = workstation.rotation_euler
        
        # Apply transformations
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Create display material
        display_material = bpy.data.materials.new(name=f"Biotechnica_DisplayMaterial_{i}")
        display_material.use_nodes = True
        nodes = display_material.node_tree.nodes
        links = display_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties - different colors for different displays
        colors = [
            (0.0, 0.8, 0.2, 1.0),  # Green
            (0.2, 0.0, 0.8, 1.0),  # Blue
            (0.8, 0.0, 0.2, 1.0),  # Red
            (0.8, 0.8, 0.0, 1.0),  # Yellow
            (0.0, 0.8, 0.8, 1.0),  # Cyan
            (0.8, 0.0, 0.8, 1.0),  # Magenta
        ]
        emission.inputs['Color'].default_value = colors[i]
        emission.inputs['Strength'].default_value = 1.5
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Assign material
        holo_display.data.materials.append(display_material)
        
        interior_objects.append(holo_display)
    
    # Add bioluminescent lighting throughout the building
    # Create transparent tubes with flowing colored liquids
    tube_count = 10
    tube_radius = 0.2
    
    for i in range(tube_count):
        # Create a path for the tube
        start_x = entrance_x - building_size.x/2 + random.uniform(2.0, building_size.x - 4.0)
        start_y = entrance_y - random.uniform(2.0, 5.0)
        end_y = secret_y - random.uniform(2.0, 5.0)
        
        # Create tube
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=tube_radius,
            depth=abs(end_y - start_y),
            enter_editmode=False,
            align='WORLD',
            location=(start_x, (start_y + end_y)/2, entrance_z + random.uniform(1.0, 4.0))
        )
        tube = bpy.context.active_object
        tube.name = f"Biotechnica_FluidTube_{i}"
        
        # Rotate to align with path
        tube.rotation_euler.x = math.radians(90)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create tube material
        tube_material = bpy.data.materials.new(name=f"Biotechnica_TubeMaterial_{i}")
        tube_material.use_nodes = True
        nodes = tube_material.node_tree.nodes
        links = tube_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # White
        principled.inputs['Metallic'].default_value = 0.0
        principled.inputs['Roughness'].default_value = 0.1
        #principled.inputs['Transmission'].default_value = 0.9
        principled.inputs['IOR'].default_value = 1.45
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        tube.data.materials.append(tube_material)
        
        interior_objects.append(tube)
        
        # Create fluid inside tube
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=tube_radius * 0.8,
            depth=abs(end_y - start_y) * 0.99,
            enter_editmode=False,
            align='WORLD',
            location=(start_x, (start_y + end_y)/2, entrance_z + random.uniform(1.0, 4.0))
        )
        fluid = bpy.context.active_object
        fluid.name = f"Biotechnica_Fluid_{i}"
        
        # Rotate to align with tube
        fluid.rotation_euler.x = math.radians(90)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create fluid material
        fluid_material = bpy.data.materials.new(name=f"Biotechnica_FluidMaterial_{i}")
        fluid_material.use_nodes = True
        nodes = fluid_material.node_tree.nodes
        links = fluid_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties - different colors for different fluids
        hue = i / tube_count
        fluid_color = (0.1 * hue, 0.8 - 0.5 * hue, 0.2 + 0.6 * hue, 1.0)
        emission.inputs['Color'].default_value = fluid_color
        emission.inputs['Strength'].default_value = 1.0
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Assign material
        fluid.data.materials.append(fluid_material)
        
        interior_objects.append(fluid)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection


def create_black_nexus_interior(black_nexus_objects, materials, interior_materials):
    """Create interior spaces for Black Nexus (ShadowRunner's Hidden Hub)"""
    # Extract objects from the black_nexus_objects dictionary
    building = black_nexus_objects.get("station")
    collection = black_nexus_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Black Nexus objects")
        return None
    
    # Create a subcollection for interior objects
    if "BlackNexus_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("BlackNexus_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["BlackNexus_Interior"]
    
    interior_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create entrance (rusted hatch with hidden scanner)
    entrance_x = building_loc[0]
    entrance_y = building_loc[1] - building_size.y/2
    entrance_z = building_loc[2]
    
    # Create hatch frame
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 0.5)
    )
    hatch_frame = bpy.context.active_object
    hatch_frame.name = "BlackNexus_HatchFrame"
    
    # Scale hatch frame
    hatch_frame.scale.x = 2.0
    hatch_frame.scale.y = 0.5
    hatch_frame.scale.z = 2.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    hatch_frame.data.materials.append(interior_materials["BlackNexus_Interior"])
    
    interior_objects.append(hatch_frame)
    
    # Create hatch door
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x, entrance_y - 0.3, entrance_z + 0.5)
    )
    hatch_door = bpy.context.active_object
    hatch_door.name = "BlackNexus_HatchDoor"
    
    # Edit the hatch door
    bm = bmesh.from_edit_mesh(hatch_door.data)
    
    # Scale hatch door
    for v in bm.verts:
        v.co.x *= 1.8
        v.co.y *= 0.1
        v.co.z *= 1.8
    
    # Update mesh
    bmesh.update_edit_mesh(hatch_door.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create hatch material with rust effect
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
    colorramp.color_ramp.elements[0].color = (0.4, 0.15, 0.05, 1.0)  # Rust color
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
    hatch_door.data.materials.append(hatch_material)
    
    interior_objects.append(hatch_door)
    
    # Create hidden scanner/camera
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x + 1.0, entrance_y - 0.1, entrance_z + 1.0)
    )
    scanner = bpy.context.active_object
    scanner.name = "BlackNexus_HiddenScanner"
    
    # Scale scanner
    scanner.scale.x = 0.1
    scanner.scale.y = 0.1
    scanner.scale.z = 0.1
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create scanner material
    scanner_material = bpy.data.materials.new(name="BlackNexus_ScannerMaterial")
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
    emission.inputs['Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Red
    emission.inputs['Strength'].default_value = 0.5  # Subtle glow
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    scanner.data.materials.append(scanner_material)
    
    interior_objects.append(scanner)
    
    # Create reinforced door behind the hatch
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y - 1.0, entrance_z + 0.5)
    )
    reinforced_door = bpy.context.active_object
    reinforced_door.name = "BlackNexus_ReinforcedDoor"
    
    # Scale reinforced door
    reinforced_door.scale.x = 1.5
    reinforced_door.scale.y = 0.2
    reinforced_door.scale.z = 1.5
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    reinforced_door.data.materials.append(interior_materials["BlackNexus_Interior"])
    
    interior_objects.append(reinforced_door)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection


def create_militech_armory_interior(militech_objects, materials, interior_materials):
    """Create interior spaces for Militech Armory (Upper Tier)"""
    # Extract objects from the militech_objects dictionary
    building = militech_objects.get("fortress")
    collection = militech_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Militech Armory objects")
        return None
    
    # Create a subcollection for interior objects
    if "Militech_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("Militech_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["Militech_Interior"]
    
    interior_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create reinforced blast doors with security checkpoint
    entrance_x = building_loc[0]
    entrance_y = building_loc[1] - building_size.y/2
    entrance_z = building_loc[2]
    
    # Create door frame
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 2.0)
    )
    door_frame = bpy.context.active_object
    door_frame.name = "Militech_DoorFrame"
    
    # Scale door frame
    door_frame.scale.x = 4.0
    door_frame.scale.y = 1.0
    door_frame.scale.z = 4.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    door_frame.data.materials.append(interior_materials["Militech_Interior"])
    
    interior_objects.append(door_frame)
    
    # Create blast doors (left and right panels)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=True,
            align='WORLD',
            location=(entrance_x + side * 1.0, entrance_y - 0.3, entrance_z + 2.0)
        )
        blast_door = bpy.context.active_object
        blast_door.name = f"Militech_BlastDoor_{'Left' if side < 0 else 'Right'}"
        
        # Edit the blast door
        bm = bmesh.from_edit_mesh(blast_door.data)
        
        # Scale blast door
        for v in bm.verts:
            v.co.x *= 1.8
            v.co.y *= 0.3
            v.co.z *= 3.8
        
        # Update mesh
        bmesh.update_edit_mesh(blast_door.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Create blast door material
        blast_door_material = bpy.data.materials.new(name=f"Militech_BlastDoorMaterial_{side}")
        blast_door_material.use_nodes = True
        nodes = blast_door_material.node_tree.nodes
        links = blast_door_material.node_tree.links
        
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
        blast_door.data.materials.append(blast_door_material)
        
        interior_objects.append(blast_door)
    
    # Create security checkpoint elements
    
    # Create security desk
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y - 3.0, entrance_z + 1.0)
    )
    security_desk = bpy.context.active_object
    security_desk.name = "Militech_SecurityDesk"
    
    # Scale security desk
    security_desk.scale.x = 3.0
    security_desk.scale.y = 1.0
    security_desk.scale.z = 1.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    security_desk.data.materials.append(interior_materials["Militech_Interior"])
    
    interior_objects.append(security_desk)
    
    # Create security monitors
    for i in range(3):
        offset = (i - 1) * 0.8
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x + offset, entrance_y - 3.0, entrance_z + 1.5)
        )
        monitor = bpy.context.active_object
        monitor.name = f"Militech_SecurityMonitor_{i}"
        
        # Scale monitor
        monitor.scale.x = 0.4
        monitor.scale.y = 0.05
        monitor.scale.z = 0.3
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create monitor screen material
        monitor_material = bpy.data.materials.new(name=f"Militech_MonitorMaterial_{i}")
        monitor_material.use_nodes = True
        nodes = monitor_material.node_tree.nodes
        links = monitor_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties
        emission.inputs['Color'].default_value = (0.1, 0.3, 0.6, 1.0)  # Blue screen
        emission.inputs['Strength'].default_value = 1.0
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Assign material
        monitor.data.materials.append(monitor_material)
        
        interior_objects.append(monitor)
    
    # Create retractable gun turrets flanking entrance
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.3,
            depth=0.6,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x + side * 3.0, entrance_y, entrance_z + 3.0)
        )
        turret_base = bpy.context.active_object
        turret_base.name = f"Militech_TurretBase_{side}"
        
        # Rotate to point outward
        turret_base.rotation_euler.x = math.radians(90)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create turret gun
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.1,
            depth=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x + side * 3.0, entrance_y - 0.5, entrance_z + 3.0)
        )
        turret_gun = bpy.context.active_object
        turret_gun.name = f"Militech_TurretGun_{side}"
        
        # Rotate to point outward
        turret_gun.rotation_euler.x = math.radians(90)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create turret material
        turret_material = bpy.data.materials.new(name=f"Militech_TurretMaterial_{side}")
        turret_material.use_nodes = True
        nodes = turret_material.node_tree.nodes
        links = turret_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set properties
        principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dark gray
        principled.inputs['Metallic'].default_value = 0.9
        principled.inputs['Roughness'].default_value = 0.3
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign materials
        turret_base.data.materials.append(turret_material)
        turret_gun.data.materials.append(turret_material)
        
        interior_objects.append(turret_base)
        interior_objects.append(turret_gun)
    
    # Create red warning lights
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.2,
            depth=0.1,
            enter_editmode=False,
            align='WORLD',
            location=(entrance_x + side * 2.0, entrance_y, entrance_z + 4.0)
        )
        warning_light = bpy.context.active_object
        warning_light.name = f"Militech_WarningLight_{side}"
        
        # Rotate to point downward
        warning_light.rotation_euler.x = math.radians(90)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create warning light material
        light_material = bpy.data.materials.new(name=f"Militech_WarningLightMaterial_{side}")
        light_material.use_nodes = True
        nodes = light_material.node_tree.nodes
        links = light_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties
        emission.inputs['Color'].default_value = (1.0, 0.1, 0.1, 1.0)  # Red
        emission.inputs['Strength'].default_value = 3.0
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Assign material
        warning_light.data.materials.append(light_material)
        
        interior_objects.append(warning_light)
    
    # Create corporate logo
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 5.0)
    )
    logo = bpy.context.active_object
    logo.name = "Militech_CorporateLogo"
    
    # Scale logo
    logo.scale.x = 3.0
    logo.scale.y = 1.0
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create logo material
    logo_material = bpy.data.materials.new(name="Militech_LogoMaterial")
    logo_material.use_nodes = True
    nodes = logo_material.node_tree.nodes
    links = logo_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set properties
    emission.inputs['Color'].default_value = (1.0, 0.1, 0.1, 1.0)  # Red
    emission.inputs['Strength'].default_value = 2.0
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    logo.data.materials.append(logo_material)
    
    interior_objects.append(logo)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection


def create_rust_vault_interior(rust_vault_objects, materials, interior_materials):
    """Create interior spaces for Rust Vault (Lower Tier hacker den)"""
    # Extract objects from the rust_vault_objects dictionary
    building = rust_vault_objects.get("door")
    collection = rust_vault_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Rust Vault objects")
        return None
    
    # Create a subcollection for interior objects
    if "RustVault_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("RustVault_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["RustVault_Interior"]
    
    interior_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create heavy vault-style door with manual wheel lock
    entrance_x = building_loc[0]
    entrance_y = building_loc[1] - building_size.y/2
    entrance_z = building_loc[2]
    
    # Create door frame
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 1.0)
    )
    door_frame = bpy.context.active_object
    door_frame.name = "RustVault_DoorFrame"
    
    # Scale door frame
    door_frame.scale.x = 2.5
    door_frame.scale.y = 0.5
    door_frame.scale.z = 2.5
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    door_frame.data.materials.append(interior_materials["RustVault_Interior"])
    
    interior_objects.append(door_frame)
    
    # Create vault door
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=1.0,
        depth=0.3,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y - 0.3, entrance_z + 1.0)
    )
    vault_door = bpy.context.active_object
    vault_door.name = "RustVault_VaultDoor"
    
    # Rotate door to face outward
    vault_door.rotation_euler.x = math.radians(90)
    
    # Apply rotation
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Create vault door material with heavy rust
    vault_material = bpy.data.materials.new(name="RustVault_DoorMaterial")
    vault_material.use_nodes = True
    nodes = vault_material.node_tree.nodes
    links = vault_material.node_tree.links
    
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
    vault_door.data.materials.append(vault_material)
    
    interior_objects.append(vault_door)
    
    # Create manual wheel lock
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.6,
        minor_radius=0.05,
        major_segments=32,
        minor_segments=8,
        align='WORLD',
        location=(entrance_x, entrance_y - 0.15, entrance_z + 1.0)
    )
    wheel_lock = bpy.context.active_object
    wheel_lock.name = "RustVault_WheelLock"
    
    # Rotate wheel to face outward
    wheel_lock.rotation_euler.x = math.radians(90)
    
    # Apply rotation
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Create wheel spokes
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        spoke_x = entrance_x + 0.3 * math.cos(angle)
        spoke_y = entrance_y - 0.15
        spoke_z = entrance_z + 1.0 + 0.3 * math.sin(angle)
        
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.03,
            depth=0.5,
            enter_editmode=False,
            align='WORLD',
            location=(spoke_x, spoke_y, spoke_z)
        )
        spoke = bpy.context.active_object
        spoke.name = f"RustVault_WheelSpoke_{i}"
        
        # Rotate spoke to point from center
        direction = Vector((spoke_x - entrance_x, 0, spoke_z - (entrance_z + 1.0)))
        rot_quat = direction.to_track_quat('Z', 'Y')
        spoke.rotation_euler = rot_quat.to_euler()
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Assign material
        spoke.data.materials.append(vault_material)
        
        interior_objects.append(spoke)
    
    # Assign material to wheel lock
    wheel_lock.data.materials.append(vault_material)
    
    interior_objects.append(wheel_lock)
    
    # Create hidden keypad under rust patch
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x + 1.0, entrance_y - 0.1, entrance_z + 0.5)
    )
    keypad = bpy.context.active_object
    keypad.name = "RustVault_HiddenKeypad"
    
    # Scale keypad
    keypad.scale.x = 0.2
    keypad.scale.y = 0.05
    keypad.scale.z = 0.3
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create keypad material
    keypad_material = bpy.data.materials.new(name="RustVault_KeypadMaterial")
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
    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.5
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    keypad.data.materials.append(keypad_material)
    
    interior_objects.append(keypad)
    
    # Create keypad buttons
    for i in range(9):
        row = i // 3
        col = i % 3
        
        button_x = entrance_x + 1.0 + (col - 1) * 0.05
        button_y = entrance_y - 0.05
        button_z = entrance_z + 0.5 + (1 - row) * 0.07
        
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            enter_editmode=False,
            align='WORLD',
            location=(button_x, button_y, button_z)
        )
        button = bpy.context.active_object
        button.name = f"RustVault_KeypadButton_{i+1}"
        
        # Scale button
        button.scale.x = 0.02
        button.scale.y = 0.02
        button.scale.z = 0.02
        
        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Create button material
        button_material = bpy.data.materials.new(name=f"RustVault_ButtonMaterial_{i+1}")
        button_material.use_nodes = True
        nodes = button_material.node_tree.nodes
        links = button_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        
        # Set properties
        emission.inputs['Color'].default_value = (0.2, 0.8, 0.2, 1.0)  # Green
        emission.inputs['Strength'].default_value = 0.5  # Subtle glow
        
        # Connect nodes
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Assign material
        button.data.materials.append(button_material)
        
        interior_objects.append(button)
    
    # Create rust patch covering keypad
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x + 1.0, entrance_y - 0.05, entrance_z + 0.5)
    )
    rust_patch = bpy.context.active_object
    rust_patch.name = "RustVault_RustPatch"
    
    # Edit the rust patch to make it irregular
    bm = bmesh.from_edit_mesh(rust_patch.data)
    
    # Scale rust patch
    for v in bm.verts:
        v.co.x *= 0.25
        v.co.y *= 0.02
        v.co.z *= 0.35
    
    # Randomize vertices to create irregular shape
    for v in bm.verts:
        v.co.x += random.uniform(-0.05, 0.05)
        v.co.z += random.uniform(-0.05, 0.05)
    
    # Update mesh
    bmesh.update_edit_mesh(rust_patch.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Assign material
    rust_patch.data.materials.append(vault_material)
    
    interior_objects.append(rust_patch)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection



def create_wire_nest_interior(wire_nest_objects, materials, interior_materials):
    """Create interior spaces for Wire Nest (Mid Tier hacker den)"""
    # Extract objects from the wire_nest_objects dictionary
    building = wire_nest_objects.get("frame")
    collection = wire_nest_objects.get("collection")
    
    if not building or not collection:
        print("Error: Missing required Wire Nest objects")
        return None
    
    # Create a subcollection for interior objects
    if "WireNest_Interior" not in bpy.data.collections:
        interior_collection = bpy.data.collections.new("WireNest_Interior")
        collection.children.link(interior_collection)
    else:
        interior_collection = bpy.data.collections["WireNest_Interior"]
    
    interior_objects = []
    
    # Get building location and dimensions
    building_loc = building.location
    building_size = building.dimensions
    
    # Create concealed entrance behind fake utility panel
    entrance_x = building_loc[0]
    entrance_y = building_loc[1] - building_size.y/2
    entrance_z = building_loc[2]
    
    # Create utility panel frame
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x, entrance_y, entrance_z + 1.0)
    )
    panel_frame = bpy.context.active_object
    panel_frame.name = "WireNest_UtilityPanelFrame"
    
    # Scale panel frame
    panel_frame.scale.x = 2.0
    panel_frame.scale.y = 0.2
    panel_frame.scale.z = 2.5
    
    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Assign material
    panel_frame.data.materials.append(interior_materials["WireNest_Interior"])
    
    interior_objects.append(panel_frame)
    
    # Create utility panel door
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=True,
        align='WORLD',
        location=(entrance_x, entrance_y - 0.1, entrance_z + 1.0)
    )
    panel_door = bpy.context.active_object
    panel_door.name = "WireNest_UtilityPanelDoor"
    
    # Edit the panel door
    bm = bmesh.from_edit_mesh(panel_door.data)
    
    # Scale panel door
    for v in bm.verts:
        v.co.x *= 1.8
        v.co.y *= 0.1
        v.co.z *= 2.3
    
    # Update mesh
    bmesh.update_edit_mesh(panel_door.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create panel material with tech look
    panel_material = bpy.data.materials.new(name="WireNest_PanelMaterial")
    panel_material.use_nodes = True
    nodes = panel_material.node_tree.nodes
    links = panel_material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set properties
    principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.25, 1.0)  # Dark blue-gray
    principled.inputs['Metallic'].default_value = 0.7
    principled.inputs['Roughness'].default_value = 0.3
    
    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material
    panel_door.data.materials.append(panel_material)
    
    interior_objects.append(panel_door)
    
    # Create retinal scanner disguised as broken light fixture
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=0.2,
        depth=0.1,
        enter_editmode=False,
        align='WORLD',
        location=(entrance_x + 1.0, entrance_y - 0.1, entrance_z + 1.8)
    )
    scanner = bpy.context.active_object
    scanner.name = "WireNest_RetinalScanner"
    
    # Rotate scanner to face outward
    scanner.rotation_euler.x = math.radians(90)
    
    # Apply rotation
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Create scanner material
    scanner_material = bpy.data.materials.new(name="WireNest_ScannerMaterial")
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
    emission.inputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Very dim light
    emission.inputs['Strength'].default_value = 0.2  # Subtle glow
    
    # Connect nodes
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    # Assign material
    scanner.data.materials.append(scanner_material)
    
    interior_objects.append(scanner)
    
    # Create exposed wiring forming door outline
    wire_segments = 20
    for i in range(wire_segments):
        # Calculate position along the door frame
        angle = i * (2 * math.pi / wire_segments)
        radius_x = 1.0
        radius_z = 1.25
        
        wire_x = entrance_x + radius_x * math.cos(angle)
        wire_z = entrance_z + 1.0 + radius_z * math.sin(angle)
        
        # Create wire segment
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.05,
            depth=0.3 + 0.1 * random.random(),  # Slightly random length
            enter_editmode=False,
            align='WORLD',
            location=(wire_x, entrance_y - 0.05, wire_z)
        )
        wire = bpy.context.active_object
        wire.name = f"WireNest_DoorWire_{i}"
        
        # Rotate wire to point outward from door
        wire.rotation_euler.x = math.radians(90)
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Create wire material with random color
        wire_material = bpy.data.materials.new(name=f"WireNest_WireMaterial_{i}")
        wire_material.use_nodes = True
        nodes = wire_material.node_tree.nodes
        links = wire_material.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Set random color
        r = random.choice([0.1, 0.8, 0.2, 0.3])
        g = random.choice([0.1, 0.2, 0.7, 0.3])
        b = random.choice([0.1, 0.2, 0.3, 0.8])
        principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
        principled.inputs['Metallic'].default_value = 0.3
        principled.inputs['Roughness'].default_value = 0.8
        
        # Connect nodes
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign material
        wire.data.materials.append(wire_material)
        
        interior_objects.append(wire)
    
    # Move all objects to the interior collection
    for obj in interior_objects:
        if obj.name not in interior_collection.objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.move_to_collection(collection_index=bpy.data.collections.find(interior_collection.name))
    
    return interior_collection


# Main function to implement building interiors
def implement_building_interiors(building_objects, materials):
    """Implement interior spaces for all buildings"""
    # Create interior materials

    interior_materials = create_interior_materials()
    
    # Combine all materials
    all_materials = {**materials, **interior_materials}
    
    # Implement interiors for each building
    interiors = {}
    
    # NeoTech Labs Tower
    if "neotech_tower" in building_objects:
        interiors["NeoTech_Interior"] = create_neotech_tower_interior(
            building_objects["neotech_tower"],
            all_materials,
            interior_materials
        )
    
    # Specter Station
    if "specter_station" in building_objects:
        interiors["Specter_Interior"] = create_specter_station_interior(
            building_objects["specter_station"],
            all_materials,
            interior_materials
        ) 
    
	# Biotechnica Spire
    if "biotechnica_spire" in building_objects:
        interiors["BiotechnicaSpire_Interior"] = create_biotechnica_spire_interior(
            building_objects["biotechnica_spire"],
            all_materials,
            interior_materials
        ) 

	# Black Nexus
    if "black_nexus" in building_objects:
	    interiors["BlackNexus_Interior"] = create_black_nexus_interior(
            building_objects["black_nexus"],
            all_materials,
            interior_materials
        ) 

	# Militech Armory
    if "militech_armory" in building_objects:
	    interiors["MilitechArmory_Interior"] = create_militech_armory_interior(
            building_objects["militech_armory"],
            all_materials,
            interior_materials
        ) 
	
	# Wire Nest
    if "wire_nest" in building_objects:
        interiors["WireNest_Interior"] = create_wire_nest_interior(
            building_objects["wire_nest"],
            all_materials,
            interior_materials
        ) 
	
	# Rust Vault
    if "rust_vault" in building_objects:
        interiors["RustVault_Interior"] = create_rust_vault_interior(
            building_objects["rust_vault"],
            all_materials,
            interior_materials
        ) 

    
    return interiors
