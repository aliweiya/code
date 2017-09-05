#include<iostream>
#include<windows.h>

using namespace std;

int minimize(int *A, int length, int start) {
	int key = start;
	for (int i = start + 1; i < length; i++) {
		if (A[i] < A[key]) {
			key = i;
		}
	}
	return key;
}
void SELECTION_SORT(int *A, int length) {
	for (int i = 0; i < length; i++) {
		int key = minimize(A, length, i);
		int temp = A[i];
		A[i] = A[key];
		A[key] = temp;
	}
}

int main() {
	int A[] = { 12,54,32,53,120,63,654,39,52,336,147,20 };
	SELECTION_SORT(A, sizeof(A) / sizeof(int));
	for (int i = 0; i < sizeof(A) / sizeof(int); i++) {
		cout << A[i] << "  ";
	}
	cout << endl;
	system("pause");
}
