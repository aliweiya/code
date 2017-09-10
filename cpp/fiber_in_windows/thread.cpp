#include"thread.h"
#include<iostream>

Schedular *s;
void WINAPI fiber(void *lpParameter);
void* mainFiber;

Thread::Thread(string tName) {
	if (s == nullptr) {
		static Schedular schedular = Schedular();
		s = &schedular;
	}
	this->context = CreateFiber(0, fiber, this);
	this->threadName = tName;
	this->threadStatus = READY;
	s->createThread(this);
	cout << this->threadId << " " << this->threadName << " created!" << endl;
}
void Thread::yield() {
	cout << this->threadId << " " << this->threadName << " yield!" << endl;
	this->context = GetCurrentFiber();
	s->suspendThread(this->threadId);
}
void Thread::exit() {
	cout << this->threadId << " " << this->threadName << " exit!" << endl;
	this->threadStatus = DIE;
	s->terminateThread(this);
}

Schedular::Schedular() {
	mainFiber = ConvertThreadToFiber(NULL);
	id = 0;
	threadNum = 0;
}
void Schedular::terminateThread(Thread* t) {
	threadNum--;
	for (auto it = this->threadList.begin(); it != this->threadList.end(); it++) {
		if ((*it) == t) {
			threadList.erase(it);
			break;
		}
	}
	s->schedule();
}
void Schedular::createThread(Thread* t) {
	t->threadId = ++id;
	threadNum++;
	threadList.push_back(t);
}
void Schedular::suspendThread(ThreadID tid) {
	for (auto it = this->threadList.begin(); it != this->threadList.end(); it++) {
		if ((*it)->threadId == tid) {
			s->currentThread->threadStatus = BLOCKED;
			s->schedule();
			return;
		}
	}
}
void Schedular::resumeThread(Thread* t) {
	for (auto it = this->threadList.begin(); it != this->threadList.end(); it++) {
		if ((*it)==t) {
			t->threadStatus = READY;
			return;
		}
	}
}
void Schedular::schedule() {
	if (threadNum == 0) {
		cout << "No thread here!" << endl;
		return;
	}
	for (auto it = this->threadList.begin(); it != this->threadList.end(); it++) {
		if ((*it)->threadStatus == DIE) {
			s->threadList.erase(it);
			threadNum--;
		}
	}
	for (auto it = this->threadList.begin(); it != this->threadList.end(); it++) {
		if ((*it)->threadStatus == READY) {
			s->currentThread = (*it);
			(*it)->threadStatus = RUNNING;
			SwitchToFiber((*it)->context);
			return;
		}
	}
	cout << "No thread can be run, schedule end!" << endl;
	return;
}
void WINAPI fiber(void *lpParameter) {
	Thread* t = (Thread*)lpParameter;
	t->run();
	SwitchToFiber(mainFiber);
}