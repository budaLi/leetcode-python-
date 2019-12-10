/**
 * Created by lenovo on 2019/12/9.
 */
;/**
 * Created by lenovo on 2019/12/6.
 */
auto.waitFor();
var height = device.height;
var width = device.width;
toast("\n设备宽" + width + "\n" + "设备高" + height + "\n" + "手机型号" + device.model + "\n安卓版本" + device.release)
sleep(2000);
setScreenMetrics(width, height);
toast("设备高" + height);
// test(18);
createFile();


function test(phone) {
    //点击加号
    toast("点击加号");
    click(1004, 161);
    //等待
    sleep(1000);
    toast("点击添加好友");
    //点击添加好友
    click(843, 470);
    sleep(1000);
    //点击微信号栏
    click(580, 291);
    sleep(1000);
    if (id("c4j").exists()) {
        textEndsWith("微信号/手机号").findOne().setText(phone);
    }
    sleep(1000);
    //点击搜索结果中的手机号
    click(540, 317);
    sleep(1000);
    if (textEndsWith("").findOne().exists()) {
        toast("已经是微信好友了");
    }
    else {
        //点击添加到通讯录
        click(540, 1160);
        sleep(1000);
        //点击发送
        textEndsWith("发送").findOne().click();

    }


    // id("b_d").findOne().click();
    toast(phone);
    //找到手机号输入框

}

function createFile() {
    files.create("/sdcard/phone_number.txt/");
    //测试写入文件
    files.write("/sdcard/1.txt", "1");
    files.write("/sdcard/1.txt", "2");
    files.write("/sdcard/1.txt", "3");
    files.write("/sdcard/1.txt", "4");
    files.write("/sdcard/1.txt", "5");

    //文件路径 并打开文本
    var f = open("/sdcard/phone_number.txt/", "r");
    //读取文本全部内容
    text = f.readlines();
    for (var i = 0; i <= text; i++) {
        sleep(1000);
        toast(text[i])
    }
    files.close();
}

