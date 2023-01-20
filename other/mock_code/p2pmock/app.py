import datetime
import time

from flask import Flask, render_template, jsonify, request
import requests
import pymysql

from utils import DBUtil

app = Flask(__name__)


# 开户
def userRegister():
    # 获取请求参数
    Version = request.form.get("Version")
    CmdId = request.form.get("CmdId")
    MerCustId = request.form.get("MerCustId")
    BgRetUrl = request.form.get("BgRetUrl")
    RetUrl = request.form.get("RetUrl")
    UsrId = request.form.get("UsrId")
    UsrName = request.form.get("UsrName")
    IdType = request.form.get("IdType")
    IdNo = request.form.get("IdNo")
    UsrMp = request.form.get("UsrMp")
    UsrEmail = request.form.get("UsrEmail")
    MerPriv = request.form.get("MerPriv")
    ChkValue = request.form.get("ChkValue")
    CharSet = request.form.get("CharSet")

    # 构造回调请求数据
    # 构造用户账号，格式：6000060011481418
    UsrCustId = "60{}".format(time.strftime("%Y%m%d%H%M%S"))
    print("UsrCustId==========", UsrCustId)
    data = {
        "UsrCustId": UsrCustId,
        "BgRetUrl": BgRetUrl,
        "UsrName": UsrName,
        "IdType": IdType,
        "MerPriv": MerPriv,
        "RetUrl": RetUrl,
        "UsrMp": UsrMp,
        "TrxId": "406544084846401438",
        "UsrId": UsrId,
        "RespCode": "000",
        "RespDesc": "成功",
        "IdNo": IdNo,
        "ChkValue": ChkValue,
        "MerCustId": MerCustId,
        "UsrEmail": UsrEmail,
        "CmdId": CmdId,
    }
    response = requests.post(RetUrl, data=data)
    print("response.txt===", response.text)

    # 保存用户信息到数据库
    conn = DBUtil.get_conn()
    conn.autocommit(True)
    cursor = DBUtil.get_cursor()
    sql = "insert into p2p_account(account, create_time) values (%s, %s)"
    cursor.execute(sql, (UsrCustId, time.strftime("%Y-%m-%d %H:%M:%S")))
    print("new id=====", cursor.lastrowid)
    DBUtil.close_cursor(cursor)
    DBUtil.close_conn()

    return "UserRegister OK"


# 充值
def netSave():
    Version = request.form.get("Version")
    CmdId = request.form.get("CmdId")
    MerCustId = request.form.get("MerCustId")
    UsrCustId = request.form.get("UsrCustId")
    OrdId = request.form.get("OrdId")
    OrdDate = request.form.get("OrdDate")
    GateBusiId = request.form.get("GateBusiId")
    OpenBankId = request.form.get("OpenBankId")
    DcFlag = request.form.get("DcFlag")
    TransAmt = request.form.get("TransAmt")
    RetUrl = request.form.get("RetUrl")
    BgRetUrl = request.form.get("BgRetUrl")
    OpenAcctId = request.form.get("OpenAcctId")
    CertId = request.form.get("CertId")
    MerPriv = request.form.get("MerPriv")
    ChkValue = request.form.get("ChkValue")
    CharSet = request.form.get("CharSet")

    # 修改数据库中的金额
    conn = DBUtil.get_conn()
    conn.autocommit(True)
    cursor = DBUtil.get_cursor()
    sql = "update p2p_account set AvlBal=AvlBal+%s,AcctBal=AcctBal+%s where account=%s"
    cursor.execute(sql, (TransAmt, TransAmt, UsrCustId))
    print("new id=====", cursor.lastrowid)
    DBUtil.close_cursor(cursor)
    DBUtil.close_conn()

    url = RetUrl
    data = {
        "UsrCustId": UsrCustId,
        "SecRespDesc": "",
        "BgRetUrl": BgRetUrl,
        "MerPriv": MerPriv,
        "transExt": "",
        "FeeAcctId": "MDT000001",
        "RespCode": "000",
        "RespDesc": "成功",
        "GateBusiId": "B2C",
        "CashierSysId": "0001092555",
        "OrdDate": OrdDate,
        "MerCustId": MerCustId,
        "OrdId": OrdId,
        "Version": Version,
        "CmdId": CmdId,
        "CardId": "",
        "FeeCustId": "6000060007313892",
        "TransAmt": TransAmt,
        "SubAcctId": "MDT000001",
        "GateBankId": "CIB",
        "SecRespCode": "",
        "RetUrl": RetUrl,
        "TrxId": "202001190001092555",
        "SaveChannel": "MUSER",
        "FeeAmt": "0.00",
        "CashierAcctDate": "20200119",
        "ChkValue": ChkValue,
    }
    response = requests.post(url, data=data)
    print("response.txt===", response.text)

    return "NetSave OK"


