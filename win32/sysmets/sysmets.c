/*----------------------------------------------------------------------------
    SYSTEM.c System Metrics Display Program
----------------------------------------------------------------------------*/
#include<windows.h>
#include "sysmets.h"

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    static TCHAR szAppName[] = TEXT("SysMets1");

    HWND        hwnd;
    MSG         msg;
    WNDCLASS    wndclass;

    wndclass.style = CS_HREDRAW | CS_VREDRAW;
    wndclass.lpfnWndProc = WndProc;
    wndclass.cbClsExtra = 0;
    wndclass.cbWndExtra = 0;
    wndclass.hInstance = hInstance;
    wndclass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);
    wndclass.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
    wndclass.lpszMenuName = NULL;
    wndclass.lpszClassName = szAppName;

    if (!RegisterClass(&wndclass)) {
        MessageBox(NULL, TEXT("This program requires Windows NT!"), szAppName, MB_ICONERROR);
        return 0;
    }

    hwnd = CreateWindow(szAppName,              // window class name
        TEXT("Get System Metrics No. 1"),       // window caption
        WS_OVERLAPPEDWINDOW,                    // window style 
        CW_USEDEFAULT,                          // initial x position
        CW_USEDEFAULT,                          // initial x position
        CW_USEDEFAULT,                          // initial x size
        CW_USEDEFAULT,                          // initial y size
        NULL,                                   // parent window handle
        NULL,                                   // window menu handle
        hInstance,                              // program instance handle
        NULL);                                  // creation parameters

    ShowWindow(hwnd, iCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    static int cxChar, cxCaps, cyChar;
    HDC hdc;
    int i;
    PAINTSTRUCT ps;
    TCHAR szBuffer[10];
    TEXTMETRIC tm;

    switch(message){
    case WM_CREATE:
        hdc = GetDC(hwnd);

        GetTextMetrics(hdc, &tm);
        cxChar = tm.tmAveCharWidth;
        // 将大写字符得平均宽度保存在静态变量中。
        // tmPitchAndFamily字段是否为等宽字体，1是变宽字体，0是等宽字体
        // 变宽字体中cxCaps设为cxChar的1.5倍
        cxCaps = (tm.tmPitchAndFamily & 1 ? 3 : 2)*cxChar / 2;
        cyChar = tm.tmHeight + tm.tmExternalLeading;
        ReleaseDC(hwnd, hdc);
        return 0;

    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);

        for (i = 0; i < NUMLINES; i++) {
            // 0表示从最左端输出
            TextOut(hdc, 0, cyChar*i, sysmetrics[i].szLabel, lstrlen(sysmetrics[i].szLabel));
            TextOut(hdc, 22 * cxCaps, cyChar*i, sysmetrics[i].szDesc, lstrlen(sysmetrics[i].szDesc));
            SetTextAlign(hdc, TA_RIGHT | TA_TOP);
            TextOut(hdc, 22 * cxCaps + 40 * cxChar, cyChar*i, szBuffer,
                wsprintf(szBuffer, TEXT("%5d"), GetSystemMetrics(sysmetrics[i].iIndex)));
            SetTextAlign(hdc, TA_LEFT | TA_TOP);
        }
        EndPaint(hwnd, &ps);
        return 0;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, message, wParam, lParam);
}