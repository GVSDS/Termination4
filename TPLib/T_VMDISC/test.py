import json

class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Version):
            return {
                "__type__": "Version",
                "major": obj.major,
                "minor": obj.minor,
                "patch": obj.patch
            }
        return super().default(obj)

data = {"Version": Version(1, 0, 999)}
json_str = json.dumps(data, cls=CustomEncoder, indent=2)
print(json_str)