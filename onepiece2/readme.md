one piece remake 
-----------------
```
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```
리메이크라더니 보호기법이 퇴화했다. 그리고 32비트로 바뀌었다. 
전체적인 메뉴 구조는 똑같은데, read시에 5바이트만 입력받는다. 

그리고 mugiwara 함수에서 0x64바이트를 입력받는데, printf에서 fsb가 발생하는걸로 보인다. 

libc주소 따고 got overwrite로 진행하자. 
5번째에서 libc주소가 나오긴 하는데 , 무슨 주소인지를 모르겠다. 
찾아보니 ld 영역 주소였음. 
18번째에서 vfprintf+11 의 주소가 나오는데 리모트에서는 좀 다르더라. 

4바이트 이상을 입력 후에 출력하면 menu전에 뭔가 leak 되는게 있는데,
이건 fgets+153의 주소값이다.

run메뉴를 보면, 전역변수 sc에 쓰여진 주소로 리턴해 들어가는 동작을 하는 부분이 있다. 
read에서 입력받는 값이 전역변수 영역으로 들어가는듯. 

pie가 안걸려있으니, main함수 시작시점으로 돌려버릴수 있다. 
그리고 init 함수에선 setvbuf 함수가 stdout, stdin 등을 인자로 실행되고 있다
따라서 setvbuf 함수의 got를 출력함수로 돌려버리고 실행시키면 std~ 의 libc 상 ���소가 나올것이다. 

fsb에서 %hn 서식문자는 지금까지 출력된 문자열 갯수를 대응되는 주소 영역에 쓰는 동작을 한다. 

어.. 근데 sc에서 실행하는게 주소값이 아니라 
써놓은 명령어 자체를 실행한다. 5바이트짜리 어셈을 넣으라는 뜻. 
fsb를 이용해서 원하는 명령어 모양을 만들어줄 수는 있다. 

exit의 got도 메인함수 위치로 바꿔버리자. 
그럼 메인으로 돌아가면서 init 함수를 실행할 수 있고, libc 주소를 찾는게 가능하다. 
가져온 주소는 stdout+71 주소. libc db 보면 여러개 나오는데 일단 하나 잡고 해봐야될듯 

이제 libc 땃으니 system("/bin/sh") 호출해야된다. 
똑같이 stdvbuf got 덮어쓰고 stdin got 를 binsh로 씌워줘보려 했는데, stdin은 write가 안된다. 

그냥 명령어 넣는 부분에서 가젯가지고 rop 가능한지 해볼까,
sc 영역 뒤에 1바이트씩 명령어를 집어넣어주자. 

push 3번 + ret 면 될거같은데.. 

쉘은 실행했으나, flag.txt 에 cat이 안된다. 이런..
cat 명령어를 막아놨다는 모양인듯. 
open-read-write로 접근해보자. 

푸시를 서너번씩은 해줘야된다. 
그리고 특정 영역에 flag.txt 문자열을 써줘야한다.

완전히 rop를 진행하란 얘기같다. 

open(sc+0x20,"r")
read(3,sc+0x50,0x50)
puts(sc+0x50)

로 세팅하고 ROP를 진행한다. 서버측 libc는 달라질 수 있으니 
libcdb에서 버전별로 찾아와서 넣어두자 . 

다른 풀이 보니까 쉘 띄우고 리눅스 커맨드로 해결하는게 있었다. 
grep Fword ./flag.txt
이거랑
read $s < flag.txt
echo $s

등등...
옘병...시간낭비 오지게 했네..
그래도 익스 짜는 연습은 잘 된듯. 
