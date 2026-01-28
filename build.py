import sys
import os


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


CXX = "g++"
CXX_VERSION = "-std=c++23"
CXX_FLAGS = "-O2 -Wall -Wextra"
CXX_m64 = "-m64"
CXX_m32 = "-m32"

DLL_LIB_FLAG = "-shared -o"
LIB_FLAG = "-Wl,--out-implib"

FINAL_DLL = "build/release_x64_walnut.dll"
FINAL_LIB = "build/release_x64_walnut.lib"

FINAL_TEST_EXE = "build/release_x64_main.exe"

def build_dll():
    if mode2 == "release":
        os.chdir(f"v{version}")
        compile_command = f'{CXX} {CXX_VERSION} {CXX_FLAGS} {DLL_LIB_FLAG} {FINAL_DLL} src/test/math.cpp'
        print(compile_command)
        os.system(compile_command)
        compile_command = f'{CXX} {CXX_VERSION} {CXX_FLAGS} {DLL_LIB_FLAG} {FINAL_DLL} src/test/math.cpp {LIB_FLAG},{FINAL_LIB}'
        print(compile_command)
        os.system(compile_command)
        os.chdir("..")

def run():
    if mode2 == "release":
        os.chdir(f"v{version}/build")
        os.system(f'release_x64_main.exe')
        os.chdir("../..")


def build():
    if mode2 == "release":
        build_dll()
        os.chdir(f"v{version}/src")
        compile_command = f'{CXX} {CXX_VERSION} {CXX_FLAGS} main.cpp ../{FINAL_DLL} -o ../{FINAL_TEST_EXE}'
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