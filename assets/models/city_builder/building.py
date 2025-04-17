"""
Neon Crucible - Specific Building Generation Script
Blender 4.2 Python Script for generating specific buildings and locations
as described in the Neon Crucible cyberpunk world requirements.

This script creates detailed models of key locations including:
- NeoTech Labs Tower (Upper Tier)
- Specter Station (Mid Tier)
- Black Nexus (ShadowRunner's Hidden Hub, Lower Tier)
- Wire Nest (Mid Tier hacker den)
- Rust Vault (Lower Tier hacker den)
- Militech Armory (Upper Tier)
- Biotechnica Spire (Upper Tier)

NOTE: The procedural city generation components have been removed.
This script focuses solely on the landmark buildings.
"""

import bpy
import bmesh
import random
import math
import os
from mathutils import Vector, Matrix

# --- Helper Functions (Originally from city_generation.py) ---

# Clear existing objects
def clear_scene():
    """Clear all objects in the scene"""
    # Deselect all objects first
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear all collections except the default "Collection"
    collections_to_remove = [col for col in bpy.data.collections if col.name != "Collection"]
    for collection in collections_to_remove:
        # Remove objects within the collection first if they weren't deleted above
        # (Handle potential hierarchy issues)
        while collection.objects:
            bpy.data.objects.remove(collection.objects[0], do_unlink=True)
        bpy.data.collections.remove(collection)

    # Clear all materials
    materials_to_remove = [mat for mat in bpy.data.materials]
    for material in materials_to_remove:
        bpy.data.materials.remove(material)

    # Clear all meshes
    meshes_to_remove = [mesh for mesh in bpy.data.meshes]
    for mesh in meshes_to_remove:
        bpy.data.meshes.remove(mesh)

    # Clear particle settings (if any remain from previous runs)
    particle_settings_to_remove = [ps for ps in bpy.data.particles]
    for ps in particle_settings_to_remove:
        bpy.data.particles.remove(ps)

    # Clear world nodes if they exist
    if bpy.context.scene.world and bpy.context.scene.world.use_nodes:
        bpy.context.scene.world.node_tree.nodes.clear()
        # Optionally set a default background
        bpy.context.scene.world.node_tree.nodes.new(type='ShaderNodeBackground')


# Create collections for organization
def create_collections():
    """Create collections for organizing the city elements"""
    collections = {
        "NeonCrucible": None,
        "UpperTier": None,
        "MidTier": None,
        "LowerTier": None,
        # Keep Lights/Props/Environment even if not used by landmarks?
        # Might be useful for context later. Let's keep them for structure.
        "Lights": None,
        "Props": None,
        "Environment": None
    }

    # Ensure the base scene collection exists
    base_coll = bpy.context.scene.collection

    # Create main collection
    if "NeonCrucible" not in bpy.data.collections:
        collections["NeonCrucible"] = bpy.data.collections.new("NeonCrucible")
        base_coll.children.link(collections["NeonCrucible"])
    else:
        collections["NeonCrucible"] = bpy.data.collections["NeonCrucible"]
        # Ensure it's linked if running multiple times in one session
        if collections["NeonCrucible"].name not in base_coll.children:
             base_coll.children.link(collections["NeonCrucible"])


    # Create sub-collections under NeonCrucible
    main_coll = collections["NeonCrucible"]
    for name in ["UpperTier", "MidTier", "LowerTier", "Lights", "Props", "Environment"]:
        if name not in bpy.data.collections:
            collections[name] = bpy.data.collections.new(name)
            main_coll.children.link(collections[name])
        else:
            collections[name] = bpy.data.collections[name]
             # Ensure it's linked if running multiple times in one session
            if collections[name].name not in main_coll.children:
                 main_coll.children.link(collections[name])

    return collections

# Create basic materials (Originally from city_generation.py)
def create_materials():
    """Create basic placeholder materials"""
    materials = {}

    # Placeholder Upper Tier materials
    upper_building = bpy.data.materials.new(name="UpperTier_Building_Basic")
    upper_building.use_nodes = True
    nodes = upper_building.node_tree.nodes
    links = upper_building.node_tree.links
    for node in nodes: nodes.remove(node) # Clear default
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.05, 0.05, 0.1, 1.0)
    principled.inputs['Metallic'].default_value = 0.9
    principled.inputs['Roughness'].default_value = 0.1
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["UpperTier_Building_Basic"] = upper_building # Renamed to avoid conflict

    # Placeholder Mid Tier materials
    mid_building = bpy.data.materials.new(name="MidTier_Building_Basic")
    mid_building.use_nodes = True
    nodes = mid_building.node_tree.nodes
    links = mid_building.node_tree.links
    for node in nodes: nodes.remove(node) # Clear default
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.12, 1.0)
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.4
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["MidTier_Building_Basic"] = mid_building # Renamed

    # Placeholder Lower Tier materials
    lower_building = bpy.data.materials.new(name="LowerTier_Building_Basic")
    lower_building.use_nodes = True
    nodes = lower_building.node_tree.nodes
    links = lower_building.node_tree.links
    for node in nodes: nodes.remove(node) # Clear default
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.15, 0.14, 0.13, 1.0)
    principled.inputs['Metallic'].default_value = 0.2
    principled.inputs['Roughness'].default_value = 0.8
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["LowerTier_Building_Basic"] = lower_building # Renamed

    # Basic Neon material
    neon = bpy.data.materials.new(name="Neon_Emission_Basic")
    neon.use_nodes = True
    nodes = neon.node_tree.nodes
    links = neon.node_tree.links
    for node in nodes: nodes.remove(node) # Clear default
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.0, 1.0, 0.8, 1.0) # Cyan
    emission.inputs['Strength'].default_value = 5.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials["Neon_Emission_Basic"] = neon # Renamed

    # Basic Ground material
    ground = bpy.data.materials.new(name="Ground_Basic")
    ground.use_nodes = True
    nodes = ground.node_tree.nodes
    links = ground.node_tree.links
    for node in nodes: nodes.remove(node) # Clear default
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.9
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["Ground_Basic"] = ground # Renamed

    return materials


# --- Landmark Building Specific Code (Originally from building_generation.py) ---

