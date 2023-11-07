# ruff: noqa
import black


def hello_world_main_template(app_name: str) -> str:
    template = f"""\"\"\"Generated by BuildFlow.\"\"\"
from buildflow import Flow

from {app_name}.processors.service import service


app = Flow()
app.add_service(service)
"""
    return template


def hello_world_service_template(app_name: str) -> str:
    template = f"""from buildflow import Service

from {app_name}.processors.hello_world import hello_world_endpoint

service = Service(service_id="hello-world-service")
service.add_endpoint(hello_world_endpoint)
"""
    return template


def hello_world_endpoint_template() -> str:
    template = """from buildflow import endpoint

@endpoint("/", method="GET")
def hello_world_endpoint() -> str:
    return "Hello World!"
"""
    return template


def hello_world_readme_template(app_name: str, app_dir: str) -> str:
    template = f"""\
# {app_name}

Welcome to BuildFlow!

If you want to just get started quickly you can run start your app with:

```
buildflow run
```

Then you can visit http://localhost:8000 to see your app running.

## Directory Structure

At the root level there are three important files:

- `buildflow.yml` - This is the main configuration file for your app. It contains all the information about your app and how it should be built.
- `main.py` - This is the entry point to your app and where your `Flow` is initialized.
- `requirements.txt` - This is where you can specify any Python dependencies your app has.

Below the root level we have:

**{app_dir}**

This is the directory where your app code lives. You can put any files you want in here and they will be available to your app. We create a couple directories and files for you:

- **processors**: This is where you can put any custom processors you want to use in your app. In here you will see we have defined a *service.py* for a service in your app and a *hello_world.py* file for a custom endpoint processor.
- **primitives.py**: This is where you can define any custom primitive resources that your app will need. Note it is empty right now since your initial app is so simple.

**.buildflow**

This is a hidden directory that contains all the build artifacts for your app. You can general ignore this directory and it will be automatically generated for you. If you are using github you probably want to put this in your *.gitignore* file.
"""
    return template
