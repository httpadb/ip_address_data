import requests
import json
import pytz
import datetime


def get_locales(proxies):
    session = requests.Session()

    if proxies is not None and proxies != "":
        session_proxies = {
            'http': "http://" + proxies,
            'https': "http://" + proxies
        }
        session.proxies = session_proxies

    url = 'http://ip-api.com/json'

    r = session.get(url, verify=False).json()

    country_code = str(r["countryCode"]).upper()
    p = pytz.timezone(r["timezone"])
    tznm = str(r["timezone"]).replace('/', '%2F')
    tzn = str(r["timezone"])

    f = open('mcc_mnc.json', )
    mcc_mnc = json.load(f)

    tz_offset_sec = int(p.utcoffset(datetime.datetime.now()).total_seconds())

    mcc_mnc_list = []
    for x in mcc_mnc:
        if x["ISO"] == str(country_code).lower():
            mcc_mnc_list.append(x)

    mcc_mnc = mcc_mnc_list[0]

    settings = json.dumps({
        "region": country_code,
        "locale": "de",
        "timezone_name": tznm,
        "tz_name": tzn,
        "tz_info": set_tzinf(tzn),
        "tz_offset": tz_offset_sec,
        "timezone": "0",
        "mcc_mnc": str(mcc_mnc["MCC"]) + str(mcc_mnc["MNC"]),
        "carrier_region_v2": str(mcc_mnc["MCC"]),
        "carrier_region": country_code,
        "operator_name": str(mcc_mnc["Network"])
    })

    return settings


def set_tzinf(tn):
    tnn = pytz.timezone(tn)
    tnz = datetime.datetime.now(pytz.timezone(str(tnn))).strftime('%Z')
    tno = datetime.datetime.now(pytz.timezone(str(tnn))).strftime('%z')

    if tno.endswith('00'):
        tno = tno[0:3]
        tno = str(tno) + ':00'

    tzinf = tnz + tno
    return tzinf