# Create advanced materials for specific buildings
def create_advanced_materials():
    """Create advanced materials for specific buildings"""
    materials = {}

    # NeoTech Labs Tower - Black glass and chrome
    neotech = bpy.data.materials.new(name="NeoTech_Exterior")
    neotech.use_nodes = True
    nodes = neotech.node_tree.nodes
    links = neotech.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.01, 0.01, 0.02, 1.0)  # Almost black
    principled.inputs['Metallic'].default_value = 0.9
    principled.inputs['Roughness'].default_value = 0.1
    #principled.inputs['Specular'].default_value = 1.0
    #principled.inputs['Clearcoat'].default_value = 1.0
    #principled.inputs['Clearcoat Roughness'].default_value = 0.1
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["NeoTech_Exterior"] = neotech

    # Specter Station - Derelict metal
    specter = bpy.data.materials.new(name="Specter_Exterior")
    specter.use_nodes = True
    nodes = specter.node_tree.nodes
    links = specter.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    noise = nodes.new(type='ShaderNodeTexNoise')
    mapping = nodes.new(type='ShaderNodeMapping')
    texcoord = nodes.new(type='ShaderNodeTexCoord')
    colorramp = nodes.new(type='ShaderNodeValToRGB')

    principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.22, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.7
    principled.inputs['Roughness'].default_value = 0.6

    noise.inputs['Scale'].default_value = 10.0
    noise.inputs['Detail'].default_value = 6.0
    noise.inputs['Roughness'].default_value = 0.7

    colorramp.color_ramp.elements[0].position = 0.4
    colorramp.color_ramp.elements[0].color = (0.2, 0.05, 0.01, 1.0)  # Rust color
    colorramp.color_ramp.elements[1].position = 0.6
    colorramp.color_ramp.elements[1].color = (0.3, 0.3, 0.32, 1.0)  # Metal color

    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(noise.outputs['Fac'], principled.inputs['Roughness']) # Use noise for roughness variation
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["Specter_Exterior"] = specter

    # Black Nexus - Concrete with neon
    black_nexus = bpy.data.materials.new(name="BlackNexus_Exterior")
    black_nexus.use_nodes = True
    nodes = black_nexus.node_tree.nodes
    links = black_nexus.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    noise = nodes.new(type='ShaderNodeTexNoise')
    mapping = nodes.new(type='ShaderNodeMapping')
    texcoord = nodes.new(type='ShaderNodeTexCoord')

    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.9

    noise.inputs['Scale'].default_value = 20.0
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.5

    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], principled.inputs['Roughness'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["BlackNexus_Exterior"] = black_nexus

    # Neon Sign Material - Binary code
    binary_neon = bpy.data.materials.new(name="Binary_Neon")
    binary_neon.use_nodes = True
    nodes = binary_neon.node_tree.nodes
    links = binary_neon.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.0, 1.0, 0.5, 1.0)  # Green-cyan
    emission.inputs['Strength'].default_value = 5.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials["Binary_Neon"] = binary_neon

    # Militech Armory - Red accented metal
    militech = bpy.data.materials.new(name="Militech_Exterior")
    militech.use_nodes = True
    nodes = militech.node_tree.nodes
    links = militech.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.15, 0.15, 0.15, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.8
    principled.inputs['Roughness'].default_value = 0.2
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["Militech_Exterior"] = militech

    # Militech Red Accent
    militech_accent = bpy.data.materials.new(name="Militech_Accent")
    militech_accent.use_nodes = True
    nodes = militech_accent.node_tree.nodes
    links = militech_accent.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1.0, 0.1, 0.1, 1.0)  # Red
    emission.inputs['Strength'].default_value = 3.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials["Militech_Accent"] = militech_accent

    # Biotechnica Spire - Green-tinted glass
    biotechnica = bpy.data.materials.new(name="Biotechnica_Exterior")
    biotechnica.use_nodes = True
    nodes = biotechnica.node_tree.nodes
    links = biotechnica.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.2, 1.0)  # Green-tinted
    principled.inputs['Metallic'].default_value = 0.5
    principled.inputs['Roughness'].default_value = 0.1
    principled.inputs['Transmission Weight'].default_value = 0.8  # Glass-like
    principled.inputs['IOR'].default_value = 1.45
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["Biotechnica_Exterior"] = biotechnica

    # Wire Nest - Skeletal metal
    wire_nest = bpy.data.materials.new(name="WireNest_Exterior")
    wire_nest.use_nodes = True
    nodes = wire_nest.node_tree.nodes
    links = wire_nest.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)  # Gray
    principled.inputs['Metallic'].default_value = 0.9
    principled.inputs['Roughness'].default_value = 0.5
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["WireNest_Exterior"] = wire_nest

    # Rust Vault - Reinforced steel
    rust_vault = bpy.data.materials.new(name="RustVault_Exterior")
    rust_vault.use_nodes = True
    nodes = rust_vault.node_tree.nodes
    links = rust_vault.node_tree.links

    for node in nodes: nodes.remove(node) # Clear default nodes

    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    noise = nodes.new(type='ShaderNodeTexNoise')
    mapping = nodes.new(type='ShaderNodeMapping')
    texcoord = nodes.new(type='ShaderNodeTexCoord')
    colorramp = nodes.new(type='ShaderNodeValToRGB')

    principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.8
    principled.inputs['Roughness'].default_value = 0.7

    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 10.0
    noise.inputs['Roughness'].default_value = 0.8

    colorramp.color_ramp.elements[0].position = 0.3
    colorramp.color_ramp.elements[0].color = (0.3, 0.1, 0.05, 1.0)  # Heavy rust color
    colorramp.color_ramp.elements[1].position = 0.7
    colorramp.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0)  # Steel color

    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(noise.outputs['Fac'], principled.inputs['Roughness']) # Use noise for roughness variation
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials["RustVault_Exterior"] = rust_vault

    return materials

# Helper function to move object to collection
def move_to_collection(obj, collection):
    """Moves an object to a specified collection, handling potential duplicates."""
    # Check if the object is already in the target collection
    if obj.name in collection.objects:
        return # Already there

    # Remove from existing collections (except scene collection)
    for coll in obj.users_collection:
        if coll != bpy.context.scene.collection:
             coll.objects.unlink(obj)

    # Link to the target collection
    collection.objects.link(obj)


# Create NeoTech Labs Tower
def create_neotech_tower(collections, materials, location=(50, 50, 0), scale_factor=1.0):
    """Create the NeoTech Labs Tower as described in the requirements"""
    neotech_collection = collections["UpperTier"].children.get("NeoTech_Tower")
    if not neotech_collection:
        neotech_collection = bpy.data.collections.new("NeoTech_Tower")
        collections["UpperTier"].children.link(neotech_collection)

    all_objects = [] # Keep track of created objects for this building

    # Create the main tower structure - obelisk shape
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=10 * scale_factor,
        depth=150 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 75 * scale_factor)
    )
    tower = bpy.context.active_object
    tower.name = "NeoTech_MainTower"
    all_objects.append(tower)

    # Taper the tower
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tower.data)
    bm.verts.ensure_lookup_table() # Ensure vertex indices are up-to-date
    center_z = tower.location.z
    top_verts = [v for v in bm.verts if v.co.z + center_z > tower.location.z + (150 * scale_factor * 0.45)] # Adjust threshold
    # Ensure we have top verts before scaling
    if top_verts:
        # Calculate center of top verts for scaling pivot
        center = Vector((0,0,0))
        for v in top_verts:
            center += v.co
        center /= len(top_verts)

        # Create scaling matrix relative to center
        mat_scale = Matrix.Scale(0.6, 4, (1.0, 0.0, 0.0)) @ Matrix.Scale(0.6, 4, (0.0, 1.0, 0.0))
        mat_trans = Matrix.Translation(center)
        mat_trans_inv = Matrix.Translation(-center)

        bmesh.ops.transform(bm, matrix=mat_trans @ mat_scale @ mat_trans_inv, verts=top_verts)
    else:
        print(f"Warning: No top vertices found for NeoTech tower tapering at Z > {tower.location.z + (150 * scale_factor * 0.45)}")

    bmesh.update_edit_mesh(tower.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    tower.data.materials.append(materials["NeoTech_Exterior"])

    # Create the base/lobby
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=20 * scale_factor,
        depth=10 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 5 * scale_factor)
    )
    base = bpy.context.active_object
    base.name = "NeoTech_Base"
    base.data.materials.append(materials["NeoTech_Exterior"])
    all_objects.append(base)

    # Create holo-ads orbiting the peak
    holo_ads = []
    for i in range(5):
        angle = i * (2 * math.pi / 5)
        ad_x = location[0] + 15 * scale_factor * math.cos(angle)
        ad_y = location[1] + 15 * scale_factor * math.sin(angle)
        ad_z = location[2] + 140 * scale_factor

        bpy.ops.mesh.primitive_plane_add(
            size=5 * scale_factor,
            enter_editmode=False,
            align='WORLD',
            location=(ad_x, ad_y, ad_z)
        )
        ad = bpy.context.active_object
        ad.name = f"NeoTech_HoloAd_{i}"

        direction = Vector((location[0], location[1], ad_z)) - Vector((ad_x, ad_y, ad_z))
        rot_quat = direction.to_track_quat('-Y', 'Z') # Track -Y towards center, Z up
        ad.rotation_euler = rot_quat.to_euler()
        ad.rotation_euler.z += math.pi/2 # Adjust if needed


        ad_material = bpy.data.materials.new(name=f"NeoTech_Ad_{i}")
        ad_material.use_nodes = True
        nodes = ad_material.node_tree.nodes
        links = ad_material.node_tree.links
        for node in nodes: nodes.remove(node) # Clear default
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        r, g, b = random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)
        emission.inputs['Color'].default_value = (r, g, b, 1.0)
        emission.inputs['Strength'].default_value = 3.0
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        ad.data.materials.append(ad_material)
        holo_ads.append(ad)
        all_objects.append(ad)

    # Create laser grid security
    laser_grids = []
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        grid_x = location[0] + 25 * scale_factor * math.cos(angle)
        grid_y = location[1] + 25 * scale_factor * math.sin(angle)
        grid_z = location[2] + 2 * scale_factor

        bpy.ops.mesh.primitive_plane_add(
            size=10 * scale_factor,
            enter_editmode=False,
            align='WORLD',
            location=(grid_x, grid_y, grid_z)
        )
        grid = bpy.context.active_object
        grid.name = f"NeoTech_LaserGrid_{i}"
        grid.rotation_euler = (0, 0, angle) # Rotate to align with angle

        grid_material = bpy.data.materials.new(name=f"LaserGrid_{i}")
        grid_material.use_nodes = True
        nodes = grid_material.node_tree.nodes
        links = grid_material.node_tree.links
        for node in nodes: nodes.remove(node) # Clear default
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1.0, 0.1, 0.1, 1.0)  # Red
        emission.inputs['Strength'].default_value = 2.0
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        grid.data.materials.append(grid_material)
        laser_grids.append(grid)
        all_objects.append(grid)

    # Move all created objects to the building's collection
    for obj in all_objects:
        move_to_collection(obj, neotech_collection)

    return {
        "tower": tower,
        "base": base,
        "holo_ads": holo_ads,
        "laser_grids": laser_grids,
        "collection": neotech_collection
    }

