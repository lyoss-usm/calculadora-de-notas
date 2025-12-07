"""
Entry point for the Flask Application.
Executes the application factory and starts the server.
"""
import os
import sys
from app import create_app

# Detectamos el entorno (default: 'development')
env = os.getenv('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    try:
        # Configuración de red
        host = '0.0.0.0'
        port = int(os.environ.get('PORT', 5000))
        pid = os.getpid()

        # Logs técnicos de inicio
        print("-" * 60)
        print(f"Server Process ID (PID): {pid}")
        print(f"Environment: {env.upper()}")
        print(f"Debug Mode:  {'ENABLED' if app.debug else 'DISABLED'}")
        print("-" * 60)
        print(f" * Serving Flask app '{app.name}'")
        print(f" * Access URL: http://127.0.0.1:{port}")
        print("-" * 60)

        # Iniciar servidor
        app.run(host=host, port=port)

    except OSError as e:
        print(f"\n[ERROR] Port {port} is likely in use or requires permissions.")
        print(f"System message: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user request (SIGINT).")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n[CRITICAL] Unexpected error during startup: {e}")
        sys.exit(1)