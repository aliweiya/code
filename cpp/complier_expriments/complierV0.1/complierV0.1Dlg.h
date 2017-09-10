
// complierV0.1Dlg.h : header file
//

#pragma once
#include "afxwin.h"
#include "afxcmn.h"


// CcomplierV01Dlg dialog
class CcomplierV01Dlg : public CDialogEx
{
// Construction
public:
	CcomplierV01Dlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_COMPLIERV01_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnOpenFile();
	afx_msg void OnExit();
	afx_msg void OnRun();
	CEdit source;
	CListCtrl lexicalAnalysis;
	CListCtrl fourElementType;
	CListCtrl grammerAnalysis;
};
