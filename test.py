import unittest
import subprocess
import os
import json

class TestDependencyGraphBuilder(unittest.TestCase):

    def setUp(self):
        # Создаем временные файлы для тестирования
        self.package_lock_path = 'test_package_lock.json'
        self.output_path = 'test_output'
        self.package_name = 'test-package'
        
        # Пример данных для package-lock.json
        self.package_lock_data = {
            "name": "test-package",
            "version": "1.0.0",
            "dependencies": {
                "dep-a": {
                    "version": "1.0.0",
                    "resolved": "https://example.com/dep-a",
                    "dependencies": {
                        "dep-b": {
                            "version": "1.0.0",
                            "resolved": "https://example.com/dep-b",
                            "dependencies": {}
                        }
                    }
                }
            }
        }
        
        # Записываем test_package_lock.json
        with open(self.package_lock_path, 'w', encoding='utf-8') as f:
            json.dump(self.package_lock_data, f, indent=2)

    def tearDown(self):
        # Удаляем временные файлы
        if os.path.exists(self.package_lock_path):
            os.remove(self.package_lock_path)
        if os.path.exists(self.output_path + '.dot'):
            os.remove(self.output_path + '.dot')
        if os.path.exists(self.output_path + '.pdf'):
            os.remove(self.output_path + '.pdf')

    def test_invalid_json(self):
        # Создадим неверный JSON файл для проверки
        with open(self.package_lock_path, 'w', encoding='utf-8') as f:
            f.write("{invalid-json}")
        
        result = subprocess.run([
            'python', 'main.py', self.package_name, self.package_lock_path, self.output_path, '2'
        ], capture_output=True, text=True)
        self.assertIn("Ошибка: Неверный JSON в test_package_lock.json.", result.stdout)

    def test_package_not_found(self):
        result = subprocess.run([
            'python', 'main.py', 'nonexistent-package', self.package_lock_path, self.output_path, '2'
        ], capture_output=True, text=True)
        self.assertIn("Ошибка: Пакет 'nonexistent-package' не найден в package-lock.json.", result.stdout)

    def test_depth_is_not_integer(self):
        result = subprocess.run([
            'python', 'main.py', self.package_name, self.package_lock_path, self.output_path, 'two'
        ], capture_output=True, text=True)
        self.assertIn("Ошибка: Глубина должна быть целым числом.", result.stdout)

    def test_invalid_argument_count(self):
        result = subprocess.run([
            'python', 'main.py', self.package_name, self.package_lock_path, self.output_path
        ], capture_output=True, text=True)
        self.assertIn("Использование: python main.py <имя_пакета> <путь_к_package_lock> <путь_для_сохранения> <глубина>", result.stdout)

if __name__ == '__main__':
    unittest.main()
