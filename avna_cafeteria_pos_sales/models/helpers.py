def money(x):
    try: return round(float(x or 0.0),2)
    except: return 0.0
