#!/usr/bin/env python3
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
import json
import oss2
import web

urls = (
    '/.*', 'OssSts'
)
app = web.application(urls, globals())
def get_token():
    access_key_id = '<key>'
    access_key_secret = '<secret>'
    role_arn = 'acs:ram::<id>:role/oss-sts-role'
    policy_text = """{
  "Statement": [
    {
      "Action": [
        "oss:PutObject",
        "oss:ListParts",
        "oss:AbortMultipartUpload",
        "oss:ListObjects"
      ],
      "Effect": "Allow",
      "Resource": ["<resource>"]
    }
  ],
  "Version": "1"
}"""
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    req = AssumeRoleRequest.AssumeRoleRequest()
    req.set_accept_format('json')
    req.set_RoleArn(role_arn)
    req.set_DurationSeconds(900)
    req.set_RoleSessionName('session-name')
    req.set_Policy(policy_text)
    body = clt.do_action_with_exception(req)
    token = json.loads(oss2.to_unicode(body))
    return token

class OssSts:
    def POST(self):
        t=get_token()
        token=self.format_token(t)
        web.header("Access-Control-Allow-Origin", "*")
        return token

    def format_token(self,token):
        new_json={}
        SecurityToken=token['Credentials']['SecurityToken']
        AccessKeyId=token['Credentials']['AccessKeyId']
        AccessKeySecret=token['Credentials']['AccessKeySecret']
        new_json['SecurityToken']=SecurityToken
        new_json['AccessKeyId']=AccessKeyId
        new_json['AccessKeySecret']=AccessKeySecret
        return json.dumps(new_json)
sts_app=app.wsgifunc()
