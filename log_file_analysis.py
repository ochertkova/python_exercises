#!/usr/bin/env python3
import sys
import os
import re
import csv
import operator

#log_text = "May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (msmith) \nJune 1 11:06:48 ubuntu.local ticky: ERROR: Connection to DB failed (jdoe)\n May 30 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (jdoe)\n June 3 11:06:48 ubuntu.local ticky: ERROR: Connection to DB failed (msmith)\n June 1 11:06:48 ubuntu.local ticky: ERROR: Unexpected timeout (jdoe)"
err_dict = {}
user_dict = {}
#print(log_text)
#with open ("project_log_test.txt","w") as file:
 #   file.write(log_text)

log_file = "project_log_test_big.txt"
error_text = "ERROR.*(?=\()"
info_text = "INFO.*(?=\()"

def error_search(log_file):
  returned_errors = []
  with open(log_file, mode='r',encoding='UTF-8') as file:
    for log in file.readlines():
      #print(log)
      #error_pattern = "ERROR.*(?=\()"
      #reg_find = re.search(error_pattern, log)
      error_pattern = re.search(error_text, log)
      
      if error_pattern:
        returned_errors.append(error_pattern.group(0).strip())
 
    file.close()
  return returned_errors


def count_err(errors):
    i = 0
    dict_errors = {}
    for error in errors:
        if error not in dict_errors:
            dict_errors[error] = 0
            #print("Initial adding error")
        dict_errors[error] += 1
        #print("Adding error")
    dict_errors_sort = sorted(dict_errors.items(),key=operator.itemgetter(1),reverse = True)
    print(dict_errors_sort)
    return dict_errors_sort


def user_search(log_file):
    
    dict_list = []
    with open(log_file, mode='r',encoding='UTF-8') as file:
        for log in file.readlines():
            #print(log)
            user_pattern =  re.search(r"\((\w*)\)", log)
            #print(user_pattern.group(1))
            error_pattern = re.search(error_text, log)
            info_pattern = re.search(info_text, log)
            i = 0
            if user_pattern:   
                user_name = user_pattern.group(1)
                if user_name not in [u["Username"] for u in dict_list if "Username" in u]: #Initialize the first entry for unique username
                    dict_users = {}
                    dict_users["Username"] = user_name
                    dict_users["INFO"] = 0
                    dict_users["ERROR"] = 0
                    
                    if error_pattern:
                        dict_users["ERROR"] = 1
                        
                    if info_pattern:
                        dict_users["INFO"] = 1

                    dict_list.append(dict_users)
                    #print("Initial adding user")

                else:
                    #print("Adding info errors")
                    for i in dict_list:
                        if user_name == i["Username"]:
                            if error_pattern:
                                i["ERROR"] += 1
                            if info_pattern:
                                i["INFO"] += 1
                    
            #print(dict_list)   

    return dict_list

def gen_user_report(dict_list):

    with open("user_report.csv","w") as users_csv:
        fieldnames = ["Username", "INFO", "ERROR"]
        writer = csv.DictWriter(users_csv, fieldnames = fieldnames)
        writer.writeheader()
        #user_list = list(dict_users.keys())
        s_users = sorted(dict_list, key=lambda d: d['Username'])
        for row in s_users:
            writer.writerow(row)
    return users_csv

def gen_error_report(dict_errors):
    with open("error_report.csv","w") as errors_csv:
        writer = csv.writer(errors_csv, delimiter = ' ')
        writer.writerow(['Error', 'Count'])
        #error_list = list(dict_errors.items())
        s_errors = sorted(dict_errors,key = operator.itemgetter(1), reverse = True)
        for row in s_errors:
            writer.writerow(row)
    return errors_csv






#print(error_search(log_file))
errors = error_search(log_file)
#print(count_err(errors))
#print(user_search(log_file))
users = user_search(log_file)
c_errors = count_err(errors)
#print(gen_user_report(users))
print(gen_error_report(c_errors))
