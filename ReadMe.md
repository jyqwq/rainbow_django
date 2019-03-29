隔离环境
    
    更改环境时运行
    生成requirement文件：pip freeze > requirements.txt
    
    生成环境时运行
    根据requirement文件安装依赖库：pip install -r requirement.txt

服务器状态码

    codes=[
        {"status_code": "10000", "status_text": "用户名已经存在"},
        {"status_code":"10001","status_text":"注册成功"},
        {"status_code":"10002","status_text":"用户已经存在"},
        {"status_code":"40004","status_text":"系统错误"},
        {"status_code":"10003","status_text":"登录成功"},
        {"status_code":"10004","status_text":"该用户不存在"},
        {"status_code":"10005","status_text":"密码错误"},
        {"status_code":"10006","status_text":"登录过期"},
        {"status_code":"10007","status_text":"未登录"},
        {"status_code":"40005","status_text":"数据格式不合法"},
        {"status_code":"10008","status_text":"发布成功"},
        {"status_code":"10009","status_text":"关注成功"},
        {"status_code":"10010","status_text":"删除成功"},
        {"status_code":"10011","status_text":"已关注"},
        {"status_code":"10012","status_text":"未关注"},
        {"status_code":"10013","status_text":"记录成功"},
        {"status_code":"10014","status_text":"更新成功"},
        {"status_code":"10015","status_text":"收藏成功"},
        {"status_code":"10016","status_text":"已收藏"},
        {"status_code":"10017","status_text":"未收藏"},
        {"status_code":"10018","status_text":"赞成功"},
        {"status_code":"10019","status_text":"已赞"},
        {"status_code":"10020","status_text":"未赞"},
        {"status_code":"10021","status_text":"评论成功"},
        ,
        {"status_code":"40000","status_text":"请求方法不合法"},
        {"status_code":"20000","status_text":"请求成功"},
        {"status_code":"10023","status_text":"保存成功"},
    ]

路由接口传值表

    总路由
        django_project
            # 网站主页 index post请求
            # 子路由
            user.urls
            sharing.urls
            search.urls

    分路由

        user
            # 用户主页 index
            # 登录 login post请求  
                {"telephone":*,"password":*}
            # 注册 register post请求 
                {"telephone":*,"password":*,"name":*,"register_time":*}
            # 修改手机号 newTel post请求
            # 修改密码 newPassword post请求
            # 个人信息改查 personInfo post请求 
                查 {"user_id":*,"method":"check"} 
                改 {"user_id":*,"method":"update","name|autograph|birth":*}
            # 我的个人动态 myDynamics get请求 
                user_id/page/
            # 我的关注动态 trendsConcern get请求  
                user_id/page/
            # 单个动态 oneDynamic get请求 
                (dynamic|dairy|test)/id/
            # 评论增删查 viewComment post请求
                增 {"method":"add","type":"dynamic|dairy|test|commodity","id":*,"user_id":*,"content":*,"date":*} //id为动态或者产品id
                删 {"method":"del","type":"dynamic|dairy|test|commodity","id":*,"user_id":*} //id为动态或者产品id
                查 {"method":"check","target":[{"type":"dynamic|dairy|test|commodity","id":*},{...}]} //id为动态或者产品id
            # 点赞增删改查 viewCompliment post请求
                增 {"method":"add","type":"dynamic|dairy|test|commodity","id":*,"user_id":*,"date":*} //id为动态或者产品id
                删 {"method":"del","type":"dynamic|dairy|test|commodity","id":*,"user_id":*} //id为动态或者产品id
                查 {"method":"check","target":[{"type":"dynamic|dairy|test|commodity","id":*,"user_id":*},{...}]} //id为动态或者产品id (只给id 只给user_id 都给)
            # 收藏增删改查 viewCollections post请求
                增 {"method":"add","type":"dynamic|dairy|test|commodity","id":*,"user_id":*,"date":*} //id为动态或者产品id
                删 {"method":"del","type":"dynamic|dairy|test|commodity","id":*,"user_id":*} //id为动态或者产品id
                查 {"method":"check","target":[{"type":"dynamic|dairy|test|commodity","id":*,"user_id":*},{...}]} //id为动态或者产品id (只给id 只给user_id 都给)
            # 关注增删改查 viewConcern post请求
                增 {"method":"add","concern_id":*,"follower_id":*,"date":*}
                删 {"method":"del","concern_id":*,"follower_id":*}
                查 {"method":"check","concern_id":*,"follower_id":*}
            # 七牛云token qiniuToken post请求
                上传头像 {"method":"icon","iconname":*}
                分享图片 {"method":"sharing","name":[*,*,*]}
            # 保存图片 imgSave post请求
                {"type":"dynamic|dairy|test|commodity","id":*,"url":*}

        sharing
            # 分享主页 index
            # 分享发布 releaseSharing post请求
                心情 {"type":"dynamic","content":*,"tags":*,"date":*,"user_id":*}
                日记 {"type":"dairy","title":*,"content":*,"tags":*,"date":*,"user_id":*}
                测评 {"type":"test","title":*,"content":*,"tags":*,"date":*,"user_id":*,"subtitle":[{"title":*,"content":*},{"title":*,"content":*}]}
                产品 {"type":"commodity":*,"name":*,"price":*,"brand":*,"component":*,"Effect":*,"capacity":*,"security":*,"overdue":*,"date":*,"category_id":*,"skin":[中性肤质,干性肤质,油性肤质,混合性肤质,敏感性肤质]}

        search
            # 搜索主页 index
            # 普通搜索 searchAll get请求
                ?key=*&page=*
            # 产品分类搜索 searchProduct get请求
                ?key=*&page=*
            # 品牌分类搜索 searchBrand get请求
                ?key=*&page=*
            # 成分分类搜索 searchComponent get请求
                ?key=*&page=*
            # 效果分类搜索 searchEffect get请求
                ?key=*&page=*
            # 品种分类搜索 searchVarieties get请求
                ?key=*&page=*
            # 标签分类搜索 searchTags get请求
                ?key=*&page=*
            # 搜索心情 searchDynamic get请求
                ?key=*&page=*
            # 搜索日记 searchJournal get请求
                ?key=*&page=*
            # 搜索测评 searchTest get请求
                ?key=*&page=*
            # 实时热搜排行 hotSearch get请求
                ?page=*
            # 热门日记排行 hotDairy get请求
                ?page=*
            # 热门测评排行 hotTest get请求
                ?page=*
            # 热门妆品排行 hotCosmetics get请求
                ?page=*
            # 热搜关键字 增查 hotKey post请求
                增 {"method":"add","content":*,"date":*,"user_id":*}
                查 {"method":"check"}
            # 单个产品 oneProduct get请求
                ?id=*

