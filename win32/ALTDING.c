/*----------------------------------------------------------------------------
ALTWIND.c Alternate and Winding Fill Modes
----------------------------------------------------------------------------*/
#include<windows.h>

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    static TCHAR szAppName[] = TEXT("AltWind");

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
        TEXT("Bezier Splines"),                         // window caption
        WS_OVERLAPPEDWINDOW,                            // window style 
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

    static POINT aptFigure[10] = { 10,70,50,70,50,10,90,10,90,50,30,50,30,90,70,90,70,30,10,30 };
    static int cxClient, cyClient;
    HDC hdc;
    int i;
    PAINTSTRUCT ps;
    POINT apt[10];

    switch (message) {
    case WM_SIZE:
        cxClient = LOWORD(lParam);
        cyClient = HIWORD(lParam);
        return 0;

    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);

        SelectObject(hdc, GetStockObject(GRAY_BRUSH));

        for (i = 0; i < 10; i++) {
            apt[i].x = cxClient*aptFigure[i].x / 200;
            apt[i].y = cxClient*aptFigure[i].y / 200;
        }

        SetPolyFillMode(hdc, ALTERNATE);
        Polygon(hdc, apt, 10);

        for (i = 0; i < 10; i++) {
            apt[i].x += cxClient / 2;
        }

        SetPolyFillMode(hdc, WINDING);
        Polygon(hdc, apt, 10);

        EndPaint(hwnd, &ps);
        return 0;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, message, wParam, lParam);
}