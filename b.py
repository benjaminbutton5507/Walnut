import sys

from build_package import BuildConfig, RunConfig

if sys.platform != "win32":
    print("This build script is intended to be run on Windows.")
    sys.exit(1)

if len(sys.argv) > 2:
    MODE = sys.argv[1]
    CONFIG = sys.argv[2]

else:
    print("Insufficient arguments provided. Usage: python build.py <mode> <config>")
    sys.exit(1)


def main():
    config_file = ".build_config/config.json"

    if MODE == "build":
        build_config = BuildConfig(config_file, CONFIG)
        build_config.Info()
        build_config.build()
    elif MODE == "run":
        run_config = RunConfig(config_file, CONFIG)
        run_config.Info()
        run_config.run()
    else:
        print(f"Unknown mode '{MODE}'. Use 'build' or 'run'.")
        sys.exit(1)


if __name__ == "__main__":
    main()