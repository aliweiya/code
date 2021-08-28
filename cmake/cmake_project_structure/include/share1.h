#ifndef _SHARE1_H_
#define _SHARE1_H_

#ifdef _WIN32
int __declspec(dllexport) add(int a, int b);
int __declspec(dllexport) test(int a);
#else
int add(int a, int b);
int test(int a);
#endif

#endif  // _SHARE1_H_