/**
 * Created by lenovo on 2019/12/6.
 */
auto.waitFor();
var height = device.height;
var width = device.width;
toast("\n设备宽" + width + "\n" + "设备高" + height + "\n" + "手机型号" + device.model + "\n安卓版本" + device.release)
setScreenMetrics(width, height);
toast("设备高" + height);
autoplay();

function autoplay() {
    if (textEndsWith("签到").exists()) {
        textEndsWith("签到").findOne().click();
        sleep(1600);
        toast("签到成功")
    }
    sleep(2000);
    toast("完成[签到]检测");

    while (textEndsWith("去浏览").exists()) {
        //要支持的动作
        toast("存在去浏览");
        textEndsWith("去浏览").findOne().click();
        sleep(1500);
        swipe(width / 2, height - 500, width / 2, 0, 500);
        sleep(2500);
        swipe(width / 2, height - 500, width / 2, 0, 500);
        sleep(10000);
        swipe(width / 2, height - 500, width / 2, 0, 500);
        sleep(8000);
        back();
        sleep(1600);
    }
    toast("完成[去浏览]检测");
    sleep(2000);
    toast("结束");

}