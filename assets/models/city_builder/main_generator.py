# --- START OF FILE main_generator.py ---
import bpy
import sys
import os
import importlib
import traceback # Import traceback for detailed error printing

print("\n--- Script Start: main_generator.py ---")

# --- Determine Script Directory (More Robustly) ---
script_file_path = None
script_dir = None
print("Determining script directory...")

# Try getting path from the Text Editor context
context = bpy.context
space_data = getattr(context, 'space_data', None)
text_block = getattr(space_data, 'text', None) if space_data else None

if text_block:
    if text_block.filepath:
        try:
            script_file_path = bpy.path.abspath(text_block.filepath)
            script_dir = os.path.dirname(script_file_path)
            print(f" -> Method: Active Text Block (Saved): {script_dir}")
        except Exception as e:
             print(f" -> Warning: bpy.path.abspath failed on text_block.filepath ('{text_block.filepath}'): {e}")
             script_dir = None
    else:
        print(" -> Method: Active Text Block (Not Saved)")
        # Attempt to get blend file directory as a potential location for scripts
        if bpy.data.is_saved and bpy.data.filepath:
            blend_dir = os.path.dirname(bpy.path.abspath(bpy.data.filepath))
            print(f" -> Trying Blend file directory: {blend_dir}")
            # Check if a key script exists there
            potential_building_path = os.path.join(blend_dir, "building.py")
            if os.path.exists(potential_building_path):
                 script_dir = blend_dir
                 print(f" -> Found required scripts in Blend directory. Using: {script_dir}")
            else:
                 print(f" -> Could not find required scripts in Blend directory.")
                 script_dir = None
        else:
             print(" -> Blend file is also not saved. Cannot determine script directory via this method.")
             script_dir = None

elif '__file__' in locals() or '__file__' in globals():
     # Fallback: Try using __file__ if available
     try:
          script_file_path = os.path.abspath(__file__)
          script_dir = os.path.dirname(script_file_path)
          print(f" -> Method: __file__ attribute: {script_dir}")
     except NameError:
         print(" -> Method: __file__ not defined.")
         script_dir = None
     except Exception as e:
         print(f" -> Error resolving __file__: {e}")
         script_dir = None
else:
     print(" -> Method: No Text Editor context and __file__ not defined.")
     script_dir = None


# Final check and error if directory not found
if not script_dir or not os.path.isdir(script_dir):
     print("\nCRITICAL ERROR: Could not determine a valid directory containing the scripts.")
     print("Please ensure main_generator.py and all other .py modules (building.py, etc.)")
     print("are all saved in the SAME directory, and run main_generator.py from")
     print("Blender's Text Editor AFTER saving it.")
     raise Exception("Script directory could not be determined or is invalid. Please save all scripts.")
else:
     print(f"Using script directory: {script_dir}")


# --- Add Script Directory to sys.path ---
if script_dir not in sys.path:
    print(f"Adding script directory to sys.path: {script_dir}")
    sys.path.insert(0, script_dir) # Insert at beginning
else:
    print(f"Script directory already in sys.path.")


# --- Module Loading and Reloading (Revised) ---
# Define the modules we expect to load. Global variables with these names will be created.
module_names = ["building", "building_interiors", "building_rooms", "building_windows"]
modules_loaded_successfully = False
loaded_modules = {} # Keep track of successfully loaded modules

