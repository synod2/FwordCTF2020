movotov
-------
```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```
시작시 어떤 주소값을 출력하고 입력을 받음. 

출력되는건 시스템 함수의 주소. 
ROP를 이용하면 될듯. 
입력 갯수 제한은 없다. 

libc주소는 libc db 통해서 찾아와 오프셋 연산을 진행한다. 

