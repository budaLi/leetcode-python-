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
main();
toast("脚本结束！！！");

function main() {
    lis = createFile();
    //toast(lis);
    for (var i = 0; i <= lis.length; i++) {
        if (lis[i] != " ") {
            toast(lis[i]);
            test(lis[i]);
        }
    }
}


function test(phone) {
    //点击加号
    //toast("点击加号");
    //click(1004,161);
    //等待
    //sleep(1000);
    //toast("点击添加好友");
    //点击添加好友
    //click(843,470);
    //sleep(1000);
    //点击微信号栏
    //sleep(2000);
    //click(580,291);
    sleep(2000);
    //if(id("c4j"). exists()){
    textEndsWith("微信号/手机号").findOne().setText(phone);
    //}
    sleep(2000);
    //点击搜索结果中的手机号
    click(540, 317);
    sleep(2000);
    if (textEndsWith("发消息").exists()) {
        toast("已经是微信好友了");
        sleep(2000);
        back();
        id("m3").findOne().click();
        sleep(2000);
    }
    else {
        //点击添加到通讯录
        click(540, 1160);
        sleep(2000);
        //点击发送
        //textEndsWith("发送").findOne().click();
        toast("已发送好友申请");
        sleep(2000);
        back();
        sleep(2000);
        id("m3").findOne().click();
        //back();

    }



    // id("b_d").findOne().click();
    //toast(phone);
    //找到手机号输入框

}

function createFile() {
    //toast(files.create("/sdcard/脚本/phone_numbers.txt"));
    //测试写入文件
    //files.write("/sdcard/phone_numbers.txt",1);
    // files.write("/sdcard/phone_numbers.txt",1);
    //files.write("/sdcard/phone_numbers.txt",1);


    //文件路径 并打开文本
    var f = open("/sdcard/脚本/phone_numbers.txt", "r");
    //读取文本全部内容
    text = f.readlines();
    //for(var i=0;i<=text.length;i++){
    // sleep(2000);
    //  toast(text[i]);
    //  }
    return text;


}