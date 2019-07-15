<h1 align="center">用户管理</h1>

# 当前用户数据

## GET*

查看当前用户及加入房间的信息

#### url
- /api/user/current

#### return（上面成功，下面失败）
    {
        "status": 1,
        "message": "成功！"
        "data":{
            "user": {
                "username": 用户名(如果设置了),
                "user_id": 用户id,
                "registration_time": 注册时间(datetime),
                "joined_room": 是否已加入房间(布尔值),
                "gander": 性别(1为男性，0位女性),
                "birthday": 生日(str),
                "icon": 头像id,
                "individuality": 个性签名
            }
            "room":{
                "room_id": 房间id,
                "room_name": 房间名称,
                "owner_id": 房间创建者id,
                "room_size": 房间大小(2或4),
                "count": 房间现在的人数,
                "create_time": 房间创建时间(datetime)
            }
            "roommates": [
                {
                    "user_id": 用户id,
                    "join_time": 加入时间(datetime),
                    "username": 用户名
                }
                ...
            ]
        }
    }    
    
    {
        "status": 0,
        "message": 原因
    }
    
    

## POST
创建用户&登录

#### url
- /api/user/current


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    code    |    false    |    str   |    临时登录凭证    |

#### return
    {
        "status": 1,
        "message": "成功!"
        "data": {
            "token": token
        }
    }
    
    {
        "status": 0,
        "message": 原因
    } 
    
## PUT*
修改用户相关信息

#### url
- /api/user/current


#### args(可仅发送需要修改的)

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    username    |    true    |    str   |    用户名    |
|    birthday    |    true    |    str or date   |    生日      |
|    individuality    |    true    |    str   |    个性签名     |
|    gender    |    true    |    int   |    性别（1为男性，0位女性）     |
|    icon    |    true    |    int   |    头像id     |

#### return
    {
        "status": 1,
        "message": "成功!"
    }
    
    {
        "status": 0,
        "message": 原因
    }    

## DELETE*
删除用户

#### url
- /api/user/current


#### args(可仅发送需要修改的)

无


#### return（上面成功，下面失败）
    {
        "status": 1,
        "message": "成功!"
    }
    
    {
        "status": 0,
        "message": 原因
    }    



<h1 align="center">房间管理</h1>




# 房间数据

## GET*
查看指定房间id的信息

#### url
- /api/room/data


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    room_id    |    false    |    int   |  房间id   |

#### return
    {
        "status": 1,
        "message": "成功！"
        "data":{
            "room_id": 房间id,
            "room_name": 房间名称,
            "room_size": 房间大小(2或4),
            "count": 房间现在的人数,
            "create_time": 房间创建时间
        }
    }    
    
    {
        "status": 0,
        "message": 原因
    }
    

## POST*
创建房间

#### url
- /api/room/data


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    room_name    |    false    |    str   |    房间名称    |
|    room_size    |    false    |    int   |    房间大小(只能2或4)  |
|    room_password    |    false    |    str   |  房间密码   |

#### return
    {
        "status": 1,
        "message": "房间建立成功！",
        "data": {
            "room_id": 房间id
        }
    }    
    
    {
        "status": 0,
        "message": 原因
    }    
## PUT*
修改房间信息

#### url
- /api/room/data


#### args(可仅发送需要修改的)
带*表示房间创建者才能修改

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    notice    |    true    |    str   |    房间公告    |
|    room_name    |    true    |    str   |    房间名称*  |
|    room_password    |    true    |    str   |  房间密码*   |
|    room_size    |    true    |    int   |  房间大小（只能往大改）*   |


#### return
    {
        "status": 1,
        "message": "修改成功"
    }
    
    {
        "status": 0,
        "message": 原因
    } 

## DELETE*
（房间创建者）删除房间

#### url
- /api/room/data

#### args
 无
 
#### return
    {
        "status": 1,
        "message": "房间删除成功！"
    }
    
    {
        "status": 0,
        "message": 原因
    } 


# 加入房间

## POST*

#### url
- /api/room/join


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    room_id    |    false    |    int   |    房间id    |
|    room_password    |    false    |    str   |  房间密码   |

#### return
    {
        "status": 1,
        "message": "房间加入成功！",
        "data": {
            "room_id": 房间id
        }
    }    
    
    {
        "status": 0,
        "message": 原因
    } 

## DELETE*
（非房间创建者）离开房间

#### url
- /api/room/join

#### args
 无
 
#### return
    {
        "status": 1,
        "message": "房间离开成功！"
    }
    
    {
        "status": 0,
        "message": 原因
    } 

<Br />
<p align="right">其他信息一般通过socket.io传输</p>   
<p align="right">请求方式带*表示需提供token</p>
