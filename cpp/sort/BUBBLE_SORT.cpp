#include<iostream>

using namespace std;

int BUBBLE(int *A, int length, int start) {
	int key = start;
	for (int i = start + 1; i<length; i++) {
		if (A[key] >= A[i]) {
			key=i;
		}
	}
	return key;
}

void BOBBLE_SORT(int *A, int length) {
	int key;
	for (int i = 0; i<length; i++) {
		key = BUBBLE(A, length, i);
		int temp = A[key];
		A[key] = A[i];
		A[i] = temp;
	}
}

int main() {
	int A[] = { 1,5,4,36,25,48,72,12,54 };
	BOBBLE_SORT(A, sizeof(A) / sizeof(int));
	for (int i = 0; i<sizeof(A) / sizeof(int); i++) {
		cout << A[i] << " ";
	}
	cout << endl;
	return 0;
}
