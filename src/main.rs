use bevy::prelude::*;
mod terminal;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Data Heist at NeoTech Labs".into(),
                resolution: (800., 600.).into(),
                ..default()
            }),
            ..default()
        }))
        .add_plugins(bevy::gltf::GltfPlugin) // Explicitly add GLTF support
        .add_systems(Startup, (setup_camera, setup_world, terminal::setup_terminal))
        .add_systems(Update, (terminal::handle_input, terminal::update_terminal))
        .run();
}

fn setup_camera(mut commands: Commands) {
    commands.spawn(Camera3dBundle {
        transform: Transform::from_xyz(0.0, 1.5, 5.0).looking_at(Vec3::ZERO, Vec3::Y),
        ..default()
    });
}

fn setup_world(mut commands: Commands, asset_server: Res<AssetServer>) {
    info!("Loading hideout.glb...");
    let scene_handle = asset_server.load("models/hideout.glb");
    info!("Scene handle: {:?}", scene_handle.path());
    commands.spawn(SceneBundle {
        scene: scene_handle,
        transform: Transform::from_xyz(0.0, 0.0, 0.0),
        ..default()
    });
    commands.spawn(PointLightBundle {
        transform: Transform::from_xyz(0.0, 5.0, 0.0),
        point_light: PointLight {
            intensity: 1500.0,
            shadows_enabled: true,
            ..default()
        },
        ..default()
    });
}