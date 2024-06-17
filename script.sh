#!/bin/bash

# Colors
RED='\033[1;31m'   # Rojo brillante
GREEN='\033[1;32m' # Verde brillante
NO_COLOR='\033[0m' # Sin color, para restablecer al color por defecto

print_ascii_skull() {
    echo -e "${GREEN}"
    cat << "EOF"
  ____               _                                   _                  _           ____    _       _         _       _                 
 |  _ \    ___    __| |   __ _    __ _    ___     __ _  (_)   ___    __ _  | |         |  _ \  | |__   (_)  ___  | |__   (_)  _ __     __ _ 
 | |_) |  / _ \  / _` |  / _` |  / _` |  / _ \   / _` | | |  / __|  / _` | | |  _____  | |_) | | '_ \  | | / __| | '_ \  | | | '_ \   / _` |
 |  __/  |  __/ | (_| | | (_| | | (_| | | (_) | | (_| | | | | (__  | (_| | | | |_____| |  __/  | | | | | | \__ \ | | | | | | | | | | | (_| |
 |_|      \___|  \__,_|  \__,_|  \__, |  \___/   \__, | |_|  \___|  \__,_| |_|         |_|     |_| |_| |_| |___/ |_| |_| |_| |_| |_|  \__, |
                                 |___/           |___/                                                                                |___/ 
EOF
    echo -e "${NO_COLOR}"
}

print_ascii_skull

# Ruta al entorno virtual
VENV_DIR="venv"

# Activar el entorno virtual
source "$VENV_DIR/bin/activate"

# Ruta al intérprete de Python (ya no necesario porque se usa el de venv)
PYTHON_SCRIPT="main.py"

# Parámetros por defecto
PARAMS=""

# Procesar opciones y argumentos
while (( "$#" )); do
  case "$1" in
    -a|--argumento1)
      ARGUMENTO1=$2
      shift 2
      ;;
    -b|--argumento2)
      ARGUMENTO2=$2
      shift 2
      ;;
    *)
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

# Ejecutar el script Python con los argumentos
python "$PYTHON_SCRIPT" $ARGUMENTO1 $ARGUMENTO2 $PARAMS

# Desactivar el entorno virtual
deactivate