# Create Specter Station
def create_specter_station(collections, materials, location=(0, 80, 0), scale_factor=1.0):
    """Create Specter Station as described in the requirements"""
    specter_collection = collections["MidTier"].children.get("Specter_Station")
    if not specter_collection:
        specter_collection = bpy.data.collections.new("Specter_Station")
        collections["MidTier"].children.link(specter_collection)

    all_objects = []

    # Create the main tower structure - skeletal spire
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=6,
        radius=5 * scale_factor,
        depth=80 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 40 * scale_factor)
    )
    tower = bpy.context.active_object
    tower.name = "Specter_MainTower"
    all_objects.append(tower)

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tower.data)
    bm.faces.ensure_lookup_table()
    faces_to_delete = [f for i, f in enumerate(bm.faces) if i % 2 == 0 and abs(f.normal.z) < 0.1] # Delete side faces
    if faces_to_delete:
         bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
    bmesh.update_edit_mesh(tower.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    tower.data.materials.append(materials["Specter_Exterior"])

    # Create antennae
    antennae = []
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        ant_x = location[0] + 6 * scale_factor * math.cos(angle)
        ant_y = location[1] + 6 * scale_factor * math.sin(angle)
        ant_z_base = location[2] + 70 * scale_factor
        height = random.uniform(10, 20) * scale_factor

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=4,
            radius=0.5 * scale_factor,
            depth=height,
            enter_editmode=False,
            align='WORLD',
            location=(ant_x, ant_y, ant_z_base + height/2)
        )
        antenna = bpy.context.active_object
        antenna.name = f"Specter_Antenna_{i}"
        antenna.rotation_euler = (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0)
        antenna.data.materials.append(materials["Specter_Exterior"])
        antennae.append(antenna)
        all_objects.append(antenna)

    # Create broken solar panels
    panels = []
    for i in range(5):
        angle = i * (2 * math.pi / 5)
        panel_x = location[0] + 10 * scale_factor * math.cos(angle)
        panel_y = location[1] + 10 * scale_factor * math.sin(angle)
        panel_z = location[2] + random.uniform(30, 60) * scale_factor

        bpy.ops.mesh.primitive_plane_add(
            size=5 * scale_factor,
            enter_editmode=False, # Edit after creation
            align='WORLD',
            location=(panel_x, panel_y, panel_z)
        )
        panel = bpy.context.active_object
        panel.name = f"Specter_SolarPanel_{i}"
        panel.rotation_euler = (random.uniform(0, 0.5), random.uniform(0, 0.5), angle)

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(panel.data)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2)
        for vert in bm.verts:
            if random.random() > 0.7:
                vert.co.z += random.uniform(-0.5, 0.5) * scale_factor
        bmesh.update_edit_mesh(panel.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        panel_material = bpy.data.materials.new(name=f"SolarPanel_{i}")
        panel_material.use_nodes = True
        nodes = panel_material.node_tree.nodes
        links = panel_material.node_tree.links
        for node in nodes: nodes.remove(node) # Clear default
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.05, 0.1, 0.2, 1.0) # Dark blue
        principled.inputs['Metallic'].default_value = 0.9
        principled.inputs['Roughness'].default_value = 0.3
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        panel.data.materials.append(panel_material)
        panels.append(panel)
        all_objects.append(panel)

    # Create the command deck
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=8 * scale_factor,
        depth=2 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 60 * scale_factor)
    )
    deck = bpy.context.active_object
    deck.name = "Specter_CommandDeck"
    deck.data.materials.append(materials["Specter_Exterior"])
    all_objects.append(deck)

    # Create neon glyphs
    glyphs = []
    # Using a single plane for simplicity, texture would be better for real text
    bpy.ops.mesh.primitive_plane_add(
        size=1, # Scale later
        enter_editmode=False,
        align='WORLD',
        location=(location[0] + 5.1 * scale_factor, location[1], location[2] + 30 * scale_factor) # Offset from tower radius
    )
    glyph = bpy.context.active_object
    glyph.name = "Specter_Glyph"
    glyph.scale = (5 * scale_factor, 1 * scale_factor, 1) # Make it wide
    glyph.rotation_euler = (math.pi/2, 0, math.pi/2) # Rotate to face out

    glyph_material = bpy.data.materials.new(name="Specter_Glyph_Material")
    glyph_material.use_nodes = True
    nodes = glyph_material.node_tree.nodes
    links = glyph_material.node_tree.links
    for node in nodes: nodes.remove(node) # Clear default
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.5, 0.0, 1.0, 1.0)  # Purple
    emission.inputs['Strength'].default_value = 3.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    glyph.data.materials.append(glyph_material)
    glyphs.append(glyph)
    all_objects.append(glyph)

    # Move all to collection
    for obj in all_objects:
        move_to_collection(obj, specter_collection)

    return {
        "tower": tower,
        "deck": deck,
        "antennae": antennae,
        "panels": panels,
        "glyphs": glyphs,
        "collection": specter_collection
    }


