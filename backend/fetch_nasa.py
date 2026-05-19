import requests
import pandas as pd

DISTRICTS = {
    "Pune":           {"lat": 18.5204, "lon": 73.8567},
    "Nashik":         {"lat": 20.0059, "lon": 73.7898},
    "Solapur":        {"lat": 17.6599, "lon": 75.9064},
    "Aurangabad":     {"lat": 19.8762, "lon": 75.3433},
    "Kolhapur":       {"lat": 16.7050, "lon": 74.2433},
    "Latur":          {"lat": 18.4088, "lon": 76.5604},
    "Nagpur":         {"lat": 21.1458, "lon": 79.0882},
    "Amravati":       {"lat": 20.9374, "lon": 77.7796},
    "Nanded":         {"lat": 19.1383, "lon": 77.3210},
    "Satara":         {"lat": 17.6805, "lon": 74.0183},
    "Sangli":         {"lat": 16.8524, "lon": 74.5815},
    "Jalgaon":        {"lat": 21.0077, "lon": 75.5626},
    "Ahmednagar":     {"lat": 19.0948, "lon": 74.7480},
    "Raigad":         {"lat": 18.5158, "lon": 73.1298},
    "Thane":          {"lat": 19.2183, "lon": 72.9781},
    "Palghar":        {"lat": 19.6967, "lon": 72.7697},
    "Ratnagiri":      {"lat": 16.9902, "lon": 73.3120},
    "Sindhudurg":     {"lat": 16.3490, "lon": 73.8567},
    "Dhule":          {"lat": 20.9042, "lon": 74.7749},
    "Nandurbar":      {"lat": 21.3653, "lon": 74.2421},
    "Buldhana":       {"lat": 20.5292, "lon": 76.1842},
    "Akola":          {"lat": 20.7002, "lon": 77.0082},
    "Washim":         {"lat": 20.1120, "lon": 77.1342},
    "Yavatmal":       {"lat": 20.3888, "lon": 78.1204},
    "Wardha":         {"lat": 20.7453, "lon": 78.6022},
    "Gondia":         {"lat": 21.4624, "lon": 80.1948},
    "Bhandara":       {"lat": 21.1667, "lon": 79.6500},
    "Chandrapur":     {"lat": 19.9615, "lon": 79.2961},
    "Gadchiroli":     {"lat": 20.1809, "lon": 80.0000},
    "Osmanabad":      {"lat": 18.1860, "lon": 76.0416},
    "Hingoli":        {"lat": 19.7175, "lon": 77.1490},
    "Parbhani":       {"lat": 19.2704, "lon": 76.7749},
    "Jalna":          {"lat": 19.8347, "lon": 75.8816},
    "Beed":           {"lat": 18.9890, "lon": 75.7601},
    "Mumbai City":    {"lat": 18.9388, "lon": 72.8354},
    "Mumbai Suburban":{"lat": 19.0760, "lon": 72.8777},
}

PARAMETERS = "T2M,RH2M,PRECTOTCORR,WS2M,ALLSKY_SFC_SW_DWN"
START = "20190101"
END   = "20231231"

def fetch_district(name, lat, lon):
    print(f"⏳ Fetching {name}...")
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={PARAMETERS}"
        f"&community=AG"
        f"&longitude={lon}&latitude={lat}"
        f"&start={START}&end={END}"
        f"&format=JSON"
    )
    try:
        res = requests.get(url, timeout=60)
        data = res.json()
        props = data["properties"]["parameter"]
        dates = list(props["T2M"].keys())

        rows = []
        for date in dates:
            rows.append({
                "district":    name,
                "date":        date,
                "temperature": props["T2M"][date],
                "humidity":    props["RH2M"][date],
                "rainfall":    props["PRECTOTCORR"][date],
                "wind_speed":  props["WS2M"][date],
                "sunlight":    props["ALLSKY_SFC_SW_DWN"][date],
            })
        print(f"  ✅ {name} done — {len(rows)} days")
        return rows

    except Exception as e:
        print(f"  ❌ {name} failed — {e}")
        return []

all_rows = []
for i, (name, coords) in enumerate(DISTRICTS.items(), 1):
    print(f"[{i}/36]", end=" ")
    rows = fetch_district(name, coords["lat"], coords["lon"])
    all_rows.extend(rows)

df = pd.DataFrame(all_rows)
df.to_csv("maharashtra_weather.csv", index=False)
print(f"\n🎉 All done!")
print(f"📊 Total rows : {len(df)}")
print(f"🗺️  Districts  : {df['district'].nunique()}")
print(f"📅 Date range : {df['date'].min()} → {df['date'].max()}")
print(df.head(5))