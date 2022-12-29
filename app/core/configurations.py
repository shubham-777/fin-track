import configparser
import os

package_path, package_filename = os.path.split(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(package_path, "data/config.ini"))


def read_config_from_env(plst_vars):
    ldict_configs = dict()
    for lstr_sec, llst_vars in plst_vars.items():
        for lstr_var in llst_vars:
            if lstr_var in os.environ and lstr_sec == "ENVIRONENT":
                ldict_configs[lstr_var] = os.environ.get(lstr_var)
            else:
                ldict_configs[lstr_var] = config[lstr_sec][lstr_var]
    return ldict_configs


PACKAGE_PATH = package_path

llst_vars = {"ENVIRONENT": ["PSQL_HOSTNAME", "PSQL_PORT", "PSQL_DBNAME", "PSQL_UNAME", "PSQL_PASS"],
             "GENERAL": ['TITLE', 'VERSION', 'DESCRIPTION', 'NAME', 'EMAIL', 'WEB_URL']}
ldict_configs = read_config_from_env(llst_vars)

HOSTNAME = str(ldict_configs["PSQL_HOSTNAME"])
PORT = str(ldict_configs["PSQL_PORT"])
DBNAME = str(ldict_configs["PSQL_DBNAME"])
UNAME = str(ldict_configs["PSQL_UNAME"])
PASS = str(ldict_configs["PSQL_PASS"])

TITLE = str(ldict_configs["TITLE"])
VERSION = str(ldict_configs["VERSION"])
DESCRIPTION = str(ldict_configs["DESCRIPTION"])
NAME = str(ldict_configs["NAME"])
EMAIL = str(ldict_configs["EMAIL"])
WEB_URL = str(ldict_configs["WEB_URL"])
