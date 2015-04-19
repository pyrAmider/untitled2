#!/usr/bin/python
import argparse
import csv
import sys
import os
import pymysql

DATA_DIR = r'C:\Users\Boyd\Downloads\structural-cluster-alignments.v4_0_0\structural-cluster-alignments'
DATABASE_HOST = "localhost"
#DATABASE_HOST = "40.163.0.220"
DATABASE_USER = "lrngsql"
DATABASE_NAME = "bank"
DATABASE_PASSWD = "timexindiglo"
DATABASE_PORT = 3306

select_phenotype_sql = """SELECT account_id, cust_id, avail_balance, product_cd
                          FROM account
                          WHERE avail_balance > ANY (SELECT a.avail_balance
                                                     FROM account a INNER JOIN individual i
                                                       ON a.cust_id = i.cust_id
                                                     WHERE i.fname = 'Frank' AND i.lname = 'Tucker')
                          """

def IsNotNull(value):
    return value is not None and len(value) > 0

#def process_file(infile):


def calculate_columns(errfilename, infilename):
    con = None
    update_con = None

    try:
        print([line for line in open(infilename)])

        errfile = open(errfilename, 'w')
        con = pymysql.connect(host=DATABASE_HOST,user=DATABASE_USER, passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT))
        cursor = con.cursor(pymysql.cursors.DictCursor)

        update_con = pymysql.connect(host=DATABASE_HOST,user=DATABASE_USER, passwd=DATABASE_PASSWD, db=DATABASE_NAME, port=int(DATABASE_PORT))
        update_cursor = update_con.cursor(pymysql.cursors.Cursor)

        # Read current records
        cursor.execute(select_phenotype_sql)

        for row in cursor:
#            account_id = row['account_id']
#            cust_id = row['cust_id']
#            open_date = row['open_date']
#            close_date = row['close_date']
#            last_activity_date = row['last_activity_date']
#            status = row['status']
#            open_branch_id = row['open_branch_id']
#            open_emp_id = row['open_emp_id']
#            avail_balance = row['avail_balance']
#            pending_balance = row['pending_balance']
#            product_cd = row['product_cd']

            print(row)
            L = [row[key] for key in row]
            print(L)
            print(DATA_DIR)

            """
            # calculate crp
            if IsNotNull(row['crp_ng_ml']):
                value = str(float(row['crp_ng_ml'])/1000.0)
                update_phenotype_sql = 'update phenotypes set crp=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            if IsNotNull(row['c_react_prot']):
                value = row['c_react_prot']
                update_phenotype_sql = 'update phenotypes set crp=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            # calculate ldl-c from sui ldl c
            if IsNotNull(row['siu_ldlc_demacker']):
                value = 38.67 * float(row['siu_ldlc_demacker'])
                update_phenotype_sql = 'update phenotypes set ldl_c=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            # calculate cholesterol ratio
            if IsNotNull(row['tsc']) and IsNotNull(row['hdl_c']):
                value = float(row['tsc'])/float(row['hdl_c'])
                update_phenotype_sql = 'update phenotypes set cholesterol_ratio=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            # calculate cholesterol ratio
            if IsNotNull(row['tsc']) and IsNotNull(row['hdl_c_npa']):
                value = float(row['tsc'])/float(row['hdl_c_npa'])
                update_phenotype_sql = 'update phenotypes set cholesterol_ratio_npa=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            # calculate mean arterial pressure
            if IsNotNull(row['diastolic_bp']) and IsNotNull(row['systolic_bp']):
                value = ((2.0/3.0)*float(row['diastolic_bp']))+((1.0/3.0)*float(row['systolic_bp']))
                update_phenotype_sql = 'update phenotypes set mean_arterial_pressure=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            # calculate mean arterial pressure npa
            if IsNotNull(row['diastolic_bp_npa']) and IsNotNull(row['systolic_bp_npa']):
                value = ((2.0/3.0)*float(row['diastolic_bp_npa']))+((1.0/3.0)*float(row['systolic_bp_npa']))
                update_phenotype_sql = 'update phenotypes set mean_arterial_pressure_npa=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

            # calculate homa_ir
            if IsNotNull(row['fasting_glucose']) and IsNotNull(row['fasting_insulin']):
                value = float(row['fasting_glucose'])*float(row['fasting_insulin'])/405.0
                update_phenotype_sql = 'update phenotypes set homa_ir=%s where ego=%s and visit=%s'
                update_cursor.execute(update_phenotype_sql, (value,ego,visit))

        update_con.commit()
"""
    except pymysql.Error as e:
        errfile.write("Error %d: %s" % (e.args[0], e.args[1]))
    except csv.Error as e:
        errfile.write("Error file %s, line %d: %s" %(infile.name, reader.line_num, e))
    finally:
        if con:
            con.close()
        if update_con:
            update_con.close()

    errfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='calculate_columns.py',description='calcucate column values from other column values.')
    parser.add_argument('-e', '--errfilename',
                        help='The error file location.',
                        required=True)
    parser.add_argument('-i', '--infilename',
                        help='The input file location.',
                        required=True)

    args = parser.parse_args()

    calculate_columns(args.errfilename, args.infilename)
    #process_file(args.infile)