#pragma once

#ifdef _WIN32
    #ifdef WALNUT_BUILD_DLL
        #define WALNUT_API __declspec(dllexport)
    #else
        #define WALNUT_API __declspec(dllimport)
    #endif
#else
    #error Walnut only supports Windows.
#endif