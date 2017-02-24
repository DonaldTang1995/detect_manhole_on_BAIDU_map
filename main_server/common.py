def check_keys(data,keys):
        for key in keys:
            if key not in data:
                return key

        return None