print("\n--- Loading / Reloading Modules ---")
for module_name in module_names:
    print(f"Processing module: '{module_name}'...")
    try:
        # Check if the actual .py file exists before attempting import/reload
        expected_path = os.path.join(script_dir, f"{module_name}.py")
        if not os.path.exists(expected_path):
            # Raise ImportError specifically so the outer catch handles it cleanly
            raise ImportError(f"File not found at expected location: {expected_path}")

        # Dynamically import or reload the module
        if module_name in sys.modules:
            print(f" -> Reloading existing module (from {sys.modules[module_name].__file__})")
            # Reload and assign to our tracking dictionary
            loaded_modules[module_name] = importlib.reload(sys.modules[module_name])
        else:
            print(f" -> Importing module for the first time")
            # Import and assign to our tracking dictionary
            loaded_modules[module_name] = importlib.import_module(module_name)

        # Verify successful load
        if loaded_modules.get(module_name) is not None:
            print(f" -> Module '{module_name}' is ready.")
        else:
            # This handles cases where import/reload failed silently
            raise ImportError(f"Module object for '{module_name}' is None after import/reload attempt.")

    except ImportError as e:
        print(f"\nERROR: Could not import or reload module '{module_name}'.")
        print(f"       Please ensure '{module_name}.py' exists and is saved in the script directory:")
        print(f"       '{script_dir}'")
        print(f"       Also check for syntax errors within the file.")
        print(f"       ImportError details: {e}")
        modules_loaded_successfully = False
        # traceback.print_exc() # Uncomment for more details if needed
        break # Stop trying to load other modules if one fails
    except Exception as e:
        print(f"\nAn unexpected error occurred while loading/reloading module '{module_name}':")
        traceback.print_exc() # Print full traceback for unexpected errors
        modules_loaded_successfully = False
        break
else:
    # This block executes if the loop completed without a 'break'
    modules_loaded_successfully = True
    print("--- Successfully imported/reloaded all specified modules. ---")


