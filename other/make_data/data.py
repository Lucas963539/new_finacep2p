import time
import traceback
import uuid

from utils import DBUtil


# 数据准备
def init_data():
    conn, cursor = None, None
    try:
        conn = DBUtil.get_conn(DBUtil.DB_FINANCE)
        cursor = conn.cursor()

        # 基本信息
        member_id = 303
        member_name = "13012340000"

        # 借款标主表
        sql = """
        INSERT INTO `fn_loan` (`ind`, `serialno`, `name`, `member_id`, `member_name`, `amount`, `credited_amount`, 
        `progress`, `tender_count`, `category_id`, `category_type`, `repay_type`, `period`, `apr`, `sort_index`, 
        `sort_top`, `status`, `hidden_status`, `additional_status`, `deposit_certificate`, `certificate_file_id`, 
        `loan_repay_status`, `loan_repay_time`, `overdue_time`, `add_date`, `add_time`, `verify_time`, `reverify_time`, 
        `add_ip`, `vouch_company_id`, `op_status`, `marker_type`) 
        VALUES (%s, %s, %s, %s, %s, %s, 0.00, 
        0.00, 0, 1, '1', 5, %s, %s, 1, 
        NULL, 3, 1, -1, -1, NULL, 
        NULL, NULL, 1584064625, %s, %s, %s, NULL, 
        2071691736, 0, -1, 'test...');
        """
        ind = str(uuid.uuid1()).replace("-", "")  # 借款订单号系统生成唯一32位
        serialno = 202002250001  # 借款标编号
        name = "sql借款02"
        amount = 1000
        period = 60  # 借款期限
        apr = 3.00  # 借款年利率
        add_date = time.strftime("%Y-%m-%d")
        add_time = int(time.time())
        verify_time = int(time.time())
        cursor.execute(sql, (ind, serialno, name, member_id, member_name, amount, period, apr, add_date, add_time, verify_time))

        loan_id = cursor.lastrowid
        print("loan_id=", loan_id)

        # 借款标明细表
        sql = """
        INSERT INTO `fn_loan_info` (`loan_id`, `thumbs`, `contents`, `attachment_ids`, `password`, `use`, 
        `tender_amount_min`, `tender_amount_max`, `freeze_amount`, `freeze_amount_proportion`, `freeze_period`, 
        `award_status`, `fail_award_status`, `award_amount`, `award_proportion`, `award_amount_total`, 
        `validate`, `part_status`, `tender_count`, `comment_status`, `comment_count`, `is_company`, 
        `company_name`, `vouch_company_info`, `vouch_company_pic`, `vouch_company_guaranty`, `amount_category_id`, 
        `hits`, `cancel_admin_id`, `cancel_remark`, `cancel_time`, `verify_admin_id`, `verify_admin_name`, 
        `verify_remark`, `verify_time`, `verify_ip`, `reverify_admin_id`, `reverify_admin_name`, `reverify_remark`, 
        `reverify_time`, `reverify_ip`, `auto_scale`, `is_auto`, `additional_status`, `additional_apr`, 
        `additional_name`, `additional_amount_max`, `additional_pic`, `product_process`, `information`) 
        VALUES (%s, NULL, %s, 'a:0:{}', NULL, 10105, %s, %s, NULL, 10.00, NULL, -1, -1, 
        NULL, NULL, NULL, %s, NULL, 0, -1, 0, -1, NULL, NULL, NULL, NULL, 1, 1, NULL, NULL, NULL, 1, 'diyou', 
        '初审通过', %s, 2071691736, NULL, NULL, NULL, NULL, NULL, NULL, 1, -1, 0.000000, NULL, 0.000000, 
        NULL, NULL, NULL);
        """
        contents = "借款详细信息..."
        tender_amount_min = 50  # 最小投资金额
        tender_amount_max = 100  # 最大投资金额
        validate = 30  # 借款标有效期限，筹标期限（单位天）
        verify_time = int(time.time())  # 初审时间
        cursor.execute(sql, (loan_id, contents, tender_amount_min, tender_amount_max, validate, verify_time))

        # 借款额度表
        # 修改冻结信用额度
        sql = "update fn_loan_amount set credit_amount_freeze=credit_amount_freeze+%s where member_name=%s"
        cursor.execute(sql, (amount, member_name))

        # 额度变化日志表
        # 添加借款冻结记录
        sql = """
        INSERT INTO `fn_loan_amount_log` (`member_id`, `member_name`, `category_id`, `type`, `amount`, `remark`, 
        `add_time`) VALUES (%s, %s, 1, 4, %s, '借款冻结', %s);
        """
        add_time = int(time.time())
        cursor.execute(sql, (member_id, member_name, amount, add_time))

        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        traceback.print_exc()
    finally:
        DBUtil.close(cursor, conn)


if __name__ == '__main__':
    init_data()










# 数据清理
def clear_data():
    pass
