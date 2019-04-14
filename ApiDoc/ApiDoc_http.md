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
                "username": 用户名,
                "user_id": 用户id,
                "email": 电子邮箱,
                "confirmed": 邮箱是否已验证(布尔值),
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
创建用户（登录）

#### url
- /api/user/current


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    username    |    false    |    str   |    用户名    |
|    email    |    false    |    str   |    邮箱      |
|    password    |    false    |    str   |    密码      |
|    password2    |    false    |    str   |    密码验证      |

#### return
    {
        "status": 1,
        "message": "成功!"
    }
    
    {
        "status": 0,
        "message": 原因
    } 
    
## PUT*
修改用户相关信息(除密码)

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
# token相关

## POST
生成token（登录）

#### url
- /api/user/token


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    username    |    false    |    str   |    用户名(邮箱也行）    |
|    password    |    false    |    str   |    密码      |

#### return
    {
        "token": token
    }
    
    {
        "status": 0,
        "message": 原因
    }    


# 修改密码（已登录状态）
需要原密码且已登录

## PUT*

#### url
- /api/user/password


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    old_password    |    false    |    str   |    旧密码    |
|    new_password    |    false    |    str   |    新密码      |
|    new_password2    |    false    |    str   |    新密码验证      |

#### return
    {
        "status": 1,
        "message": "成功!"
    }
    
    {
        "status": 0,
        "message": 原因
    } 

# 忘记密码(未登录状态)

## POST
仅发送邮件

#### url
- /api/user/forget


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|
|    username    |    false    |    str   |    用户名    |
|    email    |    false    |    str   |    邮箱    |

#### return
    {
        "status": 1,
        "message": "邮件已发送!"
    }
    
    {
        "status": 0,
        "message": 原因
    } 
## PUT
重置密码(邮箱点击链接)（还没写完）

#### url
- /api/user/forget


#### args

| args | nullable | type | remark   |
|:------:|:------:|:------:|:------:|

#### return

# 邮箱相关
验证邮箱

## GET

#### url
- /api/user/email


#### args

再定

#### return
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
