
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
