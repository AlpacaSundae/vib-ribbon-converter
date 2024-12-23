# flake.nix

{
  description = "converts audio files and creates a .cue for importing into vib-ribbon";

  outputs = { self, nixpkgs, ... }: {
    devShell.x86_64-linux = let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      
      # Use Python 3.13 explicitly
      pythonEnv = pkgs.python313.withPackages (ps: with ps; [
        ffmpeg-python
      ]);

    in pkgs.mkShell {
      buildInputs = [ pythonEnv ];
      
      #shellHook = ''
      #  echo ""
      #'';
    };
  };
}

