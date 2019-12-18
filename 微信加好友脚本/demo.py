# conding:utf-8
from appium import webdriver
from time import sleep

'''
deviceName:通过adb device来获取，84325b42;  127.0.0.1:62001
platformName:操作系统的名字，Android
platformVersion:操作系统的版本，6.0.1;   5.1.1
appPackage:被测试app的包，apk,com.tencent.mobileqq
Activity:被测APP的启动项,activity.LoginActivity
'''

# 通过appium连接手机app，配置caps
caps = {}
# caps['deviceName'] = '127.0.0.1:62001'
caps['deviceName'] = 'HBSBB18830527105'
caps['platformName'] = 'Android'
caps['platformVersion'] = '5.1.1'
caps['appPackage'] = 'com.tencent.mobileqq'
caps['appActivity'] = '.activity.SplashActivity'
caps['unicodeKeyboard'] = True  # 自动化操作中是否需要输入中文，默认false

# 连接appium，访问到app
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
driver.implicitly_wait(20)

# 定位弹出框同意的按钮，并点击
driver.find_element_by_xpath('//android.widget.TextView[@content-desc="同意"]').click()
driver.implicitly_wait(10)

# 定位登录按钮并点击
driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget'
                             '.LinearLayout/android.widget.FrameLayout/android.widget'
                             '.RelativeLayout/android.widget.FrameLayout/android.widget'
                             '.FrameLayout/android.widget.RelativeLayout/android.widget'
                             '.LinearLayout/android.widget.Button[2]').click()
driver.implicitly_wait(10)

# 定位输入账号的输入框，点击一次
driver.find_element_by_xpath('//android.widget.EditText[@content-desc="请输入QQ号码或手机或邮箱"]').click()
driver.implicitly_wait(10)

# 定位输入账号的输入框，输入账号
driver.find_element_by_xpath('//android.widget.EditText[@content-desc="请输入QQ号码或手机或邮箱"]').send_keys('317708313')

# 定位输入密码的输入框，点击一次
driver.find_element_by_xpath('//android.widget.EditText[@content-desc="密码 安全"]').click()
driver.implicitly_wait(10)

# 定位输入账号的输入框，输入密码
driver.find_element_by_xpath('//android.widget.EditText[@content-desc="密码 安全"]').send_keys('cz2017tw')
driver.implicitly_wait(10)

# 定位登录按钮，点击一次
driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="登 录"]').click()
