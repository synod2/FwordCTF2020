#include <stdio.h>

int main(){
    int * fd ;
    char buf[10];
    fd = open("flag.txt",0);
    read(fd,buf,10);
    write(0,buf,10);
    
    return 0;
}