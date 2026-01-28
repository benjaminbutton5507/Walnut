import json
import sys
import os

from .build import BuildConfig


class RunConfig:
    def __init__(self, config_file: str, config_name: str):
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        self.label: str | None = None
        self.language: str | None = None
        self.executable: str | None = None
        self.arguments: list[str] = []
        self.dependencies: list[str] = []

        for run in config_data["runs"]:
            if run["label"] == config_name:
                self.label = run["label"]
                self.language = run["language"]
                self.executable = run['executable']
                self.arguments = run["arguments"]
                self.dependencies = run["dependencies"] if "dependencies" in run else []
                break

        if not self.label:
            print(f"Run configuration '{config_name}' not found in {config_file}.")
            sys.exit(1)

    def Info(self):
        print(f"Run Configuration: {self.label}")
        print(f"Language: {self.language}")
        print(f"Input File: {self.executable}")
        print(f"Arguments: {self.arguments}")
        print(f"Dependencies: {self.dependencies}")

    def run(self):
        if self.language == "C++":
            self.RunCpp()
        elif self.language == "Python":
            self.RunPython()
        else:
            print(f"Unsupported language '{self.language}' for running. Use 'C++' or 'Python'.")
            sys.exit(1)

    def RunCpp(self):
        if self.executable:
            if self.dependencies:
                for dep in self.dependencies:
                    b = BuildConfig(".build_config/config.json", dep)
                    b.build()
            args_str = ' '.join(self.arguments)
            command = f"{self.executable} {args_str}"
            print(f"Executing run command: {command}")
            print("============================================================")
            os.chdir("Walnut/build")
            os.system(command)
            os.chdir("../..")

    def RunPython(self):
        if self.executable:
            args_str = ' '.join(self.arguments)
            command = f"python {self.executable} {args_str}"
            print(f"Executing run command: {command}")
            print("============================================================")
            os.system(command)