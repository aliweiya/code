/*----------------------------------------------------------------------------
SYSTEM2.c System Metrics Display Program No. 2
----------------------------------------------------------------------------*/
#include<windows.h>
#include "sysmets.h"

#define LOWORD(l) ((WORD)(l))
#define HIDOWD(l) ((WORD)(((DWORD)(1) >> 16) & 0xFFFF))

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    static TCHAR szAppName[] = TEXT("SysMets3");

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

    hwnd = CreateWindow(szAppName,                      // window class name
        TEXT("Get System Metrics No. 2"),               // window caption
        WS_OVERLAPPEDWINDOW | WS_VSCROLL | WS_HSCROLL,  // window style 
        CW_USEDEFAULT,                                  // initial x position
        CW_USEDEFAULT,                                  // initial x position
        CW_USEDEFAULT,                                  // initial x size
        CW_USEDEFAULT,                                  // initial y size
        NULL,                                           // parent window handle
        NULL,                                           // window menu handle
        hInstance,                                      // program instance handle
        NULL);                                          // creation parameters

    ShowWindow(hwnd, iCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    /* 
    typedef struct tagScrollINFO{
        UINT cbSize;    // sizeof(SCROLLINFO)
        UINT fMask;     // 要设置或获取的值
        int nMin;       // 范围的最小值
        int nMax;       // 范围的最大值
        UINT nPage;     // 页面大小
        int nPos;       // 当前位置
        int nTrackPos;  // 当前追踪位置
    }SCROLLINFO, *PSCROLLINFO;
    */
    static int cxChar, cxCaps, cyChar, cxClient, cyClient, iMaxWidth;
    HDC hdc;
    int i, x, y, iVertPos, iHorzPos, iPaintBeg, iPaintEnd;
    PAINTSTRUCT ps;
    SCROLLINFO si;
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

        iMaxWidth = 40 * cxChar + 22 * cxCaps;
        return 0;

    case WM_SIZE:
        cxClient = LOWORD(lParam);
        cyClient = HIWORD(lParam);

        si.cbSize = sizeof(si);
        // 设置页面range和page
        si.fMask = SIF_RANGE | SIF_PAGE;
        si.nMin = 0;
        si.nMax = NUMLINES - 1;
        si.nPage = cyClient / cyChar;
        SetScrollInfo(hwnd, SB_VERT, &si, TRUE);

        si.cbSize = sizeof(si);
        si.fMask = SIF_RANGE | SIF_PAGE;
        si.nMin = 0;
        si.nMax = 2 + iMaxWidth / cxChar;
        si.nPage = cxClient / cxChar;
        // SetScrollInfo(hwnd, iBar, &si, bRedraw);
        SetScrollInfo(hwnd, SB_HORZ, &si, TRUE);
        return 0;

    case WM_VSCROLL:
        si.cbSize = sizeof(si);
        // SIF_RANGE, SIF_POS, SIF_PAGE, SIF_TRACKPOS
        si.fMask = SIF_ALL;
        GetScrollInfo(hwnd, SB_VERT, &si);

        iVertPos = si.nPos;

        switch(LOWORD(wParam)) {
        case SB_TOP:
            si.nPos = si.nMin;
            break;
            
        case SB_BOTTOM:
            si.nPos = si.nMax;
            break;

        case SB_LINEUP:
            si.nPos -= 1;
            break;

        case SB_LINEDOWN:
            si.nPos += 1;
            break;

        case SB_PAGEUP:
            si.nPos -= si.nPage;
            break;

        case SB_PAGEDOWN:
            si.nPos += si.nPage;
            break;

        case SB_THUMBTRACK:
            si.nPos = si.nTrackPos;
            break;

        default:
            break;
        }

        // 在调用SetScrollInfo时，须在nPos字段中指定滚动条的位置
        // 而GetScrollInfo则在nPos中返回当前的位置
        si.fMask = SIF_POS;
        SetScrollInfo(hwnd, SB_VERT, &si, TRUE);
        GetScrollInfo(hwnd, SB_VERT, &si);

        if (si.nPos != iVertPos) {
            // 后两个参数设置为NULL，标志滚动这个客户区。
            ScrollWindow(hwnd, 0, cyChar*(iVertPos - si.nPos), NULL, NULL);
            UpdateWindow(hwnd);
        }

        return 0;

    case WM_HSCROLL:
        si.cbSize = sizeof(si);
        si.fMask = SIF_ALL;
        GetScrollInfo(hwnd, SB_HORZ, &si);

        iHorzPos = si.nPos;

        switch (LOWORD(wParam)) {
        case SB_LINELEFT:
            si.nPos -= 1;
            break;

        case SB_LINERIGHT:
            si.nPos += 1;
            break;

        case SB_PAGELEFT:
            si.nPos -= si.nPage;
            break;

        case SB_PAGERIGHT:
            si.nPos += si.nPage;
            break;

        case SB_THUMBPOSITION:
            si.nPos = si.nTrackPos;
            break;

        default:
            break;
        }

        si.fMask = SIF_POS;
        SetScrollInfo(hwnd, SB_HORZ, &si, TRUE);
        GetScrollInfo(hwnd, SB_HORZ, &si);

        if (si.nPos != iHorzPos) {
            ScrollWindow(hwnd, cxChar*(iHorzPos - si.nPos), 0, NULL, NULL);
            UpdateWindow(hwnd);
        }

        return 0;

    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);

        si.cbSize = sizeof(si);
        si.fMask = SIF_POS;
        GetScrollInfo(hwnd, SB_VERT, &si);
        iVertPos = si.nPos;

        GetScrollInfo(hwnd, SB_HORZ, &si);
        iHorzPos = si.nPos;

        // 决定哪些行落在了无效矩形中，并只重绘这些行。
        iPaintBeg = max(0, iVertPos + ps.rcPaint.top / cyChar);
        iPaintEnd = min(NUMLINES - 1, iVertPos + ps.rcPaint.bottom / cyChar);

        for (i = iPaintBeg; i < iPaintEnd; i++) {
            x = cxChar*(1 - iHorzPos);
            y = cyChar *(i - iVertPos);

            TextOut(hdc, x, y, sysmetrics[i].szLabel, lstrlen(sysmetrics[i].szLabel));
            TextOut(hdc, x + 22 * cxCaps, y, sysmetrics[i].szDesc, lstrlen(sysmetrics[i].szDesc));
            SetTextAlign(hdc, TA_RIGHT | TA_TOP);
            TextOut(hdc, x + 22 * cxCaps + 40 * cxChar, y, szBuffer,
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