{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python39
    python39Packages.pip
    python39Packages.virtualenv
    postgresql_16
    gcc
  ];

  shellHook = ''
    export PYTHONPATH="${pkgs.python39}/lib/python3.9/site-packages:$PYTHONPATH"
    export LD_LIBRARY_PATH="${pkgs.postgresql_16}/lib:$LD_LIBRARY_PATH"
  '';
} 