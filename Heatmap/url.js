var g_http = null;

// XMLHttpRequest 객체생성
function getXMLHttpRequest()
{
    if(window.ActiveXObject)
    {
        try
        {
            // IE 상위버전
            return new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch(e1)
        {
            try
            {
                // IE 하위버전
                return new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch(e2)
            {
                return null;
            }
        }
    }
    else if(window.XMLHttpRequest)
    {
        // 기타 브라우저
        return new XMLHttpRequest();
    }
    else
        return null;
}

// GET방식으로 url 호출
function goGetURL(url, param)
{
    //var url = "http://xxxxxx/get_page.asp";
    //var param = "?param1=1111&param2=2222";

    g_http = getXMLHttpRequest();
    g_http.onreadystatechange = callbackGet;
    g_http.open("GET", url + param, true);
    g_http.send(null);
}

// POST방식으로 url 호출
function goPostURL(url, param)
{
    //var url = "http://xxxxx/post_page.asp";
    //var param = "param1=1111&param2=2222";

    g_http = getXMLHttpRequest();
    g_http.onreadystatechange = callbackPost;
    g_http.open("POST", url, true);
    g_http.send(param);
}

function callbackGet()  // callbackPost()도 동일
{
    if(g_http.readyState == 4 && g_http.status == 200)
    {
        var result = g_http.responseText;
        alert(result);
    }
}

