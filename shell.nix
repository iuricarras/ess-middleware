let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.requests
      python-pkgs.flask
      python-pkgs.flask-cors
      python-pkgs.proxmoxer
      python-pkgs.pyopenssl
      python-pkgs.flask-login
      
      python-pkgs.flask-sqlalchemy
      python-pkgs.python-dotenv
      python-pkgs.python-socketio
      python-pkgs.websocket-client
    ]))
    pkgs.openssl
    pkgs.certbot
  ];
}

