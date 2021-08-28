$iii = Add-Type -memberDefinition @"
[DllImport("User32")]
public static extern int MessageBox (
long hWnd,
string lpText,
string lpCaption,
int uType);
"@ -passthru -name XXX
 
$iii::MessageBox(0 ,'test' ,'title' ,0)