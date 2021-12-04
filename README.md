# hanwhabot
This is Hanwhabot
plz make branch master
## Mission 1 Describe
Mission 1 is for lane detection and get stopped in stop line.

알고리즘은 다음과 같다.
finish field는 white pixel의 수가 많은 지점을 기준으로 한다. 하지만 매번 한다면 그것은 데이터 낭비이니 service를 이용하여 특정한 때에만 시도하도록 한다.
## Mission 3 Describe
Mission 3 is for climbing stairs, discover grenade and get it.

~~어쩌면 그냥 도착지점에서 일정한 속도로 일정한 시간 후 끝내는게 안전할지도? 왜냐면 인식은 계속해서
할 수 있지만, 그것이 finish 인지 인지하는 것은 매우 힘들고, 인지한다 하더라도, 거기까지의 거리를 
따로 측정해 줘야지만 stop signal 호출이 편한데, 둘 다 힘든 케이스 인듯 하다.~~

Imu data의 UpDown, DownUp을 기준으로 판단한다. 초기 상태는 pitch 데이터가 거의 0에 수렴하는 상태일 것. 하지만 계단을 오른다면 약 -30' 까지 올라갈 것. 그 상태에서 정상에 오른다면 다시 0에 수렴할 것이고, 내려간다면 +30' 까지 내려갈 것. 그 후 다시 도착지점에 온다면 pitch data 가 0에 수렴할 것이다. 그러므로 우리는 up down signal 을 판단하는 것을 만들어 속도를 조절해야 한다. ~~또한 직선으로 가냐 아니냐의 유무를 따지기 위해, pid 를 이용해 자신의 자세를 조정하는 것을 개발한다.~~

어떻게 하면 선형적으로 받는 데이터로 부터 현재 내가 up->down상태인지, down->up 상태인지 알 수 있을까. 부호는 쓸 수 없다. 왜냐하면 filter를 거쳐도 정상 상태일때도 완벽한 0이 아니며, -가 될 수도, +가 될 수도 있기 때문이다. 그렇다면 연속된 데이터간의 차이는 어떨까? 시간은 이미 일정한 상태이니, 

그렇다면, 매 각도 마다 signal을 만드는건 어떨까?

[0,0,0,0,-1,-8, -15, -30,-29, -31,..., -20, -10, 0, 0, ..., 10, 20, 30, 30, 30,, 20, 10, 0, 0, 0]

[0-> -30 = up, -30->0 = down, 0->30 = down, 30->0 = up]

up = 값 빼기, down = 값 더하기
0 = 정상상태, -30 = up상태, +30 = down상태 -> 

if data near 0: ZeroStableCondition = True 
elif data near -5 ~ -30 : UpStableCondition = True, else False
elif data near 5~30 : DownStableCondition = True else False

0    1    2  -->  signal box
zero up zero -> UpDownSignal --> give client req and reset
zero down zero -> DownUpSignal --> give client req and shutdown.


그렇다면 센서 값의 절대값을 특정값을 지날 때 마다 저장해서 그 값들 마다 비교하기?

아니면 0, -30, 0 을 하나의 시그널 0, 30, 0을 하나의 시그널로 생각하여 
## Mission 4 Describe
Mission 4 is for clean up obstacle and open the door and get out of there.

---
## Mission 2 and 5 with ROS1 Navigation stack
you need to have chrony or something with time synchronizer.

first launch robot description. 
```shell
roslaunch hanwhabot_description hanwhabot_bringup.launch
roslaunch hanwhabot_navigation hanwhabot_navigation_test.launch
```
above that, then publish your initial pose and goal position

```
# initial pose
rostopic pub initialpose geometry_msgs/PoseWithCovarianceStamped '{header: {seq: 3, stamp: now, frame_id: "map"}, pose: {pose: {position: {x:?, y:?, z:?, w:?}}}}'

# goal position
rostopic pub move_base_simple/goal geometry_msgs/PoseStamped '{header: {seq: 3, stamp: now, frame_id: "map"}, pose: {position: {x:?, y:?, z:?, w:?}, orientation: {x:?, y:?, z:?, w:?}}}'
```

---
## Mission Commonality(임무간 공통점)
It should start at the starting point and end at the end point.

1. start를 인지 한다.
   1. tesseract 를 이용하여 이미지에서 start를 찾는다. 
   2. masking image(start 마스크)를 이용하여, 통과한 픽셀 수가 일정 개수를 넘으면 통과로 인지
   3. 단순히 흰 화면을 인지하기. (hsv를 이용)


2. 인식이 되었고, start 라고 인지 했다면 main 모터 노드에 시그널을 보낸다. 이는 service 를 이용한다.

3. 모든 mission의 마지막은 find end 시그널을 보내야 한다.