数据库对照表

    user模块

        user 用户表
            telephone
            password
            register_time

        sex 性别表
            sex

        icon 头像表
            icon_url

        skin 肤质表
            skin

        followers 关注表
            follower
            concern
            date

        userInfo 用户信息表
            user
            name
            autograph
            birth
            sex
            icon
            skin
            fans
            follow
            fbs
            cols
            com

    sharing模块

        dynamic 心情表
            user
            content
            tags
            date
            click
            fbs
            cols
            com

        dairy 日记表
            user
            title
            content
            tags
            date
            click
            fbs
            cols
            com

        test 测评表
            user
            title
            content
            tags
            date
            click
            fbs
            cols
            com

        testSubtitle 测评附表
            main
            title
            content

        dynamicImg 心情图片表
            url
            dynamic
            size

        dairyImg 日记图片表
            url
            dairy
            size

        testImg 测评图片表
            url
            test
            size

        dynamicFbs 心情点赞表
            user
            dynamic
            date

        dairyFbs 日记点赞表
            user
            dairy
            date

        testFbs 测评点赞表
            user
            test
            date

        dynamicCol 心情收藏表
            user
            dynamic
            date

        dairyCol 日记收藏表
            user
            dairy
            date

        testCol 测评收藏表
            user
            test
            date

        dynamicCom 心情评论表
            user
            dynamic
            content
            date

        dairyCom 日记评论表
            user
            dairy
            content
            date

        testCom 测评评论表
            user
            test
            content
            date

    search模块
        
        Category 品种表
            Category
            
        Commodity 产品表
            name
            price
            brand 品牌
            component 成分
            Effect 效果
            adaptability 皮肤适性 MM
            category 种类 F
            capacity 容量
            security
            overdue
            date
            click
            fbs
            cols
            com
            
        CommodityImg 产品图片表
            url
            commodity
            size
            
        CommodityFbs 产品点赞表
            user
            commodity
            date
            
        CommodityCol 产品收藏表
            user
            commodity
            date
            
        CommodityCom 产品评论表
            user
            commodity
            content
            date
            
        SearchKey 搜索关键字表
            user
            content
            date