# {{ project_name }}

###***Iniciar proyecto***
```
uv sync
```

###***Variables de entorno***
```
cp .env.template .env
```

###***Activa el entorno virtual***
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

###***Para verificar y formatear el codigo***
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