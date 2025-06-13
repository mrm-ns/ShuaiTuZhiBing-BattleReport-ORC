import sqlite3
from datetime import datetime

def create_teamdic(report):
    team_dic = {
        "玩家名": report.player,
        "队伍类型": report.team_type,
        "大营": report.characters[0],
        "大营战法1": report.tactics[0],
        "大营战法2": report.tactics[1],
        "中军": report.characters[1],
        "中军战法1": report.tactics[2],
        "中军战法2": report.tactics[3],
        "前锋": report.characters[2],
        "前锋战法1": report.tactics[4],
        "前锋战法2": report.tactics[5]
    }

    return team_dic


def create_database_and_table(database, table):
    """创建数据库和表结构（使用中文字段名）"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    # 创建队伍信息表（全部使用中文字段名）
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table} (
        编号 INTEGER PRIMARY KEY AUTOINCREMENT,
        玩家名 TEXT NOT NULL,
        队伍类型 TEXT NOT NULL,
        大营 TEXT NOT NULL,
        大营战法1 TEXT NOT NULL,
        大营战法2 TEXT NOT NULL,
        中军 TEXT NOT NULL,
        中军战法1 TEXT NOT NULL,
        中军战法2 TEXT NOT NULL,
        前锋 TEXT NOT NULL,
        前锋战法1 TEXT NOT NULL,
        前锋战法2 TEXT NOT NULL,
        添加时间 TIMESTAMP DEFAULT (datetime('now', 'localtime'))
    )
    ''')
    conn.commit()
    conn.close()

def add_team_data(team_info, database, table):
    """添加队伍数据到数据库（带去重机制）"""
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    # 1. 检查重复数据（排除自增ID和时间戳字段）
    cursor.execute(f'''
    SELECT COUNT(*) FROM {table}
    WHERE 
        玩家名 = ? AND 队伍类型 = ? AND
        大营 = ? AND 大营战法1 = ? AND 大营战法2 = ? AND
        中军 = ? AND 中军战法1 = ? AND 中军战法2 = ? AND
        前锋 = ? AND 前锋战法1 = ? AND 前锋战法2 = ?
    ''', (
        team_info['玩家名'],
        team_info['队伍类型'],
        team_info['大营'],
        team_info['大营战法1'],
        team_info['大营战法2'],
        team_info['中军'],
        team_info['中军战法1'],
        team_info['中军战法2'],
        team_info['前锋'],
        team_info['前锋战法1'],
        team_info['前锋战法2']
    ))
    
    # 2. 存在重复则跳过插入
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False
    
    # 3. 无重复则执行插入
    cursor.execute(f'''
    INSERT INTO {table} (
        玩家名, 队伍类型, 
        大营, 大营战法1, 大营战法2,
        中军, 中军战法1, 中军战法2,
        前锋, 前锋战法1, 前锋战法2
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        team_info['玩家名'],
        team_info['队伍类型'],
        team_info['大营'],
        team_info['大营战法1'],
        team_info['大营战法2'],
        team_info['中军'],
        team_info['中军战法1'],
        team_info['中军战法2'],
        team_info['前锋'],
        team_info['前锋战法1'],
        team_info['前锋战法2']
    ))
    
    conn.commit()
    conn.close()
    return True