{
  description = "Bitebook project with Python, Flask, and Google Cloud Storage";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }: 
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        zsh = pkgs.zsh;
        tailwindcss = pkgs.tailwindcss;
        flyctl = pkgs.flyctl;
        pythonEnv = pkgs.python310.withPackages (ps: with ps; [
          flask
          flask-jwt-extended
          google-cloud-storage
          python-dotenv
          google-api-python-client
          google-auth-httplib2
          google-auth-oauthlib
          openai
          gunicorn
          # Add any other Python dependencies here
        ]);
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [ pythonEnv tailwindcss flyctl zsh ];
          SHELL = "${pkgs.zsh}/bin/zsh";
          shellHook = ''
            export FLASK_APP=app.py
            export FLASK_ENV=development
            if [ -z "$IN_NIX_SHELL_ZSH_STARTED" ]; then
              export IN_NIX_SHELL_ZSH_STARTED=1
              exec $SHELL
            fi
          '';
        };
      }
    );
}

