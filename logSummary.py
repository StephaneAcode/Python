#!/usr/bin/env python
# coding: utf-8

import re
# WARNING, don't use the argparse module because it isn't supported by the Harman platforms !!!
# Keep the deprecated OptionParser instead as below:
from optparse import OptionParser
import os
import sys

parser = OptionParser()
parser.add_option("-l",                      dest="logPrefix",  help="read data from <logPrefix>*.log")
parser.add_option("-a", action="store_true", dest="printAll",   help="Print all tests (OK and NOK).")
parser.add_option("-v", action="store_true", dest="verbose",    help="Print NOK details.")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
(myArgs, args) = parser.parse_args()


#fileList = subprocess.check_output(["ls"])
#fileListArray = subprocess.check_output(["ls"]).splitlines()

#logFileList = re.findall(myArgs.logPrefix, subprocess.check_output(["ls"]))
logFileList = [filename for filename in os.listdir(os.path.join(os.path.dirname(myArgs.logPrefix), ".")) if (filename.startswith(os.path.basename(myArgs.logPrefix)) and filename.endswith(".log"))]


NOK_dataAndTune=0
NOK_test=0
NOT_run=0
Total_test=0
first_line=0
data_base={}
flag_base={}
test_name=""
std_name=""
scenario_nb=0
loop_cnt=0
validation_ver="NA"
driver_ver="NA"
hal_ver="NA"


print "OK+NOK" if myArgs.printAll else "NOK", ; print "test detail:"

