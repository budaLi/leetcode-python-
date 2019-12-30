def Game():
    # 小游戏的开发：唐僧大战白骨精
    # 打印欢迎语句
    print('*' * 20, "欢迎来到游戏！", '*' * 20)
    print("请选择你的角色")
    print("\t1.唐僧")
    print("\t2.白骨精")
    User_Role = input("请输入1~2：")
    # 打印一行分割符
    print('-' * 55)
    if User_Role == '1':
        # 选择1
        print("你已经选择了1，你将以->唐僧<-的身份进行游戏")
    elif User_Role == '2':
        # 选择2
        print("你居然选择白骨精，太不要脸了，系统将为你匹配->唐僧<-的身份进行游戏")
    else:
        # 输入其他
        print("你的输入错误！系统将为您自动分配身份，你将以->唐僧<-的身份进行游戏")
    # 进入游戏

    # 创建变量保存玩家的信息（攻击力和生命值）
    User_life = 2  # 生命值
    User_attack = 2  # 攻击力
    # 创建变量保存Boss的生命值和攻击力
    Boss_life = 10  # boss的生命值
    Boss_attack = 10  # boss 的攻击力

    # 打印一行分割符
    print('-' * 55)

    # 显示玩家信息
    print('你的生命值为 {},你的攻击力为 {}'.format(User_life, User_attack))

    # 由于游戏选项是反复显示的，所以将以下代码写入循环中，而且是一个死循环，由break来控制循环结束
    while True:
        # 打印一行分割符
        print('-' * 55)

        # 显示游戏选项，游戏正式开始
        print("请选择你要进行的操作")
        print("\t1.练级")
        print("\t2.打boss")
        print("\t3.逃跑")
        # 获取用户的选择并保存在变量中
        User_option = input("请选择要做的操作，输入1~3：")

        # 处理用户的选择
        if User_option == '1':
            # 练级，增加玩家的生命值和攻击力
            User_life += 2
            User_attack += 2
            print('恭喜你升级了！ 你的生命值为：{},你的攻击力为：{}'.format(User_life, User_attack))
        elif User_option == '2':
            # 玩家攻击boss,boss掉血，boss掉的生命值为玩家的攻击力
            Boss_life -= User_attack

            # 打印一行分割符
            print('-' * 55)
            print("->唐僧-<攻击了->白骨精<-")
            # 判断白骨精是否还有生命值
            if Boss_life <= 0:
                # 玩家攻击力过高，白骨精死亡
                print("白骨精受到了你{}点的攻击力，重伤不治，死亡，->玩家胜利！<-".format(User_attack))
                # 游戏结束
                break
            else:
                # boss 反击
                User_life -= Boss_attack
                print("->白骨精-<攻击了->唐僧<-")
                # 判断玩家是否还有生命值
                if User_life <= 0:
                    # 白骨精攻击力过高，唐僧死亡
                    print("你受到了白骨精{}点的攻击力，重伤死亡->Game Over!<-".format(Boss_attack))
                    # 游戏结束
                    break
        elif User_option == '3':
            # 打印一行分割符
            print('-' * 55)
            # 逃跑
            print("唐僧一见到白骨精，撒腿就跑！！！游戏结束。。")
            break
        else:
            # 打印一行分割符
            print('-' * 55)
            print("输入有误！请重新输入！")


if __name__ == "__main__":
    while True:
        Game()
