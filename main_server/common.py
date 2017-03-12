def check_keys(data,keys):
        for key in keys:
            if key not in data:
                return key

        return None

def check_float(value,min_value,max_value):
    try:
        value=float(value)
        if value>=min_value and value<=max_value:
            return value
        else:
            return None
    except ValueError:
        return None
        
