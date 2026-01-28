import json
import sys
import os


class BuildConfig:
    def __init__(self, config_file: str, config_name: str):
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        self.label: str | None = None
        self.language: str | None = None
        self.type: str | None = None
        self.command: str | None = None
        self.warnings_as_errors: bool | None = None
        self.cxx_standard: str | None = None
        self.architecture: str | None = None
        self.mode: str | None = None
        self.input_files: list[str] = []
        self.output_file: str | None = None
        self.output_directory: str | None = None
        self.dependencies: str | None = None

        for build in config_data["builds"]:
            if build["label"] == config_name:
                self.label = build["label"]
                self.language = build["language"]
                self.type = build["type"]
                self.command = build["command"]
                self.warnings_as_errors = build["WarningsAsErrors"] if "WarningsAsErrors" in build else False
                self.cxx_standard = build["cxx_standard"] if "cxx_standard" in build else None
                self.architecture = build["architecture"] if "architecture" in build else None
                self.mode = build["mode"] if "mode" in build else None
                self.output_directory = build["output_directory"] if "output_directory" in build else None
                self.output_file = f"{self.output_directory}\\{build["output_file"]}"
                self.input_files = build["input_files"]
                self.dependencies = build["dependencies"]

                break

        if not self.label:
            print(f"Build configuration '{config_name}' not found in {config_file}.")
            sys.exit(1)

    def Info(self):
        print(f"Build Configuration: {self.label}")
        print(f"Language: {self.language}")
        print(f"Command: {self.command}")
        print(f"Warnings as Errors: {self.warnings_as_errors}")
        print(f"C++ Standard: {self.cxx_standard}")
        print(f"Architecture: {self.architecture}")
        print(f"Mode: {self.mode}")
        print(f"Input Files: {self.input_files}")
        print(f"Output Directory: {self.output_directory}")
        print(f"Output File: {self.output_file}")

    def build(self):
        if self.language == "C++":
            self.BuildCpp()
        else:
            print(f"Unsupported language '{self.language}' for building. Use 'C++'.")
            sys.exit(1)

    def BuildCpp(self):
        if self.type == "exe":
            self.BuildCppExe()
        elif self.type == "dll":
            self.BuildCppDll()

    def BuildCppExe(self):
        if self.command and self.cxx_standard and self.architecture and self.mode and self.input_files and self.output_file:
            final_command: str = self.command + f" -std={self.cxx_standard}"
            if self.warnings_as_errors:
                final_command += " -Werror"
            
            if self.architecture == "x64":
                final_command += " -m64"
            elif self.architecture == "x86":
                final_command += " -m32"
            
            if self.mode == "release":
                final_command += " -O2"
            elif self.mode == "debug":
                final_command += " -g"
            
            input_files_str = ' '.join(self.input_files)
            final_command += f" {input_files_str} -o {self.output_file}"

            print(f"Executing build command: {final_command}")
            os.system(final_command)

    def BuildCppDll(self):
        pass