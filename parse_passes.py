import json 
import prettyprinter


def get_category_line_nos(text) -> dict:
    """Gets starting and stopping line numbers for each category in the credentials file.

    Args:
        text (str): Raw credentials file text.

    Returns:
        dict: {category name (str) : (starting line number, stopping line number)}
    """
    line_no = 1
    results = {}
    get_next_line = False
    category = '<General>'
    category_start = 1

    lines = text.split('\n')

    for line in lines:
        # A longer line of dashes precedes a category header.
        if '-----' in line:
            get_next_line = True
            line_no += 1
            continue
        # Get the next line and strip accompanying dashes.
        if get_next_line:
            # We only want the first header line to matter, not the third
            if line.strip() == '':
                get_next_line = False
                line_no += 1
                continue
            
            # Current category ends here
            results[category] = (category_start, line_no)
            # Next category starts here
            category_start = line_no + 1
            category = line.replace('-', '').strip()
            get_next_line = False

        # When arrived at last line, finalize last category
        if line_no == len(lines):
            results[category] = (category_start, line_no)

        line_no += 1

    return results

def isolate_accounts(text) -> str:
    # There should be two newlines between accounts
    accounts_raw = text.split('\n\n')
    # Remove outer newlines
    accounts_raw = [x.strip() for x in accounts_raw]
    # Remove empty lines
    accounts_raw = [x for x in accounts_raw if x != '']
    return accounts_raw


def parse_accounts(text) -> dict:
    accounts = isolate_accounts(text)
    results = {}
    for account in accounts:
        account = account.split('\n')
        # Key is Account name, value is a dict {user: pass}.
        if len(account) > 2:
            for set_ in account[2:]:
                # Get the first value as account name, then split all following sets into key:value pairs
                if account[0] in results:
                    # Add entry to value dict
                    results[account[0]][set_.split(':')[0].strip()] = set_.split(':')[1].strip()
                else:
                    # Create first dict as value
                    results[account[0]] = { set_.split(':')[0].strip(): set_.split(':')[1].strip() }
    # prettyprinter.pprint(results, indent=4)
    return results


def parse_account_categories(text) -> dict:
    """Cut up raw text into groups of credentials, return as a dict with 
    group names as keys and raw text as values.

    Args:
        text (str): Raw text of credentials file.

    Returns:
        dict: dict with raw text split up into groups.
    """
    category_start_stop = get_category_line_nos(text)

    results = {category: '\n'.join(text.split('\n')[start_stop[0]: start_stop[1]])
                for category, start_stop in category_start_stop.items()}

    return results


def parse(input_file) -> dict:

    with open(input_file, 'r') as file_:
        text = file_.read()
    
    results = parse_account_categories(text)
    # print(json.dumps(categories, indent=4))

    for category, raw_text in results.items():
        results[category] = parse_accounts(raw_text)

    return results 


# Test
if __name__ == '__main__':
    accounts = parse('test.txt')
    prettyprinter.pprint(accounts, indent=4)
