#include<iostream>
#include"thread.h"
#include<Windows.h>

using namespace std;

extern Schedular * s;

class Thread1 : public Thread {
public:
	Thread1(string s): Thread(s) {
		threadName = s;
	}
	void run() {
		for (int i = 0; i < 10; i++) {
			Sleep(200);
			cout <<i<<" "<< this->threadId << " " << this->threadName << endl;
			if (i == 6 &&this->threadId == 1) {
				this->yield();
			}
			if (i == 6 && this->threadId == 2) {
				this->exit();
			}
		}
		this->exit();
	}
};
int main() {
	Thread1 t1 = Thread1("thread1");
	Thread1 t2 = Thread1("thread2");
	Thread1 t3 = Thread1("thread3");
	s->schedule();
	s->resumeThread(&t1);
	s->schedule();
	system("pause");
}