# Create Black Nexus (ShadowRunner's Hidden Hub)
def create_black_nexus(collections, materials, location=(-70, -50, 0), scale_factor=1.0):
    """Create the Black Nexus (ShadowRunner's hidden hub) as described in the requirements"""
    nexus_collection = collections["LowerTier"].children.get("Black_Nexus")
    if not nexus_collection:
        nexus_collection = bpy.data.collections.new("Black_Nexus")
        collections["LowerTier"].children.link(nexus_collection)

    all_objects = []

    # Create the abandoned maglev station exterior
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 3 * scale_factor)
    )
    station = bpy.context.active_object
    station.name = "BlackNexus_Station"
    station.scale = (15 * scale_factor, 10 * scale_factor, 6 * scale_factor)
    bpy.ops.object.transform_apply(scale=True) # Apply scale before material
    station.data.materials.append(materials["BlackNexus_Exterior"])
    all_objects.append(station)


    # Create the entrance (rusted hatch)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=1.5 * scale_factor,
        depth=0.5 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0] - 7 * scale_factor, location[1] + 5 * scale_factor, location[2] + 0.25 * scale_factor) # Move to front face
    )
    hatch = bpy.context.active_object
    hatch.name = "BlackNexus_Hatch"
    hatch.rotation_euler = (math.pi/2, 0, 0) # Rotate to lay flat on front face

    hatch_material = bpy.data.materials.new(name="Hatch_Material")
    hatch_material.use_nodes = True
    nodes = hatch_material.node_tree.nodes
    links = hatch_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    noise = nodes.new(type='ShaderNodeTexNoise')
    mapping = nodes.new(type='ShaderNodeMapping')
    texcoord = nodes.new(type='ShaderNodeTexCoord')
    colorramp = nodes.new(type='ShaderNodeValToRGB')
    principled.inputs['Metallic'].default_value = 0.8
    principled.inputs['Roughness'].default_value = 0.9
    noise.inputs['Scale'].default_value = 10.0
    noise.inputs['Detail'].default_value = 8.0
    colorramp.color_ramp.elements[0].position = 0.3
    colorramp.color_ramp.elements[0].color = (0.4, 0.1, 0.05, 1.0)  # Rust color
    colorramp.color_ramp.elements[1].position = 0.7
    colorramp.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0)  # Metal color
    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    hatch.data.materials.append(hatch_material)
    all_objects.append(hatch)

    # Create flickering neon sign
    bpy.ops.mesh.primitive_plane_add(
        size=1, # Scale later
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] + 5.1 * scale_factor, location[2] + 5 * scale_factor) # Front face offset
    )
    sign = bpy.context.active_object
    sign.name = "BlackNexus_Sign"
    sign.scale = (5 * scale_factor, 1 * scale_factor, 1) # Sign dimensions
    sign.rotation_euler = (math.pi/2, 0, 0) # Rotate to face front

    sign_material = bpy.data.materials.new(name="NexusSign_Material")
    sign_material.use_nodes = True
    nodes = sign_material.node_tree.nodes
    links = sign_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.0, 0.8, 1.0, 1.0)  # Cyan
    emission.inputs['Strength'].default_value = 3.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    sign.data.materials.append(sign_material)
    all_objects.append(sign)

    # Create graffiti
    graffiti = []
    for i in range(3):
        graffiti_x = location[0] + random.uniform(-7, 7) * scale_factor
        graffiti_y = location[1] + 5.01 * scale_factor # Slightly off front face
        graffiti_z = location[2] + random.uniform(1, 5) * scale_factor # Adjusted Z range

        bpy.ops.mesh.primitive_plane_add(
            size=random.uniform(1, 2) * scale_factor, # Smaller graffiti
            enter_editmode=False,
            align='WORLD',
            location=(graffiti_x, graffiti_y, graffiti_z)
        )
        graf = bpy.context.active_object
        graf.name = f"BlackNexus_Graffiti_{i}"
        graf.rotation_euler = (math.pi/2, 0, 0) # Rotate to face front
        graf.data.materials.append(materials["Binary_Neon"])
        graffiti.append(graf)
        all_objects.append(graf)

    # Create acid rain streaks
    streaks = []
    for i in range(5):
        streak_x = location[0] + random.uniform(-7, 7) * scale_factor
        streak_y = location[1] + 5.02 * scale_factor # Slightly off front face, further than graffiti
        streak_z_top = location[2] + 6 * scale_factor # Start near top edge
        streak_length = random.uniform(1.0, 4.0) * scale_factor

        bpy.ops.mesh.primitive_plane_add(
            size=1, # Scale later
            enter_editmode=False,
            align='WORLD',
            location=(streak_x, streak_y, streak_z_top - streak_length / 2) # Position center
        )
        streak = bpy.context.active_object
        streak.name = f"BlackNexus_AcidStreak_{i}"
        streak.scale = (0.1 * scale_factor, streak_length / 2, 1) # Thin and long
        streak.rotation_euler = (math.pi/2, 0, 0) # Rotate to face front

        streak_material = bpy.data.materials.new(name=f"AcidStreak_{i}")
        streak_material.use_nodes = True
        nodes = streak_material.node_tree.nodes
        links = streak_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.2, 0.3, 0.1, 1.0) # Greenish
        principled.inputs['Metallic'].default_value = 0.0
        principled.inputs['Roughness'].default_value = 0.3
        principled.inputs['Transmission Weight'].default_value = 0.8 # Translucent
        principled.inputs['Alpha'].default_value = 0.5 # Make slightly transparent
        streak_material.blend_method = 'BLEND' # Enable alpha blending
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        streak.data.materials.append(streak_material)
        streaks.append(streak)
        all_objects.append(streak)

    # Move all to collection
    for obj in all_objects:
        move_to_collection(obj, nexus_collection)

    return {
        "station": station,
        "hatch": hatch,
        "sign": sign,
        "graffiti": graffiti,
        "acid_streaks": streaks,
        "collection": nexus_collection
    }

# --- (Code from the previous response above this line) ---

