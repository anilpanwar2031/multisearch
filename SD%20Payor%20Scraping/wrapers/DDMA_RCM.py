def main(data):
    for obj in data['RcmEobClaimDetail']:
        if obj.get('DateOfService'):
            obj['DateOfService'] = obj.get('DateOfService').split('-')[0]
    return data    

