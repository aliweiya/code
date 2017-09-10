
// complierV0.1Dlg.cpp : implementation file
//

#include "stdafx.h"
#include "complierV0.1.h"
#include "complierV0.1Dlg.h"
#include "afxdialogex.h"

#include "complier.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CAboutDlg dialog used for App About

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// Dialog Data
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CcomplierV01Dlg dialog



CcomplierV01Dlg::CcomplierV01Dlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_COMPLIERV01_DIALOG, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CcomplierV01Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_EDIT1, source);
	DDX_Control(pDX, IDC_LIST1, lexicalAnalysis);
	DDX_Control(pDX, IDC_LIST2, fourElementType);
	DDX_Control(pDX, IDC_LIST3, grammerAnalysis);
}

BEGIN_MESSAGE_MAP(CcomplierV01Dlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_COMMAND(ID_32771, &CcomplierV01Dlg::OnOpenFile)
	ON_COMMAND(ID_32772, &CcomplierV01Dlg::OnExit)
	ON_COMMAND(ID_32773, &CcomplierV01Dlg::OnRun)
END_MESSAGE_MAP()


// CcomplierV01Dlg message handlers

BOOL CcomplierV01Dlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	// TODO: Add extra initialization here

	lexicalAnalysis.ModifyStyle(0, LVS_REPORT);
	fourElementType.ModifyStyle(0, LVS_REPORT);
	grammerAnalysis.ModifyStyle(0, LVS_REPORT);

	// 为列表视图控件添加全行选中和栅格风格   
	lexicalAnalysis.SetExtendedStyle( LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES);
	fourElementType.SetExtendedStyle(LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES);
	grammerAnalysis.SetExtendedStyle(LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES);

	lexicalAnalysis.InsertColumn(0, L"单词", LVCFMT_CENTER, 80);
	lexicalAnalysis.InsertColumn(1, L"二元序列", LVCFMT_CENTER, 80);
	lexicalAnalysis.InsertColumn(2, L"类型", LVCFMT_CENTER, 80);
	lexicalAnalysis.InsertColumn(3, L"位置", LVCFMT_CENTER, 80);

	fourElementType.InsertColumn(0, L"OP", LVCFMT_CENTER, 80);
	fourElementType.InsertColumn(1, L"ARG1", LVCFMT_CENTER, 80);
	fourElementType.InsertColumn(2, L"ARG2", LVCFMT_CENTER, 80);
	fourElementType.InsertColumn(3, L"RESULT", LVCFMT_CENTER, 80);

	grammerAnalysis.InsertColumn(0, L"步骤", LVCFMT_CENTER, 40);
	grammerAnalysis.InsertColumn(1, L"状态", LVCFMT_CENTER, 100);
	grammerAnalysis.InsertColumn(2, L"符号", LVCFMT_CENTER, 100);
	grammerAnalysis.InsertColumn(3, L"输入串", LVCFMT_CENTER, 100);
	grammerAnalysis.InsertColumn(4, L"操作", LVCFMT_CENTER, 200);
	

	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CcomplierV01Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CcomplierV01Dlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CcomplierV01Dlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}



void CcomplierV01Dlg::OnOpenFile()
{
	// TODO: Add your command handler code here
	CFileDialog FileDlg(TRUE, L"", L"", OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT, L"txt文件|*.txt|所有文件|*.*||");
	FileDlg.m_pOFN->lpstrTitle = L"打开文件"; //文件对话框标题  
	if (FileDlg.DoModal() == IDOK)
	{
		CString filePath = FileDlg.GetPathName();
		CString buf;
		CString strTmp;
		CStdioFile file;
		if (file.Open(filePath, CFile::modeRead)) {
			while (file.ReadString(buf) != FALSE)
				strTmp = strTmp + buf + L"\r\n";
			file.Close();
		}
		source.SetWindowTextW(strTmp);
	}
}


void CcomplierV01Dlg::OnExit()
{
	// TODO: Add your command handler code here
	PostQuitMessage(0);
}


void CcomplierV01Dlg::OnRun()
{
	// TODO: Add your command handler code here
	CString s;
	source.GetWindowTextW(s);
	string str = CStringA(s);
	lexAnalysis(str);
	lexicalAnalysis.DeleteAllItems();
	for (int i = 0; i < lex.size(); i++) {
		lexicalAnalysis.InsertItem(i,L"");
		s = lex[i].token.c_str();
		lexicalAnalysis.SetItemText(i,0,s);
		CString t,t2;
		t.Format(L"%d", lex[i].type);
		t2 = L"( " + t + L" , " + s + L" )";
		lexicalAnalysis.SetItemText(i, 1, t2);
		if(lex[i].type == 1)
			lexicalAnalysis.SetItemText(i, 2,L"关键字");
		else if(lex[i].type == 2)
			lexicalAnalysis.SetItemText(i, 2, L"标识符");
		else if (lex[i].type == 3)
			lexicalAnalysis.SetItemText(i, 2, L"常数");
		else if (lex[i].type == 4)
			lexicalAnalysis.SetItemText(i, 2, L"运算符");
		else if (lex[i].type == 5)
			lexicalAnalysis.SetItemText(i, 2, L"分隔符");
		else if (lex[i].type == 6)
			lexicalAnalysis.SetItemText(i, 2, L"关系运算符");
		CString l, r;
		l.Format(L"%d", lex[i].line);
		r.Format(L"%d", lex[i].row);
		s = L"( " + l + L" , " + r + L" )";
		lexicalAnalysis.SetItemText(i, 3, s);
	}
	if (grammAnalysis(str)) {
		for (int i = 0; i < gramm.size(); i++) {
			grammerAnalysis.InsertItem(i, L"");
			CString t,st,sy,op,left;
			t.Format(L"%d", gramm[i].step);
			grammerAnalysis.SetItemText(i, 0, t);
			st = gramm[i].status.c_str();
			grammerAnalysis.SetItemText(i, 1, st);
			sy = gramm[i].symbol.c_str();
			grammerAnalysis.SetItemText(i, 2, sy);
			left = gramm[i].left.c_str();
			grammerAnalysis.SetItemText(i, 3, left);
			op = gramm[i].op.c_str();
			grammerAnalysis.SetItemText(i, 4, op);
		}
		for (int i = 0; i < fourEle.size(); i++) {
			fourElementType.InsertItem(i, L"");
			CString o,a1,a2,r;
			o = fourEle[i].op.c_str();
			fourElementType.SetItemText(i, 0, o);
			a1= fourEle[i].arg1.c_str();
			fourElementType.SetItemText(i, 1, a1);
			a2 = fourEle[i].arg2.c_str();
			fourElementType.SetItemText(i, 2, a2);
			r = fourEle[i].result.c_str();
			fourElementType.SetItemText(i, 3, r);
		}
	}
	else {
		MessageBox(_T("ERROR"), _T("ERROR"), MB_OK);
	}
}
