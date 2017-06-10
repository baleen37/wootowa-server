from importlib import import_module


def register_blueprints(app, files, blueprint_attribute):
    print(files)
    for file in files:
        m = import_module(file)

        if hasattr(m, blueprint_attribute):
            bp = getattr(m, blueprint_attribute)
            app.register_blueprint(bp)
