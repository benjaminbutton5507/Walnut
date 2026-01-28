import sys
import os


CXX = "g++"
CXX_VERSION = "-std=c++23"
CXX_FLAGS = "-O2 -Wall -Wextra"

if sys.platform != "win32":
    print("This build script currently supports only Windows.")
    sys.exit(1)

if len(sys.argv) > 3:
    mode1 = sys.argv[1]
    mode2 = sys.argv[2]
    version = sys.argv[3]
else:
    print("Insufficient arguments provided. Usage: python build.py <mode1> <mode2> <version>")
    sys.exit(1)


def run():
    if mode2 == "release":
        os.chdir(f"v{version}/build")
        os.system(f'release_main.exe')
        os.chdir("../..")
    else:
        print("Usage: python build.py <mode1> <mode2> <version>")
        print(f"Unknown mode2: {mode2}. Use 'release'.")
        sys.exit(1)


def build():
    if mode2 == "release":
        os.chdir(f"v{version}/src")
        compile_command = f'{CXX} {CXX_VERSION} {CXX_FLAGS} main.cpp -o ../build/release_main.exe'
        print(compile_command)
        os.system(compile_command)
        os.chdir("../..")
    else:
        print("Usage: python build.py <mode1> <mode2> <version>")
        print(f"Unknown mode2: {mode2}. Use 'release'.")
        sys.exit(1)


def main():
    if mode1 == "run":
        run()
    elif mode1 == "build":
        build()
    elif mode1 == "all":
        build()
        print("Build complete. Running the application...")
        print("==============================================================")
        run()
    else:
        print("Usage: python build.py <mode1> <mode2> <version>")
        print(f"Unknown mode1: {mode1}. Use 'run', 'build', or 'all'.")
        sys.exit(1)

        

if __name__ == "__main__":
    main()
    sys.exit(0)