import sys, os
import pandas as pd
from wurfl_cloud import Cloud
from wurfl_cloud import utils
from user_agents import parse
#import MySQLdb
#import config

#check for config file
if len(sys.argv) != 2:
    print "usage: script, config error"
    sys.exit(1)

#my local directory - not used here
dir = """C:\Users\ctaylor\PycharmProjects\Programming\UA""" + os.sep

#load ad server log file
def load_data(numrows = 1000, sample=1, test_flag=True):
    global df
    if test_flag:
        df = pd.read_csv(filepath_or_buffer = "query.csv", nrows = numrows).sample(n = sample)
    else:
        df = pd.read_csv(filepath_or_buffer = "query.csv", nrows = numrows) #select top rows
    return df

#write device information to csv
def write_csv(results):
    for k,v in results.items():
        try:
            print v.head(2)
            v.to_csv(path_or_buf= "{}.csv".format(k), \
                  sep=',', na_rep='', float_format=None, columns=None, header=True, index=True,
                  mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n',
                  doublequote=True, escapechar=None, decimal='.')
        except Exception as e:
            print e.args

#create seperate classes for different mapping methods
class Pyua:

    #instantiate a pyua object based on input dataframe
    def __init__(self, df):
        self.df_p = df
        self.ua_in = self.df_p['user_agent']

    #apply built-in parse functions to individual user agent strings
    def parse_pyua(self):
        try:
            self.df_p['pyua_browser'] = map(lambda x : parse(x).browser.family, self.ua_in)
            self.df_p['pyua_device'] = map(lambda x : parse(x).device.family, self.ua_in)
            self.df_p['pyua_pc'] = map(lambda x : parse(x).is_pc, self.ua_in)
            self.df_p['pyua_mob'] = map(lambda x : parse(x).is_mobile, self.ua_in)
            self.df_p['pyua_tab'] = map(lambda x : parse(x).is_tablet, self.ua_in)
        except Exception as err:
            print "pyua can't parse this string", self.ua_in
            print err
        return self.df_p

#    def write_results(self):
#        cnn = MySQLdb.connect(host=config.DBHOST, user=config.DBUSER, passwd=config.DBPW, db=config.DBNAME)
#        sql = "delete from pyua;" #;".format(table)
#        cursor = cnn.cursor()
#        cursor.execute(sql)
#        print "ready to write to pyua"#.format(table)
#        try:
#            self.df_p.to_sql(name = 'pyua', con = cnn, flavor='mysql', if_exists='append', index=True,
        # index_label=None, chunksize=250, dtype=None)
#        except Exception as e:
#            print e.args

class Wurfl:

    #instantiate a wurfl object based on input dataframe
    def __init__(self, df):
        self.df_w = df
        self.ua_in = self.df_w['user_agent']
        self.config = utils.load_config(sys.argv[1]) #load config and cache files
        self.cache = utils.get_cache(self.config)

    #function that parses individual user agent string
    def parse_str(self, ua_in):
        try:
            #connect to the cloud database
            cloud = Cloud(self.config, self.cache)
            #load basic capabilities
            dev = cloud(ua = ua_in, headers=None, capabilities=["complete_device_name", "is_mobile",
                                                                          "form_factor"])
            if not dev["errors"]:
                #look up device information
                device = dev["capabilities"]["complete_device_name"].encode('utf-8')
                is_mobile = dev["capabilities"]["is_mobile"]
                form = dev["capabilities"]["form_factor"].encode('utf-8')
            else:
                print dev["errors"]
                print dev["errors"].item()
        except LookupError as e:
            print "lookup error", e
        return device, is_mobile, form

    #apply the above function to each user agent string
    def parse_wurfl(self):

        try:
            self.df_w['wurfl_device'] = map(lambda x : self.parse_str(x)[0], self.ua_in)
            self.df_w['wurfl_mob'] = map(lambda x : self.parse_str(x)[1], self.ua_in)
            self.df_w['wurfl_platform'] = map(lambda x : self.parse_str(x)[2], self.ua_in)
            #print self.df_w.head(2)
        except Exception as err:
            print err
            self.df_w['wurfl_device', 'wurfl_mob', 'wurfl_platform'] = None
        return self.df_w

#run the ua string mappers
if __name__ == "__main__":
    results = {
                'wurfl' : Wurfl(load_data(numrows = 300, test_flag=False)).parse_wurfl(),
                'pyua' : Pyua(load_data(numrows = 300, test_flag=False)).parse_pyua()
    }

    write_csv(results)
