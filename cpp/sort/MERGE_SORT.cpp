#include<iostream>
#include<windows.h>

using namespace std;

void MERGE(int *A, int p, int q, int r) {
	int *L = (int *)malloc((q - p + 1)*sizeof(int));
	int *R = (int *)malloc((r - q)*sizeof(int));
	for (int i = 0; i < q - p + 1; i++) {
		L[i] = A[p+i];
	}
	for (int i = 0; i < r - q; i++) {
		R[i] = A[q+i+1];
	}
	int i = 0, j = 0, k = p;
	while (i < q - p + 1 && j < r - q) {
		if (L[i] > R[j]) {
			A[k] =R[j];
			j++;
			k++;
		}
		else {
			A[k] = L[i];
			i++;
			k++;
		}
	}
	for (; i < q - p + 1; i++) {
		A[k] = L[i];
		k++;
	}
	for (; j < r - q; j++) {
		A[k] = R[j];
		k++;
	}
}
void MERGE_SORT(int *A, int p, int r) {
	if (p < r) {
		int q = (p + r) / 2;
		MERGE_SORT(A, p, q);
		MERGE_SORT(A, q + 1, r);
		MERGE(A, p, q, r);
	}
}
void main() {
	int A[] = { 12,54, 62,124,32,47,95,15,10,2,43 };
	MERGE_SORT(A, 0, sizeof(A) / sizeof(int)-1);
	for (int i = 0; i < sizeof(A) / sizeof(int); i++) {
		cout << A[i] << "  ";
	}
	cout << endl;
	system("pause");

}
