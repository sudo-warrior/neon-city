{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.alsa-lib
    pkgs.systemd.dev  # For udev headers
    pkgs.pkg-config
    pkgs.xorg.libX11
    pkgs.udev
    pkgs.openssl      # Often needed by network/TLS crates
    pkgs.xorg.libXcursor
    pkgs.xorg.libXrandr
    pkgs.xorg.libXi
    pkgs.libxkbcommon # Provides libxkbcommon-x11.so
    pkgs.vulkan-loader # For Vulkan graphics API
    pkgs.wayland       # For Wayland display server support
  ];

  # Point pkg-config to both ALSA and systemd/udev
  PKG_CONFIG_PATH = with pkgs; [
    "${alsa-lib}/lib/pkgconfig"
    "${systemd.dev}/lib/pkgconfig"  # For libudev.pc
  ] ++ (lib.optional (systemd ? pkgconfigPrefix) systemd.pkgconfigPrefix);

  # Set LD_LIBRARY_PATH for runtime linking
  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.xorg.libX11
      pkgs.xorg.libXcursor
      pkgs.xorg.libXrandr
      pkgs.xorg.libXi
      pkgs.libxkbcommon
      pkgs.vulkan-loader
      pkgs.wayland
      pkgs.alsa-lib
    ]}:$LD_LIBRARY_PATH
  '';
}