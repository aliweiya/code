#include<iostream>
#include<windows.h>

using namespace std;

void INSERTION_SORT(int *A, int length) {
	for (int j = 1; j < length; j++) {
		int key = A[j];
		int i = j - 1;
		while (i >= 0 && A[i] > key) {
			A[i+1] =A[i];
			i = i - 1;
		}
		A[i+1] = key;
	}
}
int main() {
	int A[10] = { 1,25,340,69,1200,63,478,235,45,10 };

	INSERTION_SORT(A, 10);
	for (int i = 0; i < 10; i++) {
		cout << A[i] << "  ";
	}
	cout << endl;
	system("pause");
}
