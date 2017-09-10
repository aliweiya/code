#pragma once

#include<string>
#include<windows.h>
#include<list>

using namespace std;

typedef unsigned int ThreadID;

enum ThreadStatus{RUNNING,READY,BLOCKED,DIE};

class Thread {

public:
	Thread(string tName = "unknown");
	virtual void run() = 0;
	void yield();
	void exit();

	string threadName;
	ThreadID threadId;
	void* context;
	ThreadStatus threadStatus;
};

class Schedular {
public:
	Schedular();
	void terminateThread(Thread* t);
	void createThread(Thread * t);	
	void suspendThread(ThreadID tid);
	void resumeThread(Thread* t);
	void schedule();

	list<Thread *> threadList;
	int threadNum;
	Thread* currentThread;
	ThreadID id;
};
