{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/tags/23.11.tar.gz") {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python39
    python39Packages.pip
    python39Packages.virtualenv
    postgresql_15
    gcc
  ];

  shellHook = ''
    export PYTHONPATH="${pkgs.python39}/lib/python3.9/site-packages:$PYTHONPATH"
    export LD_LIBRARY_PATH="${pkgs.postgresql_15}/lib:$LD_LIBRARY_PATH"
  '';
} 