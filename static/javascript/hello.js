function get_vcode()
{
  var xmlhttp;
  if (window.XMLHttpRequest)
  {
    // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
  }
  else
  {
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  var phonenum = document.getElementById("phonenum").value;//手机号
  if (phonenum)
        if(phonenum.length==11){
          xmlhttp.open("post","./get_vcode",false);
          xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
          xmlhttp.send("phonenum="+phonenum);
          var rsp = xmlhttp.responseText;
          if (rsp=="suc"){
            alert("已发送验证码到" + phonenum + "，10分钟内有效。");
          }
          else if (rsp == "alredy"){
            alert(phonenum + "已注册，请直接登录。");

          }
          // document.getElementById("phonenum").innerHTML=xmlhttp.responseText;
        }
        else {
            alert("请输入正确的手机号");
        }
    else {
        alert("请输入手机号");
    }
}
function reg() {
  var phonenum = document.getElementById("phonenum").value;
  var password = document.getElementById("password").value;
  var vcode = document.getElementById("vcode").value;
  var xmlhttp;
  if (window.XMLHttpRequest)
  {
    // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
  }
  else
  {
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  if(phonenum && password && vcode){
    xmlhttp.open("post","./",false);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("phonenum=" + phonenum + "&password=" + password + "&vcode=" + vcode );
    var rsp = xmlhttp.responseText;
    if (rsp =='suc')
      alert(phonenum + "注册成功！");
    else {
      if(phonenum.length=='11')
      alert(phonenum + "验证码错误！");
      else
      alert(phonenum + "注册失败！");
    }
    }
    else
      alert("请正确填写信息！");
  // body...
}