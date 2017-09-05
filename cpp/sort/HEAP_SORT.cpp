#include<iostream>
#include<windows.h>

using namespace std;

void MAX_HEAPIFY(int *A, int length, int heap_size ,int i) {
	int l = 2 * i;
	int r = 2 * i + 1;
	int largest = 0;
	if (l <= heap_size && A[l-1] > A[i-1])
		largest = l;
	else
		largest = i;
	if (r <= heap_size&&A[r-1] > A[largest-1])
		largest = r;
	if (largest != i) {
		int temp = A[largest-1];
		A[largest-1] = A[i-1];
		A[i-1] = temp;
		MAX_HEAPIFY(A, length,heap_size,largest);
	}
}

void BUILD_MAX_HEAP(int *A, int length,int heap_size) {
	for (int i = length / 2; i > 0; i--)
		MAX_HEAPIFY(A, length, heap_size, i);
}

void HEAP_SORT(int *A, int length, int heap_size) {
	BUILD_MAX_HEAP(A, length, heap_size);
	for (int i = length; i > 1; i--) {
		int temp = A[0];
		A[0] = A[i-1];
		A[i-1] = temp;
		heap_size--;
		MAX_HEAPIFY(A, length, heap_size, 1);
	}
}
int main() {
	int A[] = { 4,1,3,2,16,9,10,14,8,7 };
	HEAP_SORT(A, sizeof(A) / sizeof(int), sizeof(A) / sizeof(int));
	for (int i = 0; i < sizeof(A) / sizeof(int); i++)
		cout << A[i] << " ";
	cout << endl;
	system("pause");
}
