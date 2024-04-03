import os
import sys

project_path = "/Users/griffinbaker/projects/python-mastery"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

print(project_path)
os.environ["PROJECT_DATA_DIR"] = os.path.join(project_path, "Data")
