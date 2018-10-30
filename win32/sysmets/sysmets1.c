/*----------------------------------------------------------------------------
SYSTEM1.c System Metrics Display Program
----------------------------------------------------------------------------*/
#include<windows.h>
#include "sysmets.h"

#define LOWORD(l) ((WORD)(l))
#define HIDOWD(l) ((WORD)(((DWORD)(1) >> 16) & 0xFFFF))

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    static TCHAR szAppName[] = TEXT("SysMets2");

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
        TEXT("Get System Metrics No. 2"),       // window caption
        WS_OVERLAPPEDWINDOW | WS_VSCROLL,       // window style 
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
    static int cxChar, cxCaps, cyChar, cyClient, iVscrollPos;
    HDC hdc;
    int i, y;
    PAINTSTRUCT ps;
    TCHAR szBuffer[10];
    TEXTMETRIC tm;

    switch (message) {
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

        // 设定滚动条范围
        SetScrollRange(hwnd, SB_VERT, 0, NUMLINES - 1, FALSE);
        SetScrollPos(hwnd, SB_VERT, iVscrollPos, TRUE);
        return 0;

    case WM_SIZE:
        cyClient = HIWORD(lParam);
        return 0;

    case WM_VSCROLL:
        switch(LOWORD(wParam)) {
        case SB_LINEUP:
            iVscrollPos -= 1;
            break;

        case SB_LINEDOWN:
            iVscrollPos += 1;
            break;

        case SB_PAGEUP:
            iVscrollPos -= cyClient / cyChar;
            break;
            
        case SB_PAGEDOWN:
            iVscrollPos += cyClient / cyChar;
            break;

        case SB_THUMBPOSITION:
            iVscrollPos = HIWORD(wParam);
            break;

        default:
            break;
        }

        iVscrollPos = max(0, min(iVscrollPos, NUMLINES - 1));
        if (iVscrollPos != GetScrollPos(hwnd, SB_VERT)) {
            SetScrollPos(hwnd, SB_VERT, iVscrollPos, TRUE);
            // 使客户区无效进行重绘
            InvalidateRect(hwnd, NULL, TRUE);
            // 立即更新无效区域
            UpdateWindow(hwnd);
        }

        return 0;

    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);

        for (i = 0; i < NUMLINES; i++) {
            // 当i小于iVscrollPos时，这个值是负的。程序实际上把这些行输出到客户区的外面。
            y = cyChar *(i - iVscrollPos);

            TextOut(hdc, 0, y, sysmetrics[i].szLabel, lstrlen(sysmetrics[i].szLabel));
            TextOut(hdc, 22 * cxCaps, y, sysmetrics[i].szDesc, lstrlen(sysmetrics[i].szDesc));
            SetTextAlign(hdc, TA_RIGHT | TA_TOP);
            TextOut(hdc, 22 * cxCaps + 40 * cxChar, y, szBuffer,
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