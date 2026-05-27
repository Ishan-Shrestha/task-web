# task-web

A small python web app for task manager using FLASK:

contains following routes:
- `load` at index/home
- `add` at \add, uses requests to access the html itself and concepts regarding that.
- `done` basically used to mark the done works, will remove and renumerate the index.
- `edit` redirct to another page to edit task  

Themed by using bootstrap
Implemented login system to personalize the task manager for individual users.

### Features:
- logging
- Task Manager with priority indicator
- Database using sqlite

### libararies used:
- flask
- logging
- os
- flask_sqlalchemy

### To use:
- Install dependencies:

```cli
    pip install -r requirements.txt
```