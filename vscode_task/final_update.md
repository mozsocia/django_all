
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Create Virtual Environment",
      "type": "shell",
      "command": "python",
      "args": [
        "-m",
        "venv",
        ".venv"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "runOptions": {
        "runOn": "default"
      }
    },
    {
      "label": "Install Dependencies",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/Scripts/python",
      "args": [
        "-m",
        "pip",
        "install",
        "-r",
        "requirements.txt"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "dependsOn": "Create Virtual Environment",
      "runOptions": {
        "runOn": "default"
      }
    },
    {
      "label": "Prepare Environment and migrate",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/Scripts/python",
      "args": [
        "${workspaceFolder}/manage.py",
        "refresh_and_seed"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "dependsOn": "Install Dependencies",
      "runOptions": {
        "runOn": "default"
      }
    },
    {
      "label": "Run Django Server on Startup",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/Scripts/python",
      "args": [
        "${workspaceFolder}/manage.py",
        "runserver",
        "9000"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "runOptions": {
        "runOn": "default"
      },
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": true
      },
    }
  ]
}
```

