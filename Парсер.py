import csv
from connect_db import cur, con
import glob


def read_write():
    # ������� ������� � ������ ���������� �������� ��� ���� ������ csv, ������� OTKLONENIE ��� ��������� ����������
    # �� ��������� �������
    cur.execute('''CREATE TABLE if not exists PLAN_TABLE
         (ID SERIAL PRIMARY KEY NOT NULL,
         PROJECT TEXT NOT NULL,
         LEADER TEXT NOT NULL,
         DATE_PERIOD DATE NOT NULL,
         OTKLONENIE TEXT NULL);'''
                )
    # ������� ������� ����������
    cur.execute('''CREATE TABLE if not exists WORKER
            (ID SERIAL NOT NULL,
            PROJECT TEXT NOT NULL,
            WORKER TEXT NOT NULL,
            WORK_PLAN TEXT NOT NULL,
            PRIMARY KEY(ID));'''
                )
    # ������ ��� ����� � ������ Plan* (Plan1, Plan2, Plan3...)
    for Files in glob.glob("Plan*.csv"):
        with open(Files, 'r', newline='') as File_read:
            reader = list(csv.reader(File_read, delimiter=';'))

            for i in range(1, len(reader)):  # ����� ��������� ������� �� 2 ������� i=1
                # ��������� ����� ������ � ��������� ������� ������
                cur.execute("INSERT INTO PLAN_TABLE ( PROJECT, LEADER, DATE_PERIOD) VALUES ('%s','%s','%s')" % (
                    reader[i][0], reader[i][1], reader[i][2]))
                for k in range(3, len(reader[1])):  # ��������� � ������� WORKER ������� ����� ���������� � ������� ����
                    column = reader[0][k]
                    worker = str(column.replace(' ', '_'))  # �������� ������� � ��������� �������� �� "_"
                    cur.execute("INSERT INTO WORKER (PROJECT, WORKER, WORK_PLAN) VALUES ('%s','%s','%s')" % (
                        reader[i][0], worker, reader[i][k].replace(',', '.')))
                x = 0  # ���������� ��� ��������� ��������������� �����
                y = 0  # ���������� ��� ��������� ����������� �����
                z = '0'  # ���������� ��� �������� ���������� ����������� �����
                for j in range(3, len(reader[1])):  # ��������� ������ � �����-������ ��� ����������� �������
                    row = reader[i][j]
                    if row == "":  # ���������� ������ ������
                        continue
                    row2 = row.replace(',', '.').split('/')  # ��������� ������ �� ������ �� �����
                    x += float(row2[0])
                    y += float(row2[1])
                if x != 0:
                    z = str(round(((y - x) / x * 100), 3)) + "%"  # �������� ������������ ������� ��� ��������
                    # �������� ����������
                row3 = reader[i][0]  # �������� �������
                # ��������� ������������ ���������� ���������� ������� row3 � ��
                cur.execute("UPDATE PLAN_TABLE SET OTKLONENIE = '%s' WHERE PROJECT = '%s'" % (z, row3))



# report() ������� ����� � ������������ ��������
def report():
    # �������� �� �� ������ PROJECT, LEADER, DATE_PERIOD, OTKLONENIE ��������������� �� DATE_PERIOD � �������
    # ������������
    cur.execute("SELECT PROJECT, LEADER, DATE_PERIOD, OTKLONENIE from PLAN_TABLE ORDER BY DATE_PERIOD")
    rows = cur.fetchall()
    with open('Report.csv', 'w', newline='') as File:  # ������� ���� ��� ������
        File_write = csv.writer(File, delimiter=';')
        name = ('�������� �������', '������������', '���� �����', '����������')
        File_write.writerow(name)  # ���������� � ���� �������� ��������
        for row in rows:
            File_write.writerow(row)  # ���������� �� �������� ������ �� ��
    con.commit()
    con.close()
	
read_write()
report()
