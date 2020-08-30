one piece
---------
```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

메뉴는 read, run에서 선택 가능 . 
read메뉴 선택시 전역변수 영역에 40바이트 입력받음 
문자열에 gomugomunomi 가 들어가면 아까 문자열을 입력한 전역변수를 인자로 mugiwara 함수 실행 
특정 주소 출력해주고 스택영역에 40바이트 입력받음. 마찬가지로 libc 주어지지 않음. 

출력하는 주소는 code영역 주소로 확인됨. 

문자열 입력 전에 연산 루틴이 있는데, 입력 버퍼의 47위치까지 반복문이 돌고,
버퍼의 배열 하나씩에 read에서 입력한 문자열을 넣되, 
문자열이 z면 다음 인덱스에 0x89를 넣어준다. 

이때 버퍼 영역 바로 다음에는 fgets의 인자가 될 사이즈 값이 들어있다.
마지막 문자열에 z를 넣어주면 size를 덮어씌울 수 있는것.
그러면 0x89바이트만큼 입력을 넣어줄 수 있고, 0x38 부터 ret 위치를 덮어씌울 수 있다. 

codebase를 알고있으니 plt, got를 이용한 함수 실행이 가능하다 
rop를 진행하여 libc 찾고 main으로 돌아가자

이제 libcbase를 찾아서 원샷을 쓰던가, 아니면 rop를 마저 진행하면 될듯. 

rsi 인자에 0 을 넣어주는 동작을 먼저 하고, binsh주소를 인자로 하여 system을 실행하면 끝. 



