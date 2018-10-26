/*---------------------------------------------------------------------
  Display "Hello Windows!"

  匈牙利标注法（Hungarian Notation）
  - 变量名前都有一个短前缀，用以表明该变量的数据类型。i表示int，sz表示以零结尾的字符串
 --------------------------------------------------------------------*/

#include<windows.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
	PSTR szCmdLine, int iCmdShow) {
	MessageBox(NULL, TEXT("Hello, Windows!"), TEXT("HelloMsg"), 0);

	return 0;
}