#!/usr/bin/env python3
"""
🚀 HobbyX Launcher
Запускает бэкенд и открывает Swagger в браузере
"""
import subprocess
import sys
import webbrowser
import time
import os

def main():
    print("🔧 HobbyX — запуск...")
    
    # Определяем корень проекта
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Проверяем, есть ли docker-compose.yml в родительской папке
    compose_file = os.path.join(os.path.dirname(project_root), "docker-compose.yml")
    
    if os.path.exists(compose_file):
        print("🐳 Запускаем через Docker Compose...")
        os.chdir(os.path.dirname(project_root))
        
        # Собираем и запускаем контейнеры
        subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)
        
        # Ждём, пока поднимется сервис
        print("⏳ Ждём запуска сервисов (~15 сек)...")
        time.sleep(15)
        
        # Открываем Swagger
        swagger_url = "http://localhost:8000/docs"
        print(f"✅ Готово! Открываю: {swagger_url}")
        webbrowser.open(swagger_url)
        
        print("📋 Логи: `docker compose logs -f web`")
        print("🛑 Остановить: `docker compose down`")
        
    else:
        print("🐍 Запускаем локально (uvicorn)...")
        os.chdir(project_root)
        
        # Загружаем .env
        from dotenv import load_dotenv
        load_dotenv()
        
        # Запускаем uvicorn
        proc = subprocess.Popen(
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            cwd=project_root
        )
        
        time.sleep(3)
        swagger_url = "http://localhost:8000/docs"
        print(f"✅ Готово! Открываю: {swagger_url}")
        webbrowser.open(swagger_url)
        
        print("🛑 Остановить: Ctrl+C")
        proc.wait()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Завершено.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)