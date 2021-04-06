# Unsubscribe function
def unsubscribe():
    successes = []
    fails = []
    header={'header':'content-type: application/json'}
    email_dict = {
        'status': 'unsubscribed'
        }
    email_json = json.dumps(email_dict)

    for email in unsubscribe:
        global response
        hashed = hashlib.md5(email.encode()).hexdigest()
        response = requests.patch(api_link+NewList_endpoint+hashed,
                                 auth=(USER,key),
                                 data=email_json,
                                 header=header
                                 )

    # Unsubscribe report
    print(email)
    print(response.status_code, response.reason)
    if response.status_code != 200:
        print('Failed')
        fails.append((email, response.status_code, response.reason))
    else:
        print(email_json)
        successes.append(email)

    print(f'{str(len(successes))} emails successfully unsubscribed.')
    # Failed unsubscribes report
    if any(fails):
        print('\nThe following emails were not successfully unsubscribed:')
        for fail in fails:
            print(fail[0])
    return fails


# Subscribe function
def subscribe():
    successes = []
    fails = []
    header = {'header':'content-type:application/json'}

    for email in vendor_list:
        email_dict = {
            'email_address': email,
            'status': 'subscribed'
            }
        email_json = json.dumps(email_dict)
        global response
        response = requests.post(api_link+VendorList_endpoint,
                                 auth=('yhecht',key),
                                 data=email_json,
                                 headers=header
                                )
        # Subscribes report
        print(email)
        print(response.status_code, response.reason)
        if response.status_code == 200:
            print(email_json)
            successes.append(email)
        else:
            print('Failed')
            fails.append((email, response.status_code, response.reason))
    print(f'\n{str(len(successes))} emails successfully subscribed.')
    # Failed subscribes report
    if any(fails):
        print('\nThe following emails were not successfully subscribed:')
        for i in fails:
            print(i[0]) # See error documentation here: https://mailchimp.com/developer/guides/error-glossary/
    return fails