# --- Main Generation Function ---
def run_generation():
    # Check if essential modules were loaded
    building = loaded_modules.get("building")
    building_interiors = loaded_modules.get("building_interiors")
    # Get others
    building_rooms = loaded_modules.get("building_rooms")
    building_windows = loaded_modules.get("building_windows")


    if not modules_loaded_successfully or not building or not building_interiors:
         print("\nAborting generation: Essential modules (building, building_interiors) not loaded or failed during import.")
         return
    # Add checks for rooms/windows if they become essential before interiors etc.
    if not building_rooms:
         print("Warning: Module 'building_rooms' not loaded. Skipping room generation.")
    if not building_windows:
         print("Warning: Module 'building_windows' not loaded. Skipping window generation.")


    print("\n--- Starting Neon Crucible Generation ---")

    # 1. Generate Buildings
    print("Running building generation (clear scene, create collections, materials)...")
    generated_data = None # Initialize
    try:
        if not hasattr(building, 'generate_neon_crucible_buildings'):
             print(f"ERROR: Module 'building' does not have function 'generate_neon_crucible_buildings'")
             return
        generated_data = building.generate_neon_crucible_buildings()
    except Exception as e:
        print("\n--- ERROR DURING BUILDING GENERATION ---")
        traceback.print_exc()
        print("-----------------------------------------")
        return

    if not generated_data:
        print("Building generation returned no data or failed. Aborting.")
        return

    all_materials = generated_data.get("materials", {}) # Get the INITIAL materials dict
    print(f"Initial materials from building.py: {list(all_materials.keys())}")


    # --- <<< NEW SECTION: Create and Merge Interior Materials >>> ---
    print("Generating interior materials...")
    try:
        # Check if the function exists before calling
        if hasattr(building_interiors, 'create_interior_materials'):
            interior_mats_dict = building_interiors.create_interior_materials()
            if interior_mats_dict:
                print(f" -> Generated interior materials: {list(interior_mats_dict.keys())}")
                # Merge the interior materials into the main dictionary
                all_materials.update(interior_mats_dict)
                print(f" -> Merged materials. Current all_materials: {list(all_materials.keys())}")
            else:
                print(" -> Warning: create_interior_materials returned nothing.")
        else:
            print("ERROR: Module 'building_interiors' is missing the function 'create_interior_materials'. Cannot create interior materials.")
            # Depending on your design, you might want to return or raise an error here
            # For now, we let it continue, but subsequent steps will likely fail with KeyErrors.

    except Exception as e:
        print("\n--- ERROR DURING INTERIOR MATERIAL CREATION ---")
        traceback.print_exc()
        print("-----------------------------------------------")
        # Decide if we should abort here, maybe return?
        return
    # --- <<< END NEW SECTION >>> ---


    # 2. Implement Interiors
    print("Running interior implementation...")
    try:
        if not hasattr(building_interiors, 'implement_building_interiors'):
             print(f"ERROR: Module 'building_interiors' does not have function 'implement_building_interiors'")
             # Decide if this is critical - maybe just skip?
        else:
             # Pass generated_data (contains building objects) and the NOW MERGED materials dict
             # Note: implement_building_interiors might internally re-create its own combined dict,
             # but that's okay as long as it finds the materials it needs within the passed dict.
             # Its return value is still ignored here as per the original design.
            building_interiors.implement_building_interiors(
                generated_data,
                all_materials # Pass the merged dictionary
            )
            print("\nInterior implementation finished.")

    except Exception as e: # Catch any error during interior implementation
        print(f"\n--- An unexpected error occurred during interior implementation: ---")
        traceback.print_exc()
        print("--------------------------------------------------------------------")
        # Decide whether to continue if interiors fail


    # --- <<< INTEGRATION POINT FOR ROOMS >>> ---
    print("Running room generation...")
    print(f"generated_data: {generated_data}")
    if generated_data:
        try:
            if building_rooms: # Check if module was loaded
                if not hasattr(building_rooms, 'implement_building_rooms'):
                     print(f"ERROR: Module 'building_rooms' does not have function 'implement_building_rooms'")
                else:
                     # Call the function, passing generated data and the MERGED materials
                     building_rooms.implement_building_rooms(
                          generated_data.get("building_objects"),
                          all_materials, # Pass the merged dict
                          all_materials  # Pass the merged dict again as the expected interior_materials
                     )
                     print("\nRoom generation finished.")
            else:
                 print("Skipping room generation - module not loaded.")
        except Exception as e:
             print("\n--- ERROR DURING ROOM GENERATION ---")
             traceback.print_exc()
             print("------------------------------------")
             # Decide whether to continue
    else:
        print("Skipping room generation - generated_data is None.")
    # --- <<< END ROOMS INTEGRATION >>> ---


    # --- <<< INTEGRATION POINT FOR WINDOWS >>> ---
    print("Running window generation...")
    print(f"generated_data: {generated_data}")
    if generated_data:
        try:
            if building_windows: # Check if module was loaded
                 if not hasattr(building_windows, 'implement_building_windows'):
                      print(f"ERROR: Module 'building_windows' does not have function 'implement_building_windows'")
                 else:
                      # Call the function, passing generated data and the MERGED materials
                      building_windows.implement_building_windows(
                           generated_data.get("building_objects"),
                           all_materials, # Pass the merged dict
                           all_materials  # Pass the merged dict again as the expected interior_materials
                      )
                      print("\nWindow generation finished.")
            else:
                 print("Skipping window generation - module not loaded.")
        except Exception as e:
             print("\n--- ERROR DURING WINDOW GENERATION ---")
             traceback.print_exc()
             print("--------------------------------------")
             # Decide whether to continue
    else:
        print("Skipping window generation - generated_data is None.")
    # --- <<< END WINDOWS INTEGRATION >>> ---


    print("\n--- Generation Complete ---")
    print("Note: Hide exterior objects (H) or use Local View (Numpad /) to see interiors, rooms, windows.")


# --- Run the Main Function ---
if __name__ == "__main__":
    print(f"\nExecuting script: {__name__}")
    # Ensure we are in Object Mode before starting
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            print("Switched to Object Mode.")
        except RuntimeError as e:
            print(f"Warning: Could not set object mode automatically: {e}. Current mode: {bpy.context.mode}")
            # Don't necessarily stop, but warn the user
            print("         Please ensure you are in Object Mode before running the script if issues occur.")


    # Execute the generation within a try block for overall error catching
    print("\nExecuting main generation logic...")
    try:
        run_generation()
    except Exception as e:
        print("\n--- CRITICAL ERROR DURING SCRIPT EXECUTION ---")
        traceback.print_exc()
        print("---------------------------------------------")


print("\n--- Script End: main_generator.py ---")
# --- END OF FILE main_generator.py ---
