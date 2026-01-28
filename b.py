import sys
import os
import json

if sys.platform != "win32":
    print("This build script is intended to be run on Windows.")
    sys.exit(1)

if len(sys.argv) > 1:
    CONFIG = sys.argv[1]

else:
    print("Insufficient arguments provided. Usage: python build.py <config>")
    sys.exit(1)


class BuildConfig:
    def __init__(self, config_file: str, config_name: str):
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        self.label: str | None = None
        self.command: str | None = None
        self.warnings_as_errors: bool | None = None
        self.cxx_standard: str | None = None
        self.architecture: str | None = None
        self.mode: str | None = None
        self.input_files: list[str] = []
        self.output_file: str | None = None

        for build in config_data["builds"]:
            if build["label"] == config_name:
                self.label = build["label"]
                self.command = build["command"]
                self.warnings_as_errors = build["WarningsAsErrors"]
                self.cxx_standard = build["cxx_standard"]
                self.architecture = build["architecture"]
                self.mode = build["mode"]
                self.output_file = f"Walnut/{build["output_file"]}"

                for file in build["input_files"]:
                    self.input_files.append(f"Walnut/{file}")

                break

        if not self.label:
            print(f"Build configuration '{config_name}' not found in {config_file}.")
            sys.exit(1)

    def Info(self):
        print(f"Build Configuration: {self.label}")
        print(f"Command: {self.command}")
        print(f"Warnings as Errors: {self.warnings_as_errors}")
        print(f"C++ Standard: {self.cxx_standard}")
        print(f"Architecture: {self.architecture}")
        print(f"Mode: {self.mode}")
        print(f"Input Files: {self.input_files}")
        print(f"Output File: {self.output_file}")

    def build(self):
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



build_config = BuildConfig(".build_config/config.json", CONFIG)
build_config.Info()
build_config.build()