# Create Wire Nest (Mid Tier hacker den)
def create_wire_nest(collections, materials, location=(30, -60, 0), scale_factor=1.0):
    """Create the Wire Nest hacker den as described in the requirements"""
    nest_collection = collections["MidTier"].children.get("Wire_Nest")
    if not nest_collection:
        nest_collection = bpy.data.collections.new("Wire_Nest")
        collections["MidTier"].children.link(nest_collection)

    all_objects = []

    # --- Start Continuation ---

    # Create the billboard frame structure
    # Use wireframe modifier for skeletal look instead of deleting faces
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False, # Add modifier in object mode
        align='WORLD',
        location=(location[0], location[1], location[2] + 15 * scale_factor)
    )
    frame = bpy.context.active_object
    frame.name = "WireNest_Frame"
    frame.scale = (10 * scale_factor, 0.5 * scale_factor, 15 * scale_factor) # Make frame thinner
    bpy.ops.object.transform_apply(scale=True) # Apply scale before modifier

    # Add Wireframe Modifier
    wireframe_mod = frame.modifiers.new(name="SkeletalFrame", type='WIREFRAME')
    wireframe_mod.thickness = 0.1 * scale_factor
    wireframe_mod.use_replace = False # Keep original mesh edges
    wireframe_mod.material_offset = 1 # Use second material slot for wires if needed

    frame.data.materials.append(materials["WireNest_Exterior"])
    # Optionally add a second material slot for the wires if you want them different
    # frame.data.materials.append(materials["WireNest_Exterior"])
    all_objects.append(frame)


    # Create shredded holo-ads draped on the frame
    ads = []
    for i in range(3):
        ad_x = location[0] + random.uniform(-8, 8) * scale_factor
        ad_y = location[1] + random.uniform(-0.5, 0.5) * scale_factor # Slight Y variation
        ad_z = location[2] + random.uniform(5, 25) * scale_factor # Wider Z range

        bpy.ops.mesh.primitive_plane_add(
            size=random.uniform(4, 7) * scale_factor, # Random size
            enter_editmode=False, # Edit after creation
            align='WORLD',
            location=(ad_x, ad_y, ad_z)
        )
        ad = bpy.context.active_object
        ad.name = f"WireNest_HoloAd_{i}"

        # Random rotation to look draped
        ad.rotation_euler = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(0, math.pi * 2))

        # Edit the mesh to create torn/shredded look
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(ad.data)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=random.randint(3, 5))
        verts_to_move = [v for v in bm.verts if random.random() > 0.6]
        for vert in verts_to_move:
            vert.co.x += random.uniform(-0.5, 0.5) * scale_factor
            vert.co.y += random.uniform(-0.5, 0.5) * scale_factor
            vert.co.z += random.uniform(-0.5, 0.5) * scale_factor

        # Add some holes
        faces_to_delete = [f for f in bm.faces if random.random() > 0.8]
        if faces_to_delete:
             bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')

        bmesh.update_edit_mesh(ad.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        ad_material = bpy.data.materials.new(name=f"HoloAd_Shredded_{i}")
        ad_material.use_nodes = True
        nodes = ad_material.node_tree.nodes
        links = ad_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled') # Base for torn parts
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        noise = nodes.new(type='ShaderNodeTexNoise') # Noise to mix between emission/dark

        principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0) # Dark torn parts
        principled.inputs['Roughness'].default_value = 0.8
        emission.inputs['Color'].default_value = (1.0, 0.5, 0.0, 1.0)  # Orange "Buy Ziggurat Augs!"
        emission.inputs['Strength'].default_value = 2.0
        noise.inputs['Scale'].default_value = 5.0

        links.new(noise.outputs['Fac'], mix_shader.inputs['Fac'])
        links.new(emission.outputs['Emission'], mix_shader.inputs[1]) # Use Shader input 1 (was 0)
        links.new(principled.outputs['BSDF'], mix_shader.inputs[2]) # Use Shader input 2 (was 1)
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

        ad_material.blend_method = 'BLEND' # Enable alpha if using transparency later
        ad.data.materials.append(ad_material)
        ads.append(ad)
        all_objects.append(ad)

    # Create rope ladder (simple cylinder for now)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=0.2 * scale_factor,
        depth=15 * scale_factor, # Make it reach lower
        enter_editmode=False,
        align='WORLD',
        location=(location[0] + 8 * scale_factor, location[1], location[2] + 7.5 * scale_factor) # Position near edge
    )
    ladder = bpy.context.active_object
    ladder.name = "WireNest_Ladder"
    ladder.rotation_euler = (0, random.uniform(-0.1, 0.1), 0) # Slight swing

    rope_material = bpy.data.materials.new(name="Rope_Material")
    rope_material.use_nodes = True
    nodes = rope_material.node_tree.nodes
    links = rope_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.3, 0.2, 0.1, 1.0)  # Brown
    principled.inputs['Roughness'].default_value = 0.9
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    ladder.data.materials.append(rope_material)
    all_objects.append(ladder)

    # Create hammocks and platforms (simple planes)
    platforms = []
    for i in range(3):
        platform_x = location[0] + random.uniform(-5, 5) * scale_factor
        platform_y = location[1] + random.uniform(-0.2, 0.2) * scale_factor # Center around frame Y
        platform_z = location[2] + (5 + i * 5 + random.uniform(-1, 1)) * scale_factor # Varied heights

        bpy.ops.mesh.primitive_plane_add(
            size=random.uniform(2, 4) * scale_factor, # Random size
            enter_editmode=False,
            align='WORLD',
            location=(platform_x, platform_y, platform_z)
        )
        platform = bpy.context.active_object
        platform.name = f"WireNest_Platform_{i}"
        platform.rotation_euler.z = random.uniform(0, math.pi/4) # Random rotation

        platform_material = bpy.data.materials.new(name=f"Platform_{i}")
        platform_material.use_nodes = True
        nodes = platform_material.node_tree.nodes
        links = platform_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
        principled.inputs['Metallic'].default_value = 0.7
        principled.inputs['Roughness'].default_value = 0.6
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        platform.data.materials.append(platform_material)
        platforms.append(platform)
        all_objects.append(platform)

    # Create central "data tree" sculpture
    bpy.ops.mesh.primitive_cone_add( # Use cone for base shape
        vertices=8,
        radius1=1.5 * scale_factor,
        radius2=0.2 * scale_factor,
        depth=10 * scale_factor,
        enter_editmode=False, # Edit after creation
        align='WORLD',
        location=(location[0], location[1], location[2] + 5 * scale_factor) # Start lower
    )
    tree = bpy.context.active_object
    tree.name = "WireNest_DataTree"

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(tree.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Extrude branches randomly
    for _ in range(8): # Add more branches
        side_faces = [f for f in bm.faces if abs(f.normal.z) < 0.8 and f.calc_center_median().z > 1.0] # Faces on the side, not base
        if not side_faces: continue
        face_to_extrude = random.choice(side_faces)

        ret = bmesh.ops.extrude_face_region(bm, geom=[face_to_extrude])
        extruded_face = [f for f in ret['geom'] if isinstance(f, bmesh.types.BMFace)][0]
        extruded_verts = list(extruded_face.verts)

        # Translate outwards and upwards slightly
        extrude_dir = face_to_extrude.normal * random.uniform(1, 3) * scale_factor
        extrude_dir.z += random.uniform(0.5, 1.5) * scale_factor
        bmesh.ops.translate(bm, vec=extrude_dir, verts=extruded_verts)

        # Scale down
        bmesh.ops.scale(bm, vec=(0.5, 0.5, 0.5), verts=extruded_verts, space=Matrix.Translation(-extruded_face.calc_center_median()))

    bmesh.update_edit_mesh(tree.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    tree_material = bpy.data.materials.new(name="DataTree_Material")
    tree_material.use_nodes = True
    nodes = tree_material.node_tree.nodes
    links = tree_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.0, 0.5, 1.0, 1.0)  # Blue
    emission.inputs['Strength'].default_value = 2.0 # Less intense
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    tree.data.materials.append(tree_material)
    all_objects.append(tree)

    # Create spider web graffiti on ceiling (using plane for simplicity)
    bpy.ops.mesh.primitive_plane_add(
        size=8 * scale_factor, # Smaller web
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 29 * scale_factor) # Near the top inside frame
    )
    web = bpy.context.active_object
    web.name = "WireNest_SpiderWeb"

    web_material = bpy.data.materials.new(name="SpiderWeb_Material")
    web_material.use_nodes = True
    nodes = web_material.node_tree.nodes
    links = web_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    # Texture would be better here, using emission for now
    emission.inputs['Color'].default_value = (0.0, 0.8, 0.2, 1.0)  # Green
    emission.inputs['Strength'].default_value = 1.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    web.data.materials.append(web_material)
    all_objects.append(web)

    # Move all to collection
    for obj in all_objects:
        move_to_collection(obj, nest_collection)

    return {
        "frame": frame,
        "ads": ads,
        "ladder": ladder,
        "platforms": platforms,
        "data_tree": tree,
        "spider_web": web,
        "collection": nest_collection
    }


