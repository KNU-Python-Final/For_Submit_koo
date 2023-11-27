# 9조-패션왕 김팽맨

## 🖥️ 게임 실행 방법
mainmenu.py 파일을 실행하면 게임이 시작됩니다.

## 🎮 게임 구성 및 설명
1라운드는 팩맨, 2라운드는 피버타임(유령 피하기), 3라운드는 상점으로 구성되어 있습니다.

1라운드 설명
- 팩맨 점수 얻는 조건: 코인 획득 시 점수가 오릅니다. 또한 파워 업 상태(power_up = True)로 유령을 잡을 시 300 단위로 점수가 올라갑니다.
- 유령에 닿을 시 오른쪽 아래 생명이 하나 줄어들고, 시작 위치로 이동됩니다. 생명이 0이 될 시(= 모든 하트가 사라질 시) 게임 오버 메시지가 출력되며 게임이 종료됩니다.


2라운드 설명
- 좌 우 방향키를 이용하여 떨어지는 유령을 피하고 코인을 획득합니다.
- 2라운드는 피버타임으로 1라운드를 무조건 클리어 해야하며, 20초의 시간 제한이 있습니다.
- 시간 제한과 관련 없이 유령에 닿으면 게임이 종료됩니다.


3라운드 설명
- 1라운드와 2라운드에 모은 코인을 소비할 수 있는 상점 기능을 제공합니다.
- 총 4개의 상품을 구입할 수 있고, 버튼을 눌러 팩맨의 눈을 하트로 변경할 수 있습니다.
- 다음 게임부터 구입한 의상으로 게임을 진행할 수 있습니다.



## ✔️ 라운드 별 게임 실행 방법
test.py 파일을 이용하여 각각 라운드별로 실행할 수 있습니다. 

test.py 파일 내 import는 주석 처리를 하지 않습니다.

`import pacman_2`
`import round3`
`import round2_1`

`
`pacman_2.pacman() # 1라운드`
`round2_1.round2() # 2라운드`
`round3.round3() # 3라운드`

실행을 원하는 라운드의 주석을 해제한 후 게임을 실행하면 해당 라운드만 실행할 수 있습니다.

ex) 1라운드 실행 시

`
import pacman_2
import round3
import round2_1 

pacman_2.pacman() # 1라운드
#round2_1.round2() # 2라운드
#round3.round3() # 3라운드`
**