########################################################
# 
# Parse each log file found in logFileList
# 
########################################################
for logfile in logFileList:
    print "reading %s ..." % os.path.join(os.path.dirname(myArgs.logPrefix), logfile)
    NOK_dataAndTune=0
    NOK_test=0
    NOT_run = 0
    Total_test = 0
    std_name = "NAstd"
    test_name = "NAtest"
    data_base[std_name] = {}
    data_base[std_name][test_name] = {}
    data_base[std_name][test_name][scenario_nb] = 1
    data_base[std_name][test_name]["count"] = 0
    data_base[std_name][test_name]["err_count"] = 0
    data_base[std_name][test_name]["loop_cnt"] = 0
    data_base[std_name][test_name]["max_received"] = 0
    data_base[std_name][test_name]["min_received"] = 10000000
    data_base[std_name][test_name]["err_count"] = 0
    #data_base[std_name]["tot_count"] = 1

    for line in open(os.path.join(os.path.dirname(myArgs.logPrefix), logfile)):
        line=line.rstrip(os.linesep)
        
        #Store the first line of the log file.
        if not first_line               : first_line = line
        if re.search("\-(.*BT2*|DAB|CMMB|CTTB|(1|3)SEG)\-", line): test_info  = line

        m = re.search("Validation <tag>-g<SHA1short>: (\S+)", line)
        if m:
            validation_ver = m.group(1).rstrip()
    
        m = re.search("Driver ver: (.*)", line)
        if m:
            driver_ver = m.group(1).rstrip()
    
        m = re.search("HAL version: (\S+)", line)
        if m:
            hal_ver = m.group(1)
    
        ########################################################
        # 
        # mx pattern matching result to look for all the test executed.
        # 
        ########################################################
        #For : "{ HotPlug 1-0 -DVBT- .*"
        #For : "{ HotPlug 14 -DVBT- .*"
        #For : "{ HotPlug -DVBT- .*"
        m1 = re.search(r"{\s+(\w+)\s+((\d+)\-\d+\s+|\d+\s+|)\-(\w+)\-", line)
        if m1:
            #print "-D- matched %s" % line
            if m1.group(3):
                test_name   = m1.group(1) + "_" + m1.group(3)
                scenario_nb = int(m1.group(3))
            else:
                test_name   = m1.group(1) + "_0"
                scenario_nb = 0
            std_name    = m1.group(4)
            loop_flag = 1

        #For : "{ TestName SCnb-FEcfg -STANDARD- .*- STANDARD) .*- STANDARD)
        #Ex. : "{ BackGround 1-0 -DVBT2- Master: 1 (FE 0+4 - DVBT2) BackGnd 2 (FE 8 - DVBT2)
        m2 = re.search(r"{\s+(\w+)\s+(\d+)\-\d+\s+\-(\w+)\-.*\- (.*BT2*)\).*\- (.*BT2*)\)", line)
        if m2:
            test_name   = m2.group(1) + "_" + m2.group(2)
            scenario_nb = int(m2.group(2))
            std_name    = m2.group(3)
            std_nameM   = m2.group(4)
            std_nameS   = m2.group(5)
            if ((std_nameM != std_nameS) and (re.search("DVB", std_nameM)) and (re.search("DVB", std_nameS))):
                std_name = "DVBTT2"
            loop_flag = 1

        ########################################################
        # 
        # Initialize the data_base dictionnary.
        # 
        ########################################################
        if m1 or m2:
            if std_name not in data_base:
                data_base[std_name] = {}
            if test_name not in data_base[std_name]:
                data_base[std_name][test_name] = {}
            if scenario_nb not in data_base[std_name][test_name]:
                data_base[std_name][test_name][scenario_nb] = 1
            data_base[std_name][test_name]["count"] = data_base[std_name][test_name].get("count", 0) + 1
            if "err_count" not in data_base[std_name][test_name]:
                data_base[std_name][test_name]["err_count"] = 0
            if "loop_cnt" not in data_base[std_name][test_name]:
                data_base[std_name][test_name]["loop_cnt"] = 0
            if "max_received" not in data_base[std_name][test_name]:
                data_base[std_name][test_name]["max_received"] = 0
            if "min_received" not in data_base[std_name][test_name]:
                data_base[std_name][test_name]["min_received"] = 10000000
            #print "%s %s %d -- %s" % (std_name, test_name, scenario_nb, data_base[std_name][test_name]["count"])
    
        ########################################################
        # 
        # Look for the little loop count for each test.
        # 
        ########################################################
        m = re.search(r"^\<LOOP (\d+)\>", line)
        if m:
            loop_loc = int(m.group(1)) + 1
            #Line below because the loop_flag is already set to 1 at the begining of each test.
            if ( loop_loc > 0 ): loop_flag = 1
            if data_base[std_name][test_name]["loop_cnt"] < loop_loc:
                data_base[std_name][test_name]["loop_cnt"] = loop_loc

        m = re.search(r"Stream (2|3)\s+(on FE|).*\s*=\>\s+OK\s+Received:\s+(\d+)\s+\(Err: 0\)", line)
        if m:
            received = int(m.group(3))
            #print "-D- %s %s received : %d " % ( std_name, test_name, received )
            if data_base[std_name][test_name]["max_received"] < received:
                data_base[std_name][test_name]["max_received"] = received
            if data_base[std_name][test_name]["min_received"] > received:
                data_base[std_name][test_name]["min_received"] = received


        ########################################################
        # 
        # Increase the error count for each test for each NOK seen in the log.
        # Limit the error count to one error per loop to limit the error rate to 100%.
        # 
        ########################################################
        if re.search("[^:] NOK", line):
            NOK_dataAndTune += 1
            if loop_flag == 1:
                loop_flag = 0
                data_base[std_name][test_name]["err_count"] += 1
            if myArgs.verbose:
                test_info += "\n        " + line
    
        m = re.search("Status: (\w+)", line)
        if m:
            test_status = m.group(1)
            if test_name == "NAtest":
                test_info = ">> NAtest << " + test_info
            if test_status == "NOK":
                NOK_test += 1
                print "NOK " + test_info
                #data_base[std_name][test_name]["err_count"] += 1
            elif myArgs.printAll :
                print "    " + test_info
    
        ########################################################
        # 
        # Look for the test end (after the each test summary).
        # 
        ########################################################
        if re.search("} Status=", line): NOT_run +=1
        if re.search("} Status" , line):
            Total_test +=1
            if test_name == "NAtest":
                data_base[std_name][test_name]["count"] = data_base[std_name][test_name].get("count", 0) + 1

        ########################################################
        # 
        # Look for the test date and duration.
        # 
        ########################################################
        m = re.search("^Test duration\s+: (\d+)h(\d+):(\d+)", line)
        if m:
            if "duration" not in data_base[std_name][test_name]:
                data_base[std_name][test_name]["duration"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            else:
                data_base[std_name][test_name]["duration"] += int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            std_name = "NAstd"
            test_name = "NAtest"
            #print "-D- Duration %d" % ( data_base[std_name][test_name]["duration"] )
            #print "-D- Duration %02dh%02d:%02d" % ( int(m.group(1)), int(m.group(2)), int(m.group(3)) )
            
        ########################################################
        # 
        # Look for "watchdog exit" in case the test crashed
        # 
        ########################################################
        m = re.search("Watchdog exit", line)
        if m:
            if "watchdog" not in data_base[std_name][test_name]:
                data_base[std_name][test_name]["watchdog"] = "*"
            std_name = "NAstd"
            test_name = "NAtest"
            


    #print "%s %s %d -- %s/%s" % (std_name, test_name, scenario_nb, data_base[std_name][test_name]["err_count"], data_base[std_name][test_name]["count"])

    print "======================================"
    print first_line
    print "NOK data&tune : %4d" % NOK_dataAndTune
    print "NOK     tests : %4d" % NOK_test
    print "Not run tests : %4d" % NOT_run
    print "Total   tests : %4d\n" % Total_test

########################################################
# 
# Remove the NAstd and NAtest if it is empty
# 
########################################################
if data_base["NAstd"]["NAtest"]["count"] == 0:
    data_base.pop('NAstd', None)

########################################################
# 
# Print the summary
# 
########################################################
print "Reports used : %s ..." % myArgs.logPrefix
print "Validation ver: %s, Driver ver: %s, HAL version: %s" % (validation_ver, driver_ver, hal_ver)
#print "Loop_cnt : " + str(data_base[std_name][test_name]["loop_cnt"])
sep_length = 22 + len(data_base)*16
print "=" * sep_length
print "  Test_&_Scenario        ",
for std_name_iter in data_base.iterkeys():
    print "%-15s" % std_name_iter,
print ""
print "                     ",
for std_name_iter in data_base.iterkeys():
    print "nok / all      ",
print ""
print "-" * sep_length

all_tests_list=[]
for std_name_iter in data_base.iterkeys():
    all_tests_list.extend(data_base[std_name_iter].keys())
all_tests_list = sorted(set(all_tests_list))

########################################################
# 
# Print the NOK and OK status of all test
# 
########################################################
for test_name_iter in all_tests_list:
    print "%17s  " % test_name_iter,
    for std_name_iter in data_base.iterkeys():
        if "tot_err_count" not in data_base[std_name_iter]:
            data_base[std_name_iter]["tot_err_count"] = 0
        if "tot_count" not in data_base[std_name_iter]:
            data_base[std_name_iter]["tot_count"] = 0
        if test_name_iter not in data_base[std_name_iter]:
            data_base[std_name_iter][test_name_iter] = {}
        else:
            data_base[std_name_iter][test_name_iter]["count"] = data_base[std_name_iter][test_name_iter]["count"] * 1
        print "%1s%4s /%3s*%-4s" % ( data_base[std_name_iter][test_name_iter].get("watchdog", " "), data_base[std_name_iter][test_name_iter].get("err_count", "-") , data_base[std_name_iter][test_name_iter].get("count", "-"), data_base[std_name_iter][test_name_iter].get("loop_cnt", "-") ),
        if "watchdog" in data_base[std_name_iter][test_name_iter]:
            data_base[std_name_iter]["tot_watchdog"] = "*"
            flag_base["crash_info"] = "*: crash"
        if "err_count" in data_base[std_name_iter][test_name_iter]:
            data_base[std_name_iter]["tot_err_count"] += int(data_base[std_name_iter][test_name_iter]["err_count"])
        if "count" in data_base[std_name_iter][test_name_iter]:
            data_base[std_name_iter]["tot_count"] += ( int(data_base[std_name_iter][test_name_iter]["count"]) * data_base[std_name_iter][test_name_iter]["loop_cnt"] )

    print ""
print "-" * sep_length
print "            Total  ",
for std_name_iter in data_base.iterkeys():
    print "%1s%4s / %-5s  " % (data_base[std_name_iter].get("tot_watchdog", " "), data_base[std_name_iter]["tot_err_count"], data_base[std_name_iter]["tot_count"]),
print ""
print "%8s               " % (flag_base.get("crash_info", "        ")) ,
for std_name_iter in data_base.iterkeys():
    if data_base[std_name_iter]["tot_count"] != 0:
        print "%5.2f %%        " % ( ( data_base[std_name_iter]["tot_err_count"] * 1.0 ) / data_base[std_name_iter]["tot_count"] * 100 ),
    else:
        print "%5s %%        " % ( "NA" ),
print ""

########################################################
# 
# Print the duration information for all tests.
# 
########################################################
print "=" * sep_length
print "         Duration        "
print "-" * sep_length
for test_name_iter in all_tests_list:
    print "%17s     " % test_name_iter,
    for std_name_iter in data_base.iterkeys():
        if "tot_duration" not in data_base[std_name_iter]:
            data_base[std_name_iter]["tot_duration"] = 0
        if "duration" in data_base[std_name_iter][test_name_iter]:
            data_base[std_name_iter]["tot_duration"] += data_base[std_name_iter][test_name_iter]["duration"]
            print "%2dh%02d:%02d       " % ( data_base[std_name_iter][test_name_iter]["duration"] / 3600 , data_base[std_name_iter][test_name_iter]["duration"] % 3600 / 60 , data_base[std_name_iter][test_name_iter]["duration"] % 60 ),
        else:
            print "--h--:--       " ,
    print ""
        
print "-" * sep_length
print "            Total     ",
for std_name_iter in data_base.iterkeys():
    print "%2dh%02d:%02d       " % ( data_base[std_name_iter]["tot_duration"] / 3600 , data_base[std_name_iter]["tot_duration"] % 3600 / 60 , data_base[std_name_iter]["tot_duration"] % 60 ),

print ""
print "=" * sep_length

########################################################
# 
# Print the bitrate information for TwoStream_1 and BackGround_5 . !!! Beta !!!
# 
########################################################
if (("TwoStream_1" in all_tests_list) or ("TwoStreamMplp_1" in all_tests_list)):
    print "TwoStream(Mplp)_1 TS util data check:"
    print "      Max MBits/s      ",
    for std_name_iter in data_base.iterkeys():
        if std_name_iter == "DVBT2":
            if "max_received" in data_base["DVBT2"].get("TwoStreamMplp_1",[]):
                if "TwoStream_1" not in data_base[std_name_iter]:
                    data_base[std_name_iter]["TwoStream_1"] = {}
                if "max_received" not in data_base[std_name_iter]["TwoStream_1"]:
                    data_base["DVBT2"]["TwoStream_1"]["max_received"] = data_base["DVBT2"]["TwoStreamMplp_1"]["max_received"] * 2
                    data_base["DVBT2"]["TwoStream_1"]["min_received"] = data_base["DVBT2"]["TwoStreamMplp_1"]["min_received"] * 2
        if "max_received" not in data_base[std_name_iter]["TwoStream_1"]:
            data_base[std_name_iter]["TwoStream_1"]["max_received"] = "-"
            data_base[std_name_iter]["TwoStream_1"]["min_received"] = "-"
            print "   -           ",
        else:
            print "%4.1f           " % ( data_base[std_name_iter]["TwoStream_1"]["max_received"] * 188 * 8 / 2.0 / 1e6  ),
    print ""
    print "Max TS p received  ",
    for std_name_iter in data_base.iterkeys():
        print "%8s       " % ( data_base[std_name_iter]["TwoStream_1"]["max_received"] ),
    print ""
    print "Min TS p received  ",
    for std_name_iter in data_base.iterkeys():
        print "%8s       " % ( data_base[std_name_iter]["TwoStream_1"]["min_received"] ),
    print ""
    print "=" * sep_length

if ("BackGround_5" in all_tests_list) :
    print "     BackGround_5 TS util data check:"
    print "      Max MBits/s      ",
    for std_name_iter in data_base.iterkeys():
        if "max_received" not in data_base[std_name_iter]["BackGround_5"]:
            data_base[std_name_iter]["BackGround_5"]["max_received"] = "-"
            data_base[std_name_iter]["BackGround_5"]["min_received"] = "-"
            print "   -           ",
        else:
            print "%4.1f           " % ( data_base[std_name_iter]["BackGround_5"]["max_received"] * 188 * 8 * 2 / 2.0 / 1e6  ),
    print ""
    print "Max TS p received  ",
    for std_name_iter in data_base.iterkeys():
        print "%8s       " % ( data_base[std_name_iter]["BackGround_5"]["max_received"] ),
    print ""
    print "Min TS p received  ",
    for std_name_iter in data_base.iterkeys():
        print "%8s       " % ( data_base[std_name_iter]["BackGround_5"]["min_received"] ),
    print ""
    print "=" * sep_length

