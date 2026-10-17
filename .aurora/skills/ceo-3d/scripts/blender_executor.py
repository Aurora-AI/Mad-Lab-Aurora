import os
import subprocess
import sys
import argparse

def run_blender_headless(blender_path: str, script_path: str, output_path: str):
    """
    Executa o Blender em modo background, rodando um script Python e 
    passando o argumento de output.
    """
    if not os.path.exists(script_path):
        print(f"Erro: Script {script_path} não encontrado.", file=sys.stderr)
        sys.exit(1)

    # Passamos argumentos para dentro do script do Blender usando '--' 
    command = [
        blender_path,
        "--background",
        "--python", script_path,
        "--",
        "--output", output_path
    ]

    print(f"Executando comando: {' '.join(command)}")
    
    try:
        # Captura stdout e stderr
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Blender executado com sucesso.")
        print("--- Blender Output ---")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erro durante a execução do Blender.", file=sys.stderr)
        print(f"Exit code: {e.returncode}", file=sys.stderr)
        print("--- Blender Error Output ---", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Erro: O binário do Blender não foi encontrado no path '{blender_path}'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper para execução de Blender Headless na Aurora")
    parser.add_argument("--script", required=True, help="Caminho para o script .py que o Blender vai rodar")
    parser.add_argument("--out", required=True, help="Caminho destino para o .glb")
    # Default 'blender' assume que está no PATH do SO, mas pode ser sobreposto.
    parser.add_argument("--bin", default="blender", help="Caminho absoluto para o binário do blender (caso não esteja no PATH)")

    args = parser.parse_args()

    # Cria o diretório de destino se não existir
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    run_blender_headless(args.bin, args.script, args.out)
