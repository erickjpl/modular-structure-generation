**UV**
***Para iniciar o sincronizar un proyecto***
```
uv sync
```
***Para activa el entorno virtual***
***Linux/macOS***
```
source .venv/bin/activate
```
***Windows (Command Prompt)***
```
.venv\Scripts\activate.bat
```
***Windows (PowerShell)***
```
.venv\Scripts\Activate.ps1
```

***Para iniciar un proyecto***
```
uv init
```
***Para instalar dependencias***
```
uv python install package
uv add package
```
***Para instalar dependencias de desarrollo***
```
uv add --dev package
```
***Para eliminar dependencias***
```
uv remove package
```
***Para ejecutar un script***
```
uv run hello.py
```
***Para ejecutar un modulo***
```
uv run python -m 
```

**Ruff**
***Para verificar***
```
ruff check
```
***Para correguir***
```
ruff check --fix
```
***Para formatear***
```
ruff format
```


**Ruff con UV**
```
uvx ruff check
uvx ruff check --fix
```