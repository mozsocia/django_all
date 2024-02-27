
put this file on `.vscode/tasks.json`
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Django Server on Startup",
      "type": "shell",
      "command": "python",
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
        "runOn": "folderOpen"
      }
    }
  ]
}
```
### for windows
```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
      {
        "label": "echo",
        "type": "shell",
        "command": "echo Hello"
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
        }
      }
    ]
}
```

### for linux
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Django Server on Startup",
      "type": "shell",
      "command": "${workspaceFolder}/.venv/bin/python",  
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
        "runOn": "folderOpen"
      }
    }
  ]
}
```
