{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python39
    python39Packages.pip
    python39Packages.virtualenv
    postgresql_16
    postgresql_16.lib
    gcc
    gcc-unwrapped
    gcc-unwrapped.lib
  ];

  shellHook = ''
    export PYTHONPATH="${pkgs.python39}/lib/python3.9/site-packages:$PYTHONPATH"
    export LD_LIBRARY_PATH="${pkgs.postgresql_16}/lib:${pkgs.gcc-unwrapped.lib}/lib:$LD_LIBRARY_PATH"
    export PATH="${pkgs.postgresql_16}/bin:$PATH"
  '';
} 