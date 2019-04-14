<h1 align="center">socket.io流程</h1>

## 简要流程
1. 建立socket.io连接 URL: / 
2. 向事件 "join_room" 发送token:
    ```
   {
        "token": token
   }
    ``` 
3. 接受事件信息

## 事件介绍
注: ['event',{"key" : "value"}] 
     表示用事件'event'传输{"key" : "value"}

     
### 加入房间(socket.io里的room)及获取房间内用户信息

#### input
    [
        "join_room",
        {
            "token": token
        }   
    ]
    
#### return
    # 正常
    # 房间内所有用户信息
    [
        "last_data",
        {
            "current_user_data":{
                "user_id": 当前用户id,
                "username": 当前用户的用户名
            }
            "room_data":{
                "room_id": 房间id,
                "room_name": 房间名称,
                "owner_id": 房间创建者id,
                "room_size": 房间大小(2或4),
                "count": 房间现在的人数,
                "create_time": 房间创建时间(datetime),
                "notice": 小黑板内容
            }
            "roommates_data": [
                {
                    "username": 用户名,
                    "user_id": 用户id,
                    "action": 当前动作,
                    "join_time": 加入时间(datetime),
                }
                ....
            ]
        }   
    ]
    
    # 异常
    [
        "join_room",
        {
            "error" : 错误原因
        }
    ]

### 离开房间(socket.io里的room)

#### input
    [
        "leave_room",
        {
            "token": token
        }   
    ]
    
#### return
    # 正常
        无
    
    # 异常
    [
        "leave_room",
        {
            "error" : 错误原因
        }
    ]

### 聊天信息

#### input
    [
        "message",
        {
            "token": token,
            "message": 聊天内容
        }   
    ]
    #每次只传输一条
    
#### return(all)
    # 正常
    [
        "message",
        {
            "token": token,
            "message": 聊天内容,
            "time": 时间(datetiem)
        }   
    ]
    #每次只传输一条
    
    # 异常
    [
        "message",
        {
            "error" : 错误原因
        }
    ]
    
### 用户活动信息

动作列表：
- 00 零食-吃零食
- 01 马桶-如厕
- 02 浴室-淋浴
- 03 洗漱台-洗脸|刷牙
- 04 洗衣机-洗衣服
- 05 床-睡觉
- 06 电脑(写字台)-上网
- 07 手机(写字台)-玩手机
- 08 衣柜-换衣服
- 09 写字台-学习
- 取消动作则置空（Null）

#### input
    [
        "action",
        {
            "token": token,
            "action": 当前动作（str）
        }   
    ]
    
    #每次只传输一条
    
#### return(all)
    # 正常
    [
        "action",
        {
            "user_id": 用户id,
            "action":  当前动作,
            "time": 时间(datetiem)
        }   
    ]
    
    # 异常
    [
        "action",
        {
            "error" : 错误原因
        }
    ]
    
    #每次只传输一条

<p align="right">all表示推送给所有房间内用户</p>

    