# Create Rust Vault (Lower Tier hacker den)
def create_rust_vault(collections, materials, location=(-40, 20, 0), scale_factor=1.0):
    """Create the Rust Vault hacker den as described in the requirements"""
    vault_collection = collections["LowerTier"].children.get("Rust_Vault")
    if not vault_collection:
        vault_collection = bpy.data.collections.new("Rust_Vault")
        collections["LowerTier"].children.link(vault_collection)

    all_objects = []

    # Create the vault door
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=5 * scale_factor,
        depth=1 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] + 0.5 * scale_factor, location[2] + 5 * scale_factor) # Slightly offset Y for placement
    )
    door = bpy.context.active_object
    door.name = "RustVault_Door"
    door.rotation_euler = (math.pi/2, 0, 0) # Rotate to face front
    door.data.materials.append(materials["RustVault_Exterior"])
    all_objects.append(door)

    # Create laser scorch marks on the door (planes with dark material)
    scorch_marks = []
    for i in range(5):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(1, 4) * scale_factor
        # Calculate position on the rotated door face (Y is depth, Z is vertical)
        scorch_x = location[0] + radius * math.cos(angle)
        scorch_y = location[1] + 0.51 * scale_factor # Slightly proud of door surface
        scorch_z = location[2] + 5 * scale_factor + radius * math.sin(angle)

        bpy.ops.mesh.primitive_plane_add(
            size=random.uniform(0.5, 1.5) * scale_factor,
            enter_editmode=False,
            align='WORLD',
            location=(scorch_x, scorch_y, scorch_z)
        )
        scorch = bpy.context.active_object
        scorch.name = f"RustVault_Scorch_{i}"
        scorch.rotation_euler = (math.pi/2, 0, random.uniform(0, math.pi)) # Align with door face

        scorch_material = bpy.data.materials.new(name=f"Scorch_{i}")
        scorch_material.use_nodes = True
        nodes = scorch_material.node_tree.nodes
        links = scorch_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.01, 0.005, 0.002, 1.0) # Very dark brown/black
        principled.inputs['Metallic'].default_value = 0.0
        principled.inputs['Roughness'].default_value = 0.9
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        scorch.data.materials.append(scorch_material)
        scorch_marks.append(scorch)
        all_objects.append(scorch)

    # Create "No Entry" holo-sign
    bpy.ops.mesh.primitive_plane_add(
        size=1, # Scale later
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] + 0.6 * scale_factor, location[2] + 8 * scale_factor) # Above door, slightly forward
    )
    sign = bpy.context.active_object
    sign.name = "RustVault_Sign"
    sign.scale = (3 * scale_factor, 1 * scale_factor, 1) # Sign dimensions
    sign.rotation_euler = (math.pi/2, 0, 0) # Rotate to face outward

    sign_material = bpy.data.materials.new(name="NoEntry_Sign")
    sign_material.use_nodes = True
    nodes = sign_material.node_tree.nodes
    links = sign_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Red
    emission.inputs['Strength'].default_value = 2.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    sign.data.materials.append(sign_material)
    all_objects.append(sign)

    # Create the vault interior hint (dark cube behind door)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] - 4 * scale_factor, location[2] + 5 * scale_factor) # Positioned behind door
    )
    interior = bpy.context.active_object
    interior.name = "RustVault_Interior"
    interior.scale = (8 * scale_factor, 8 * scale_factor, 8 * scale_factor) # Smaller interior box
    bpy.ops.object.transform_apply(scale=True)

    interior_material = bpy.data.materials.new(name="Vault_Interior")
    interior_material.use_nodes = True
    nodes = interior_material.node_tree.nodes
    links = interior_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.005, 0.005, 0.005, 1.0)  # Very dark
    principled.inputs['Metallic'].default_value = 0.7
    principled.inputs['Roughness'].default_value = 0.8
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    interior.data.materials.append(interior_material)
    all_objects.append(interior)

    # Create a single red neon tube inside
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=0.1 * scale_factor,
        depth=5 * scale_factor,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1] - 5 * scale_factor, location[2] + 8 * scale_factor) # Inside interior box
    )
    tube = bpy.context.active_object
    tube.name = "RustVault_NeonTube"
    tube.rotation_euler = (0, math.pi/2, 0) # Rotate horizontal

    tube_material = bpy.data.materials.new(name="RedNeon_Tube")
    tube_material.use_nodes = True
    nodes = tube_material.node_tree.nodes
    links = tube_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Red
    emission.inputs['Strength'].default_value = 3.0
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    tube.data.materials.append(tube_material)
    all_objects.append(tube)

    # Create leaking pipes near the vault (outside, suggesting connection)
    pipes = []
    for i in range(3):
        pipe_x = location[0] + random.uniform(-5, 5) * scale_factor
        pipe_y = location[1] + 0.5 * scale_factor # Start near vault door face
        pipe_z_start = location[2] + random.uniform(8, 10) * scale_factor # Start high
        pipe_len = random.uniform(2, 5) * scale_factor

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.3 * scale_factor,
            depth=pipe_len,
            enter_editmode=False,
            align='WORLD',
            location=(pipe_x, pipe_y + pipe_len/2, pipe_z_start) # Position center of length
        )
        pipe = bpy.context.active_object
        pipe.name = f"RustVault_Pipe_{i}"
        pipe.rotation_euler = (math.pi/2, 0, random.uniform(-0.1, 0.1)) # Pointing roughly outwards

        pipe_material = bpy.data.materials.new(name=f"Pipe_{i}")
        pipe_material.use_nodes = True
        nodes = pipe_material.node_tree.nodes
        links = pipe_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        # Use RustVault material for consistency
        principled.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)
        principled.inputs['Metallic'].default_value = 0.8
        principled.inputs['Roughness'].default_value = 0.4
        # Add rust effect like vault door
        noise = nodes.new(type='ShaderNodeTexNoise')
        mapping = nodes.new(type='ShaderNodeMapping')
        texcoord = nodes.new(type='ShaderNodeTexCoord')
        colorramp = nodes.new(type='ShaderNodeValToRGB')
        noise.inputs['Scale'].default_value = 12.0
        noise.inputs['Detail'].default_value = 8.0
        colorramp.color_ramp.elements[0].position = 0.4
        colorramp.color_ramp.elements[0].color = (0.3, 0.1, 0.05, 1.0) # Rust
        colorramp.color_ramp.elements[1].position = 0.6
        colorramp.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0) # Metal
        links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        pipe.data.materials.append(pipe_material)
        pipes.append(pipe)
        all_objects.append(pipe)

    # Create a safe/stash box (optional, maybe inside the hinted interior?)
    # Let's place it just outside for visual interest
    bpy.ops.mesh.primitive_cube_add(
        size=1, # Scale later
        enter_editmode=False,
        align='WORLD',
        location=(location[0] + 5 * scale_factor, location[1] + 2 * scale_factor, location[2] + 1 * scale_factor) # Near vault, on ground
    )
    safe = bpy.context.active_object
    safe.name = "RustVault_Safe"
    safe.scale = (1.5 * scale_factor, 1.5 * scale_factor, 1.5 * scale_factor) # Small safe
    bpy.ops.object.transform_apply(scale=True)

    safe_material = bpy.data.materials.new(name="Safe_Material")
    safe_material.use_nodes = True
    nodes = safe_material.node_tree.nodes
    links = safe_material.node_tree.links
    for node in nodes: nodes.remove(node)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark gray
    principled.inputs['Metallic'].default_value = 0.9
    principled.inputs['Roughness'].default_value = 0.3
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    safe.data.materials.append(safe_material)
    all_objects.append(safe)

    # Create EMP grenades (optional, maybe just imply content)
    # Let's skip modelling tiny grenades for now, focus on building structure
    grenades = []

    # Move all to collection
    for obj in all_objects:
        move_to_collection(obj, vault_collection)

    return {
        "door": door,
        "sign": sign,
        "interior": interior,
        "neon_tube": tube,
        "scorch_marks": scorch_marks,
        "pipes": pipes,
        "safe": safe,
        "grenades": grenades, # Empty list for now
        "collection": vault_collection
    }

# Create Militech Armory
def create_militech_armory(collections, materials, location=(80, 20, 0), scale_factor=1.0):
    """Create the Militech Armory as described in the requirements"""
    militech_collection = collections["UpperTier"].children.get("Militech_Armory")
    if not militech_collection:
        militech_collection = bpy.data.collections.new("Militech_Armory")
        collections["UpperTier"].children.link(militech_collection)

    all_objects = []

    # Create the main fortress-like cube
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + 25 * scale_factor) # Centered height
    )
    fortress = bpy.context.active_object
    fortress.name = "Militech_Fortress"
    fortress.scale = (25 * scale_factor, 25 * scale_factor, 50 * scale_factor)
    bpy.ops.object.transform_apply(scale=True)
    fortress.data.materials.append(materials["Militech_Exterior"])
    all_objects.append(fortress)

    # Create turret ports (simple cylinders for now)
    turrets = []
    num_levels = 3
    num_sides = 4
    half_width = 12.5 * scale_factor # Half of fortress scale X/Y
    height_step = (50 * scale_factor) / (num_levels + 1) # Distribute height

    for level in range(num_levels):
        for side in range(num_sides):
            turret_z = location[2] + height_step * (level + 1)
            pos = Vector((0,0,0))
            rot_y = 0

            if side == 0: # Front (+Y)
                pos = Vector((location[0] + random.uniform(-half_width*0.8, half_width*0.8), location[1] + half_width + 0.1*scale_factor, turret_z))
                rot_y = 0
            elif side == 1: # Right (+X)
                pos = Vector((location[0] + half_width + 0.1*scale_factor, location[1] + random.uniform(-half_width*0.8, half_width*0.8), turret_z))
                rot_y = math.pi/2
            elif side == 2: # Back (-Y)
                pos = Vector((location[0] + random.uniform(-half_width*0.8, half_width*0.8), location[1] - half_width - 0.1*scale_factor, turret_z))
                rot_y = math.pi
            else: # Left (-X)
                pos = Vector((location[0] - half_width - 0.1*scale_factor, location[1] + random.uniform(-half_width*0.8, half_width*0.8), turret_z))
                rot_y = -math.pi/2

            bpy.ops.mesh.primitive_cylinder_add(
                vertices=16,
                radius=1.5 * scale_factor, # Smaller turrets
                depth=0.5 * scale_factor,
                enter_editmode=False,
                align='WORLD',
                location=pos
            )
            turret = bpy.context.active_object
            turret.name = f"Militech_Turret_{level}_{side}"
            turret.rotation_euler = (math.pi/2, 0, rot_y) # Point outwards
            turret.data.materials.append(materials["Militech_Accent"]) # Use accent for the port itself
            turrets.append(turret)
            all_objects.append(turret)

    # Create red neon accents along vertical edges
    accents = []
    edge_positions = [
        (location[0] + half_width, location[1] + half_width),
        (location[0] + half_width, location[1] - half_width),
        (location[0] - half_width, location[1] - half_width),
        (location[0] - half_width, location[1] + half_width),
    ]
    for i, (accent_x, accent_y) in enumerate(edge_positions):
        accent_z = location[2] + 25 * scale_factor # Center Z

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.3 * scale_factor, # Thinner accent
            depth=50 * scale_factor, # Full height
            enter_editmode=False,
            align='WORLD',
            location=(accent_x, accent_y, accent_z)
        )
        accent = bpy.context.active_object
        accent.name = f"Militech_Accent_{i}"
        accent.data.materials.append(materials["Militech_Accent"])
        accents.append(accent)
        all_objects.append(accent)

    # Move all to collection
    for obj in all_objects:
        move_to_collection(obj, militech_collection)

    return {
        "fortress": fortress,
        "turrets": turrets,
        "accents": accents,
        "collection": militech_collection
    }

