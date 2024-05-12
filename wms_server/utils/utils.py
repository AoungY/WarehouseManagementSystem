from django.conf import settings
import pyodbc

db_con = pyodbc.connect(settings.db_connect_str)

chinese_to_english = {
    "用户名": "username",
    "用户密码": "password",
    "编号": "id",
    "名称": "name",
    "生产地": "origin",
    "存放位置": "storage_location",
    "是否借出": "is_borrowed",
    "卡号": "card_number",
    "刷卡时间": "swipe_time",
    "库存": "inventory"
}
english_to_chinese = {v: k for k, v in chinese_to_english.items()}
"""
表名：用户信息表
字段：用户名，用户密码

表名：刷卡时间
字段：编号、名称、生产地、存放位置、是否借出、卡号、刷卡时间

表名：仓库信息
字段：编号、是否借出、存放位置、生产地、库存、名称、卡号
"""


def fetchone(cursor):
    """
    获取一行并转换为字典
    :param cursor: 游标对象
    :return:
    """
    columns = [chinese_to_english[column[0]] for column in cursor.description]
    _ = cursor.fetchone()
    if _ is None: return None
    row_dict = dict(zip(columns, _))
    return row_dict


def fetchall(cursor):
    """
    获取所有行并转换为字典
    :param cursor: 游标对象
    :return:
    """
    columns = [chinese_to_english[column[0]] for column in cursor.description]
    # 获取所有行并转换为字典
    rows = []
    for row in cursor.fetchall():
        row_dict = dict(zip(columns, row))
        rows.append(row_dict)
    return rows


class SQL:
    def __init__(self):
        self.con = db_con
        self.cursor = self.con.cursor()

    def get_user(self, user_name, password):
        """
        获取用户信息
        :param user_name: 用户名
        :param password: 密码
        :return:
        """
        self.cursor.execute("SELECT * FROM 用户信息表 WHERE 用户名 = ? AND 用户密码 = ?", (user_name, password))
        user = fetchone(self.cursor)
        return user

    def get_card(self, card_number):
        """
        获取卡信息
        :param card_number: 卡号
        :return:
        """
        self.cursor.execute("SELECT * FROM 仓库信息 WHERE 卡号 = ?", (card_number,))
        card = fetchone(self.cursor)
        return card

    def update_card(self, data):
        # 构建更新语句
        update_sql = "UPDATE `仓库信息` SET "
        update_values = []
        for field in data.keys():
            update_sql += f"{english_to_chinese[field]} = ?, "
            update_values.append(data[field])
        # 移除最后一个逗号
        update_sql = update_sql[:-2]
        update_sql += " WHERE 卡号 = ?"
        update_values.append(data['card_number'])
        print(update_sql,update_values)
        # 执行更新操作
        try:
            self.cursor.execute(update_sql, update_values)
            self.con.commit() # 提交事务
            return True
        except Exception as e:
            print(e)
            return False

    def delete_card(self,card_number):
        """
        删除卡信息
        :param card_number: 卡号
        :return:
        """
        self.cursor.execute("DELETE FROM 仓库信息 WHERE 卡号 = ?", (card_number,))
        self.con.commit()
        return True
