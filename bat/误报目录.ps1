Add-Type -AssemblyName System.Windows.Forms

$yesterday = (get-date).adddays(-1)| get-date -format "yyyyMMdd"

$error_path = "\\172.16.104.212\share_write\fa_analysis_ret\" + $yesterday + "_sample_web"

$error_path

if (Test-Path $error_path) {
    explorer $error_path
}
else {
    [System.Windows.Forms.MessageBox]::Show('目录不存在！', "误报目录")
}