from xmind2testlink.sharedparser import xmind_to_dict
from xmind2testlink.main import xmind_to_testlink
import json

## xmind文件地址
xmindFilename = r"C:/Users/mawei/Desktop/xmind/xmind2testlink-S-master_new/web/uploads/test3.xmind"
## testlink xml 文件地址
#testlinkXmlFilename = r"D:\DSXQ-615-CRM保险理赔需求测试用例-why.xls.xml"

## xmind文件转dict
#data = xmind_to_dict(xmindFilename)

## dict转json，然后打印出来
#print(json.dumps(data))

## 将xml文件转dict

file_out = xmind_to_testlink(xmindFilename)
print(file_out)