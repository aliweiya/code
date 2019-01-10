#include<stdlib.h>
#include<stdio.h>

#define ElemType int

typedef struct BiNode{
    ElemType data;
    struct BiNode *lchild;
    struct BiNode *rchild;
}BiNode, *BiTree;



BiTree Create(ElemType a[], int length, int index){
    BiTree T = NULL;
    if(index >= length)
        return T;
    if(a[index]==-1){
        return T;
    }
    T = (BiTree)malloc(sizeof(BiNode));
    T->data = a[index];
    T->lchild = Create(a, length, 2*index+1);
    T->rchild = Create(a, length, 2*index+2);
    return T;
}

void PreOrder(BiTree T){
    if(T!=NULL){
        printf("%d ", T->data);
        PreOrder(T->lchild);
        PreOrder(T->rchild);
    }
}

void InOrder(BiTree T){
    if(T!=NULL){
        InOrder(T->lchild);
        printf("%d ", T->data);
        InOrder(T->rchild);
    }
}

void PostOrder(BiTree T){
    if(T!=NULL){
        PostOrder(T->lchild);
        PostOrder(T->rchild);
        printf("%d ", T->data);
    }
}

void PostOrderNoRecursion(BiTree T){
    
}



int main(){
    ElemType a[] = {1,2,3,4,-1,-1,5,-1,-1,-1,-1};
    BiTree T;
    T = Create(a, 7, 0);
    PreOrder(T);
    printf("\n");
    InOrder(T);
    printf("\n");
    PostOrder(T);
    printf("\n");
}
