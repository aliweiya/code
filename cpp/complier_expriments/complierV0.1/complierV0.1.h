
// complierV0.1.h : main header file for the PROJECT_NAME application
//

#pragma once

#ifndef __AFXWIN_H__
	#error "include 'stdafx.h' before including this file for PCH"
#endif

#include "resource.h"		// main symbols


// CcomplierV01App:
// See complierV0.1.cpp for the implementation of this class
//

class CcomplierV01App : public CWinApp
{
public:
	CcomplierV01App();

// Overrides
public:
	virtual BOOL InitInstance();

// Implementation

	DECLARE_MESSAGE_MAP()
};

extern CcomplierV01App theApp;