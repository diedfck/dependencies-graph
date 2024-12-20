import json
import sys
from graphviz import Digraph

def load_package_lock(package_lock_path):
    try:
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл {package_lock_path} не найден.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: Неверный JSON в {package_lock_path}.")
        sys.exit(1)

def find_package(lock_data, package_name):
    packages = lock_data.get("packages", {})
    if package_name in packages:
        return packages[package_name]
    node_modules_path = f"node_modules/{package_name}"
    if node_modules_path in packages:
        return packages[node_modules_path]
    print(f"Ошибка: Пакет '{package_name}' не найден в package-lock.json.")
    sys.exit(1)

def build_dependency_graph(lock_data, package_name, output_path, depth_limit):
    package = find_package(lock_data, package_name)
    dependencies = package.get("dependencies", {})
    
    graph = Digraph(format='dot')
    graph.node(package_name, package_name)
    
    def add_dependencies(pkg_name, current_depth):
        if current_depth >= depth_limit:
            return
        pkg_data = find_package(lock_data, pkg_name)
        for dep, _ in pkg_data.get("dependencies", {}).items():
            graph.node(dep, dep)
            graph.edge(pkg_name, dep)
            add_dependencies(dep, current_depth + 1)
    
    add_dependencies(package_name, 0)
    graph.render(output_path, format="dot", cleanup=True)
    print(f"Граф зависимостей сохранен в {output_path}.dot")

def main():
    if len(sys.argv) != 5:
        print("Использование: python main.py <имя_пакета> <путь_к_package_lock> <путь_для_сохранения> <глубина>")
        sys.exit(1)
    
    package_name = sys.argv[1]
    package_lock_path = sys.argv[2]
    output_path = sys.argv[3]
    try:
        depth_limit = int(sys.argv[4])
    except ValueError:
        print("Ошибка: Глубина должна быть целым числом.")
        sys.exit(1)
    
    lock_data = load_package_lock(package_lock_path)
    build_dependency_graph(lock_data, package_name, output_path, depth_limit)

if __name__ == "__main__":
    main()