# Create Biotechnica Spire
def create_biotechnica_spire(collections, materials, location=(-80, 80, 0), scale_factor=1.0):
    """Create the Biotechnica Spire as described in the requirements"""
    biotechnica_collection = collections["UpperTier"].children.get("Biotechnica_Spire")
    if not biotechnica_collection:
        biotechnica_collection = bpy.data.collections.new("Biotechnica_Spire")
        collections["UpperTier"].children.link(biotechnica_collection)

    all_objects = []

    # Create the main bio-domed tower base
    tower_height = 80 * scale_factor
    tower_radius = 15 * scale_factor
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=tower_radius,
        depth=tower_height,
        enter_editmode=False,
        align='WORLD',
        location=(location[0], location[1], location[2] + tower_height / 2) # Center Z
    )
    tower = bpy.context.active_object
    tower.name = "Biotechnica_Tower"
    tower.data.materials.append(materials["Biotechnica_Exterior"])
    all_objects.append(tower)

    # Create the bio-dome on top
    dome_radius = 20 * scale_factor
    dome_center_z = location[2] + tower_height # Place dome base at top of tower

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32,
        ring_count=16,
        radius=dome_radius,
        enter_editmode=False, # Edit after creation
        align='WORLD',
        location=(location[0], location[1], dome_center_z) # Center sphere at tower top
    )
    dome = bpy.context.active_object
    dome.name = "Biotechnica_Dome"

    # Cut the bottom half using Bisect
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(dome.data)
    # Ensure lookup tables are updated
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Bisect the sphere horizontally at its local origin (z=0)
    plane_co = (0, 0, 0)  # Local Z=0
    plane_no = (0, 0, 1)  # Normal pointing up (we want to clear geometry BELOW)

    try:
        # Perform the bisection
        # IMPORTANT: Use geom=bm.faces[:] + bm.edges[:] + bm.verts[:] to affect the whole mesh
        result = bmesh.ops.bisect_plane(bm,
                                        geom=list(bm.faces) + list(bm.edges) + list(bm.verts),
                                        plane_co=plane_co,
                                        plane_no=plane_no,
                                        clear_inner=False, # Don't clear above
                                        clear_outer=True)  # Clear below the plane

        # Optionally fill the hole created by bisect if needed
        # Bisect often creates the closing face automatically if dist is small enough
        # Check if a hole exists after bisect
        bm.edges.ensure_lookup_table() # Update after bisect
        boundary_edges = [e for e in bm.edges if not e.is_boundary] # Or check len(e.link_faces) == 1
        # If a boundary loop exists, try filling it (less likely needed after bisect)
        # if boundary_edges:
        #    print("Boundary edges found after bisect, attempting fill...")
        #    try:
        #        bmesh.ops.fill(bm, edges=boundary_edges)
        #    except Exception as e_fill:
        #        print(f"Fill failed after bisect: {e_fill}")

    except Exception as e_bisect:
        print(f"Error during BMesh bisect for dome bottom: {e_bisect}")


    bmesh.update_edit_mesh(dome.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    dome.data.materials.append(materials["Biotechnica_Exterior"])
    all_objects.append(dome)


    # Create vines creeping up the facade (Use curves for better control)
        # Create vines creeping up the facade (Use curves for better control)
    vines = []
    for i in range(8):
        # Create a Bezier curve - start simpler, maybe just a line first?
        bpy.ops.curve.primitive_bezier_circle_add(radius=tower_radius * 1.01,
                                                 location=(location[0], location[1], location[2]+5*scale_factor))
        # Keep track of the active object
        if not bpy.context.object or bpy.context.object.type != 'CURVE':
             print("Error: Failed to create vine curve object.")
             continue # Skip this vine if creation failed
        vine_curve_obj = bpy.context.object # More robust way to get created object
        vine_curve_obj.name = f"Biotechnica_Vine_Curve_{i}"
        vine_curve = vine_curve_obj.data
        vine_curve.dimensions = '3D'
        vine_curve.fill_mode = 'FULL'
        vine_curve.bevel_depth = 0.1 * scale_factor # Give thickness
        vine_curve.bevel_resolution = 2

        # --- Ensure we are operating on the correct object ---
        # Deselect all other objects
        bpy.ops.object.select_all(action='DESELECT')
        # Select and make the new curve active
        vine_curve_obj.select_set(True)
        bpy.context.view_layer.objects.active = vine_curve_obj

        # Select curve and go to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Ensure spline points exist
        if not vine_curve.splines or not vine_curve.splines[0].bezier_points:
            print(f"Warning: Vine curve {vine_curve_obj.name} has no points. Skipping extrusion.")
            bpy.ops.object.mode_set(mode='OBJECT') # Exit edit mode
            all_objects.append(vine_curve_obj) # Still add the empty curve object
            vines.append(vine_curve_obj)
            continue # Skip to next vine

        # Select a point to start the vine growth
        bpy.ops.curve.select_all(action='DESELECT')
        # Select the i-th point on the first spline (more direct selection)
        vine_curve.splines[0].bezier_points[i % len(vine_curve.splines[0].bezier_points)].select_control_point = True
        # Set one point as active (often the last selected) - crucial for ops
        # Try setting the active spline element index directly if possible/needed - might not be straightforward via python
        # Let's rely on the selection being enough for now. If error persists, this needs revisiting.

        # Extrude upwards randomly along the tower
        extrude_height = tower_height * random.uniform(0.6, 1.0)
        num_segments = 10
        for seg in range(num_segments):
            z_step = extrude_height / num_segments
            rand_offset = Vector((random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), z_step)) * scale_factor

            # Check selection before extruding
            # Get selected points directly from data
            selected_points = [p for spline in vine_curve.splines for p in spline.bezier_points if p.select_control_point]
            if not selected_points:
                 print(f"Error: No point selected before extrude segment {seg} for vine {i}. Breaking.")
                 break # Stop extruding this vine

            # Try extruding
            try:
                bpy.ops.curve.extrude_move(TRANSFORM_OT_translate={"value":rand_offset})
                # After extrude, the new point is usually selected/active
                # Optionally tilt handles
                bpy.ops.curve.handle_type_set(type='FREE_ALIGN')
                bpy.ops.transform.rotate(value=random.uniform(-0.5, 0.5), orient_axis='Z')
                bpy.ops.transform.rotate(value=random.uniform(-0.2, 0.2), orient_axis='X')
            except RuntimeError as e_extrude:
                print(f"RuntimeError during curve extrude/modify for vine {i}, segment {seg}: {e_extrude}")
                print("Skipping remaining segments for this vine.")
                break # Stop extruding this vine if an operation fails

        bpy.ops.object.mode_set(mode='OBJECT')

        # Create vine material (same as before)
        vine_material = bpy.data.materials.new(name=f"Vine_{i}")
        vine_material.use_nodes = True
        nodes = vine_material.node_tree.nodes
        links = vine_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.0, 0.4, 0.1, 1.0)  # Green
        principled.inputs['Roughness'].default_value = 0.8
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        if vine_curve_obj.data.materials: # Check if material slot exists
            vine_curve_obj.data.materials[0] = vine_material
        else:
            vine_curve_obj.data.materials.append(vine_material) # Assign material to curve data
        vines.append(vine_curve_obj)
        all_objects.append(vine_curve_obj)


    # Create labs with bubbling vats (simple cylinders, visible through glass)
    vats = []
    for i in range(5):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(tower_radius * 0.2, tower_radius * 0.8)
        vat_x = location[0] + radius * math.cos(angle)
        vat_y = location[1] + radius * math.sin(angle)
        vat_z = location[2] + random.uniform(tower_height * 0.1, tower_height * 0.9) # Within tower height

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=2 * scale_factor,
            depth=5 * scale_factor,
            enter_editmode=False,
            align='WORLD',
            location=(vat_x, vat_y, vat_z)
        )
        vat = bpy.context.active_object
        vat.name = f"Biotechnica_Vat_{i}"

        vat_material = bpy.data.materials.new(name=f"Vat_{i}")
        vat_material.use_nodes = True
        nodes = vat_material.node_tree.nodes
        links = vat_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = (0.0, 0.8, 0.2, 1.0)  # Bright green liquid
        principled.inputs['Metallic'].default_value = 0.0
        principled.inputs['Roughness'].default_value = 0.1
        principled.inputs['Transmission Weight'].default_value = 0.9  # Mostly transparent
        principled.inputs['IOR'].default_value = 1.33  # Water-like
        # Add emission for glow
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (0.1, 1.0, 0.3, 1.0)
        emission.inputs['Strength'].default_value = 0.5
        add_shader = nodes.new(type='ShaderNodeAddShader')
        links.new(principled.outputs['BSDF'], add_shader.inputs[0])
        links.new(emission.outputs['Emission'], add_shader.inputs[1])
        links.new(add_shader.outputs['Shader'], output.inputs['Surface'])
        vat_material.blend_method = 'BLEND' # For transparency
        vat.data.materials.append(vat_material)
        vats.append(vat)
        all_objects.append(vat)


    # Create holo-displays of DNA strands (planes with emission)
    displays = []
    for i in range(3):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(tower_radius * 0.2, tower_radius * 0.8)
        display_x = location[0] + radius * math.cos(angle)
        display_y = location[1] + radius * math.sin(angle)
        display_z = location[2] + random.uniform(tower_height * 0.2, tower_height * 0.8) # Within tower

        bpy.ops.mesh.primitive_plane_add(
            size=1, # Scale later
            enter_editmode=False,
            align='WORLD',
            location=(display_x, display_y, display_z)
        )
        display = bpy.context.active_object
        display.name = f"Biotechnica_DNADisplay_{i}"
        display.scale = (3*scale_factor, 5*scale_factor, 1) # Rectangular display

        display.rotation_euler = (random.uniform(0, math.pi), random.uniform(0, math.pi), random.uniform(0, math.pi)) # Random orientation

        display_material = bpy.data.materials.new(name=f"DNADisplay_{i}")
        display_material.use_nodes = True
        nodes = display_material.node_tree.nodes
        links = display_material.node_tree.links
        for node in nodes: nodes.remove(node)
        output = nodes.new(type='ShaderNodeOutputMaterial')
        emission = nodes.new(type='ShaderNodeEmission')
        # Add texture later for actual DNA image
        emission.inputs['Color'].default_value = (0.0, 0.8, 0.4, 1.0)  # Green display glow
        emission.inputs['Strength'].default_value = 2.0
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        display.data.materials.append(display_material)
        displays.append(display)
        all_objects.append(display)

    # Move all to collection
    for obj in all_objects:
        move_to_collection(obj, biotechnica_collection)

    return {
        "tower": tower,
        "dome": dome,
        "vines": vines,
        "vats": vats,
        "displays": displays,
        "collection": biotechnica_collection
    }