# 余额查询
def queryBalanceBg():
    Version = request.form.get("Version")
    CmdId = request.form.get("CmdId")
    MerCustId = request.form.get("MerCustId")
    UsrCustId = request.form.get("UsrCustId")
    RetUrl = request.form.get("RetUrl")
    UsrId = request.form.get("UsrId")
    UsrName = request.form.get("UsrName")
    IdType = request.form.get("IdType")
    IdNo = request.form.get("IdNo")
    UsrMp = request.form.get("UsrMp")
    UsrEmail = request.form.get("UsrEmail")
    MerPriv = request.form.get("MerPriv")
    ChkValue = request.form.get("ChkValue")
    CharSet = request.form.get("CharSet")

    # 查询数据库
    AvlBal, AcctBal, FrzBal = "0.00", "0.00", "0.00"
    sql = "select AvlBal,AcctBal,FrzBal from p2p_account where account='{}'".format(UsrCustId)
    result = DBUtil.get_one(sql)
    print("result=========", result)
    if result:
        AvlBal, AcctBal, FrzBal = result

    data = {
        "MerCustId": MerCustId,
        "CmdId": CmdId,
        "AvlBal": AvlBal,
        "AcctBal": AcctBal,
        "FrzBal": FrzBal,
    }
    return jsonify(data)


def initiativeTender():
    Version = request.form.get("Version")
    CmdId = request.form.get("CmdId")
    MerCustId = request.form.get("MerCustId")
    UsrCustId = request.form.get("UsrCustId")
    OrdId = request.form.get("OrdId")
    OrdDate = request.form.get("OrdDate")
    TransAmt = request.form.get("TransAmt")
    MaxTenderRate = request.form.get("MaxTenderRate")
    BorrowerDetails = request.form.get("BorrowerDetails")
    IsFreeze = request.form.get("IsFreeze")
    FreezeOrdId = request.form.get("FreezeOrdId")
    RetUrl = request.form.get("RetUrl")
    BgRetUrl = request.form.get("BgRetUrl")
    MerPriv = request.form.get("MerPriv")
    ChkValue = request.form.get("ChkValue")
    CharSet = request.form.get("CharSet")
    ReqExt = request.form.get("ReqExt")
    print("RetUrl=====", RetUrl)

    # 修改数据库中的金额
    conn = DBUtil.get_conn()
    conn.autocommit(True)
    cursor = DBUtil.get_cursor()
    sql = "update p2p_account set AvlBal=AvlBal-%s,FrzBal=FrzBal+%s where account=%s"
    cursor.execute(sql, (TransAmt, TransAmt, UsrCustId))
    DBUtil.close_cursor(cursor)
    DBUtil.close_conn()
    print("update db end.....")

    url = RetUrl
    data = {
        "UsrCustId": UsrCustId,
        "BgRetUrl": BgRetUrl,
        "MerPriv": MerPriv,
        "transExt": "",
        "FeeAcctId": "",
        "RespCode": "000",
        "RespDesc": "成功",
        "OrdDate": OrdDate,
        "MerCustId": MerCustId,
        "OrdId": OrdId,
        "Version": Version,
        "CmdId": CmdId,
        "FeeCustId": "",
        "TransAmt": TransAmt,
        "SecRespCode": "",
        "SecRespDesc": "",
        "RetUrl": RetUrl,
        "TrxId": "202001210006220207",
        "FeeAmt": "",
        "ChkValue": ChkValue,
        "FreezeTrxId": "",
        "IsFreeze": "Y",
    }
    print("time1111====", datetime.datetime.now())
    response = requests.post(url, data=data)
    print("time22222====", datetime.datetime.now())
    print("response.txt===", response.text)

    return "InitiativeTender OK"


@app.route("/muser/publicRequests", methods=["GET", "POST"])
def mock():
    print("request param===", request.form)
    CmdId = request.form.get("CmdId")
    # 开户
    if CmdId == "UserRegister":
        return userRegister()
    # 充值
    elif CmdId == "NetSave":
        return netSave()
    # 查询余额
    elif CmdId == "QueryBalanceBg":
        return queryBalanceBg()
    # 主动投标
    elif CmdId == "InitiativeTender":
        return initiativeTender()
    else:
        print("未知操作！！！")
        return "ERROR"


@app.route("/")
def hello():
    return "P2P Mock Server..."


if __name__ == '__main__':
    app.run(debug=True)
