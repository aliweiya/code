#define ElemType int

#include<stdio.h>
#include<stdlib.h>
#include<time.h>

typedef struct tagLNode{
    ElemType data;
    struct LNode *next;
}LNode, *LinkList;

LinkList randomLinkList(int num, ElemType max){
    // generate a link list with random data
    LinkList L = (LinkList)malloc(sizeof(LNode));
    int i;
    LNode *p = L;

    srand((unsigned)time(NULL)); 

    for(i=0; i<=num; i++){
        LNode *new = (LNode*)malloc(sizeof(LNode));
        new->data = (ElemType)(rand() % max);
        p->next = new;
        p = new;
    }
    return L;
}


int main(){
    LinkList L = randomLinkList(100, 100);
    LNode *p = L->next;
   
    int i=1; 
    while(p->next!=NULL){
        printf("%d:%d\n", i, p->data);
        p = p->next;
        i++;
    }
    return 0;
}