# --- (Code from the previous responses above this line) ---

# --- Main Execution ---

# Main function to generate all specific buildings
def generate_neon_crucible_buildings():
    """Generate all specific buildings for Neon Crucible"""
    print("Clearing scene...")
    clear_scene()

    print("Creating collections...")
    collections = create_collections()

    print("Creating basic materials...")
    basic_materials = create_materials()

    print("Creating advanced materials...")
    advanced_materials = create_advanced_materials()

    # Combine materials - advanced override basic if names clash (they shouldn't now)
    materials = {**basic_materials, **advanced_materials}

    # Add a simple ground plane for context
    print("Creating ground plane...")
    bpy.ops.mesh.primitive_plane_add(size=300, enter_editmode=False, align='WORLD', location=(0, 0, -0.1))
    ground = bpy.context.active_object
    ground.name = "Context_Ground"
    # Use the specific ground material if available, otherwise basic
    ground_mat_name = "Ground_Basic" # Default to basic
    # Check if a more specific one exists (e.g., from advanced materials or overrides)
    # This part is optional, depends if you create a specific ground later
    # if "Ground_Advanced" in materials: ground_mat_name = "Ground_Advanced"
    if ground_mat_name in materials:
        ground.data.materials.append(materials[ground_mat_name])
    else:
        print(f"Warning: Ground material '{ground_mat_name}' not found.")
    move_to_collection(ground, collections["Environment"])


    # Set up basic world lighting (optional, but helpful for viewing)
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("BasicWorld")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if not bg_node:
        bg_node = world.node_tree.nodes.new(type='ShaderNodeBackground')
        output_node = world.node_tree.nodes.get('World Output')
        if not output_node:
            output_node = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
        world.node_tree.links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])
    bg_node.inputs['Color'].default_value = (0.01, 0.01, 0.02, 1.0) # Dark blue ambient
    bg_node.inputs['Strength'].default_value = 0.5


    # Generate specific buildings
    print("Generating NeoTech Labs Tower...")
    neotech_tower = create_neotech_tower(collections, materials, location=(50, 50, 0))

    print("Generating Specter Station...")
    specter_station = create_specter_station(collections, materials, location=(0, 80, 0))

    print("Generating Black Nexus...")
    black_nexus = create_black_nexus(collections, materials, location=(-70, -50, 0))

    print("Generating Wire Nest...")
    wire_nest = create_wire_nest(collections, materials, location=(30, -60, 10)) # Elevate Wire Nest slightly

    print("Generating Rust Vault...")
    rust_vault = create_rust_vault(collections, materials, location=(-40, 20, 0))

    print("Generating Militech Armory...")
    militech_armory = create_militech_armory(collections, materials, location=(80, -20, 0)) # Adjusted location slightly

    print("Generating Biotechnica Spire...")
    biotechnica_spire = create_biotechnica_spire(collections, materials, location=(-80, 80, 0))

    # Optional: Add a camera
    print("Adding camera...")
    bpy.ops.object.camera_add(location=(150, -150, 60), rotation=(math.radians(65), 0, math.radians(45)))
    camera = bpy.context.active_object
    camera.name = "Landmark_View_Camera"
    bpy.context.scene.camera = camera

    print("Generating building interiors...")
    building_objects = {
        "neotech_tower": {"building": neotech_tower["tower"], "collection": neotech_tower["collection"]},
        "specter_station": {"building": specter_station["tower"], "collection": specter_station["collection"]},
        "black_nexus": {"building": black_nexus["station"], "collection": black_nexus["collection"]},
        "wire_nest": {"building": wire_nest["frame"], "collection": wire_nest["collection"]},
        "rust_vault": {"building": rust_vault["door"], "collection": rust_vault["collection"]},
        "militech_armory": {"building": militech_armory["fortress"], "collection": militech_armory["collection"]},
        "biotechnica_spire": {"building": biotechnica_spire["tower"], "collection": biotechnica_spire["collection"]},
    }
    try:
        building_interiors = building_interiors_module.implement_building_interiors(building_objects, materials)
    except Exception as e:
        print(f"Error generating building interiors: {e}")
        building_interiors = {}

    print("Generating building windows...")
    try:
        building_windows = building_windows_module.implement_building_windows(building_objects, materials, building_interiors)
    except Exception as e:
        print(f"Error generating building windows: {e}")
        building_windows = {}

    print("\nNeon Crucible specific buildings generation complete!")

    return {
        "collections": collections,
        "materials": materials,
        "neotech_tower": neotech_tower,
        "specter_station": specter_station,
        "black_nexus": black_nexus,
        "wire_nest": wire_nest,
        "rust_vault": rust_vault,
        "militech_armory": militech_armory,
        "biotechnica_spire": biotechnica_spire,
        "ground": ground,
        "camera": camera,
        "building_objects": building_objects,
        "building_interiors": building_interiors,
        "building_windows": building_windows
    }

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Execute the script if run directly from Blender's text editor
if __name__ == "__main__":
    import building_interiors as building_interiors_module
    import building_windows as building_windows_module
    generate_neon_crucible_buildings()
