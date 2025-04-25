# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).

{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # Bootloader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  nix = {
   settings = {
     experimental-features = [ "nix-command" "flakes" ];
   };
  };
  networking.hostName = "nixos"; # Define your hostname.
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Enable networking
  networking.networkmanager.enable = true;

  # Set your time zone.
  time.timeZone = "Africa/Nairobi";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";

  # Enable the X11 windowing system.
  services.xserver.enable = true;
  
  # enable redis service
  services.redis.servers."".enable = true; 
 
  # Enable fingerprint services on the nixos
  # services.fprintd.enable = true;
  
  # Enable AppImage usage in my nixos 
  # programs.appimage.enable = true;
  # programs.appimage.binfmt = true;
  # pluggable authentication services
  # security.pam.services.sudo.fprintAuth = true;
  # security.pam.services.login.fprintAuth = true;
  # security.pam.services.lightdm.fprintAuth = true; # For Deepin (LightDM) if gnome then gdm

  # Enable the Deepin Desktop Environment.
  services.xserver.displayManager.lightdm.enable = true;
  services.xserver.desktopManager.deepin.enable = true;

  # Configure keymap in X11
  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };
  
  # Enable CUPS to print documents.
  services.printing.enable = true;

  # Enable sound with pipewire.
  hardware.pulseaudio.enable = false;
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    # If you want to use JACK applications, uncomment this
    #jack.enable = true;

    # use the example session manager (no others are packaged yet so this is enabled by default,
    # no need to redefine it in your config for now)
    #media-session.enable = true;
  };

  # Enable touchpad support (enabled default in most desktopManager).
  # services.xserver.libinput.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.trent = {
    isNormalUser = true;
    description = "trent";
    extraGroups = [ "networkmanager" "wheel" ];
    packages = with pkgs; [
    # thunderbird
    ];
  };

  # Install firefox.
  programs.firefox.enable = true;
  
  # docker installation
  virtualisation.docker.enable = true;


  # Enable libvirtd for virtualization
  # virtualisation.libvirtd.enable = true;
  # Optional: Enable SPICE for better VM display performance
  virtualisation.spiceUSBRedirection.enable = true;

  # List packages installed in system profile. To search, run:
  #  $ nix search wget;
  environment.systemPackages = with pkgs; [
    vim # Do not forget to add an editor to edit configuration.nix! The Nano editor is also installed by default.
    wget
    #   waydroid
    # lxc
    #    vscode
    python3
    # weston  
    # fingerprint utilities
    # fprintd
    # libfprint
    
    # installing gnome boxed and related dependencies
    # gnome-boxes
    # libvirt
    # virt-manager
  
    # for containerizing the waydroid container
    # cage  
    # python utilities
    python3Packages.pip
    python3Packages.virtualenv
    python3Packages.textual  # Add this
    nodejs_20
    pnpm
    (python3.withPackages (ps: with ps; [ textual ]))

    # rust packages
    rustc      # Rust compiler
    cargo      # Rust package manager
    rustfmt    # Rust formatter
    pkg-config  # rust audio dependencies
    alsa-lib    #rust audio dependencies
  ];

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };
  # virtualisation.waydroid.enable = true;
  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  # services.openssh.enable = true;

  # Open ports in the firewall.
  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  # Or disable the firewall altogether.
  # networking.firewall.enable = false;
  
  # virtualization technology for wayload
  # virtualisation.lxc.enable = true;
  # hardware.graphics.enable = true;

  boot.kernelParams = [ "fbcon=map:10" ];
  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It‘s perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  # Before changing this value read the documentation for this option
  # (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
  system.stateVersion = "24.11"; # Did you read the comment?

}
