use bevy::prelude::*;
use bevy::input::keyboard::KeyboardInput; // Explicit import

#[derive(Resource, Default)]
pub struct TerminalState {
    input: String,
}

pub fn setup_terminal(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    commands.insert_resource(TerminalState::default());
    
    // Terminal background sprite
    let bg_material = materials.add(StandardMaterial {
        base_color: Color::srgb(0.0, 0.0, 0.0),
        base_color_texture: Some(asset_server.load("sprites/terminal_bg.png")),
        alpha_mode: AlphaMode::Blend,
        unlit: true,
        ..default()
    });
    commands.spawn(PbrBundle {
        mesh: meshes.add(Rectangle::new(4.0, 3.0)),
        material: bg_material,
        transform: Transform::from_xyz(0.0, 1.5, 0.0),
        ..default()
    });

    // Terminal text
    let font_handle = asset_server.load("fonts/FiraMono-Regular.ttf");
    commands.spawn(Text2dBundle {
        text: Text {
            sections: vec![
                TextSection {
                    value: "Initializing...\n> Welcome to the dark pool, runner.\n".to_string(),
                    style: TextStyle {
                        font: font_handle.clone(),
                        font_size: 24.0,
                        color: Color::srgb(0.0, 1.0, 0.0),
                    },
                },
                TextSection {
                    value: "> ".to_string(),
                    style: TextStyle {
                        font: font_handle,
                        font_size: 24.0,
                        color: Color::srgb(0.0, 1.0, 0.0),
                    },
                },
            ],
            ..default()
        },
        transform: Transform::from_xyz(-1.8, 1.2, 0.1), // Adjusted for 3D
        ..default()
    });
}

pub fn handle_input(
    mut key_evr: EventReader<KeyboardInput>,
    keys: Res<ButtonInput<KeyCode>>,
    mut state: ResMut<TerminalState>,
    mut text_query: Query<&mut Text>,
) {
    let mut text = text_query.single_mut();
    for ev in key_evr.read() {
        if ev.state.is_pressed() {
            // Changed this line - ev.key_code is already a KeyCode, not an Option<KeyCode>
            let key_code = ev.key_code;
            if let Some(c) = keycode_to_char(key_code) {
                if c.is_alphanumeric() || c.is_whitespace() || c == '.' {
                    state.input.push(c);
                    text.sections[1].value.push(c);
                }
            }
        }
    }
    if keys.just_pressed(KeyCode::Backspace) && !state.input.is_empty() {
        state.input.pop();
        text.sections[1].value.pop();
    }
}

pub fn update_terminal(
    keys: Res<ButtonInput<KeyCode>>,
    mut state: ResMut<TerminalState>,
    mut query: Query<&mut Text>,
) {
    if keys.just_pressed(KeyCode::Enter) && !state.input.is_empty() {
        let cmd = state.input.trim().to_string();
        let mut text = query.single_mut();
        let response = if cmd == "nmap neotechlabs.com" {
            "> Scanning NeoTech Labs...\n> Port 80: HTTP (vulnerable)"
        } else if cmd == "ssh neotechlabs.com" {
            "> Connected—auth required"
        } else if cmd == "exploit" {
            "> Firewall breached"
        } else if cmd == "wget data" {
            "> 500MB downloaded—trace active!"
        } else if cmd == "cloak" {
            "> Trace evaded"
        } else if cmd == "exit" {
            std::process::exit(0);
        } else {
            &format!("> Unknown command: {}. Type 'help' for options.", cmd)
        };
        text.sections[0].value += &format!("{}\n", response);
        text.sections[1].value = "> ".to_string();
        state.input.clear();
    }
}

fn keycode_to_char(key_code: KeyCode) -> Option<char> {
    match key_code {
        KeyCode::KeyA => Some('a'),
        KeyCode::KeyB => Some('b'),
        KeyCode::KeyC => Some('c'),
        KeyCode::KeyD => Some('d'),
        KeyCode::KeyE => Some('e'),
        KeyCode::KeyF => Some('f'),
        KeyCode::KeyG => Some('g'),
        KeyCode::KeyH => Some('h'),
        KeyCode::KeyI => Some('i'),
        KeyCode::KeyJ => Some('j'),
        KeyCode::KeyK => Some('k'),
        KeyCode::KeyL => Some('l'),
        KeyCode::KeyM => Some('m'),
        KeyCode::KeyN => Some('n'),
        KeyCode::KeyO => Some('o'),
        KeyCode::KeyP => Some('p'),
        KeyCode::KeyQ => Some('q'),
        KeyCode::KeyR => Some('r'),
        KeyCode::KeyS => Some('s'),
        KeyCode::KeyT => Some('t'),
        KeyCode::KeyU => Some('u'),
        KeyCode::KeyV => Some('v'),
        KeyCode::KeyW => Some('w'),
        KeyCode::KeyX => Some('x'),
        KeyCode::KeyY => Some('y'),
        KeyCode::KeyZ => Some('z'),
        KeyCode::Digit0 => Some('0'),
        KeyCode::Digit1 => Some('1'),
        KeyCode::Digit2 => Some('2'),
        KeyCode::Digit3 => Some('3'),
        KeyCode::Digit4 => Some('4'),
        KeyCode::Digit5 => Some('5'),
        KeyCode::Digit6 => Some('6'),
        KeyCode::Digit7 => Some('7'),
        KeyCode::Digit8 => Some('8'),
        KeyCode::Digit9 => Some('9'),
        KeyCode::Space => Some(' '),
        KeyCode::Period => Some('.'),
        _ => None,
    }
}