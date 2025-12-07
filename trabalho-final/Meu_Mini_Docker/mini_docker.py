import os
import shutil
import time

BASE_PATH = "containers"

# ------------------------------
# 1. Criar container (pasta isolada)
# ------------------------------
def create_container(name):
    path = f"{BASE_PATH}/{name}/filesystem"
    os.makedirs(path, exist_ok=True)
    print(f"[OK] Container '{name}' criado em {path}")
    return path

# ------------------------------
# 2. Criar arquivo dentro de um container
# ------------------------------
def create_file(container, filename, content):
    filepath = f"{BASE_PATH}/{container}/filesystem/{filename}"
    with open(filepath, "w") as f:
        f.write(content)
    print(f"[OK] Arquivo '{filename}' criado no container '{container}'")

# ------------------------------
# 3. Copiar arquivo entre containers (operação lenta)
# ------------------------------
def copy_file(src_container, dst_container, filename):
    src = f"{BASE_PATH}/{src_container}/filesystem/{filename}"
    dst = f"{BASE_PATH}/{dst_container}/filesystem/{filename}"
    
    start = time.time()
    shutil.copy(src, dst)
    end = time.time()

    tempo = end - start
    print(f"[COPY] Copiado '{filename}' de {src_container} para {dst_container} em {tempo:.6f}s")
    return tempo

# ------------------------------
# 4. Criar hardlink entre containers (operação rápida - Windows)
# ------------------------------
def create_symlink(src_container, dst_container, filename):
    src = f"{BASE_PATH}/{src_container}/filesystem/{filename}"
    dst = f"{BASE_PATH}/{dst_container}/filesystem/{filename}"

    start = time.time()
    os.link(src, dst)  # Hardlink no Windows funciona sem admin
    end = time.time()

    tempo = end - start
    print(f"[LINK] Hardlink '{filename}' criado em {dst_container} apontando para {src_container} em {tempo:.6f}s")
    return tempo

# ------------------------------
# 5. Demonstração completa
# ------------------------------
def run_demo():
    print("\n=== INICIANDO DEMONSTRAÇÃO ===\n")

    # Criar containers
    create_container("c1")
    create_container("c2")

    # Criar arquivo base
    create_file("c1", "teste.txt", "Conteúdo do arquivo de teste.")

    # Operação 1: Cópia
    tempo_copia = copy_file("c1", "c2", "teste.txt")

    create_file("c1", "teste_link.txt", "Arquivo para demonstrar hardlink.")

    tempo_link = create_symlink("c1", "c2", "teste_link.txt")

    print("\n=== RESULTADOS ===")
    print(f"Tempo de cópia: {tempo_copia:.6f}s")
    print(f"Tempo de hardlink: {tempo_link:.6f}s")
    print("\nConclusão: hardlink é MUITO mais rápido que copiar um arquivo.\n")
    print(f"Tempo de hardlink: {tempo_link:.6f}s")
    print("\nConclusão: hardlink é MUITO mais rápido que copiar um arquivo.\n")


if __name__ == "__main__":
    run_demo()