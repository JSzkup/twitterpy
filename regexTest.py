import re
import pandas as pd

#name[letters A-Z, numbers 0-9, underscores] (15 chars) \n username (15 chars) \n · \n age of post (6 chars) \n text (280 chars)[link/hyperlink text might be here] \n video length (4 chars) \n From \nVideos \n comment (5 chars, can contain K or M) \n retweets (5 chars, can contain K or M) \n likes (5 chars, can contain K or M) \n Show this thread'

#tweet1 ='Michael Block\n@NYTrafficLaw\n·\n8m\nCheck out my latest article: Speeding Ticket Won In Suffolk County https://linkedin.com/pulse/speeding-ticket-won-suffolk-county-michael-block-esq-… via \n@LinkedIn\nSpeeding Ticket Won In Suffolk County\nWe recently represented a client of ours at the Southampton Town Court in Suffolk County. He was charged with a 6 point speeding ticket.\nlinkedin.com'
#
#tweet2 = 'SC Vanderbilt Museum\n@TheVanderbilt\n·\n9m\nCelebrate the lives of Irish immigrants on March 7 at the Vanderbilt Museum! Members only pre-sale open now! @ Suffolk County Vanderbilt Museum and Planetarium https://instagram.com/p/B8MSBwoHfGv/?igshid=11rry556b5js3…'
#
#tweet3 = "Le' Foogazi Times\n@MasterPhoFooga1\n·\n18m\nReplying to \n@USRoute41\n @GinSecurities\n and \n@NYGovCuomo\nNo Westchester county\nHe just goes to Suffolk as part of the Hampstein crew\n1"
#
#tweet4 = 'Builder of stuff\n@JohnDillworth\n·\n25m\nReplying to \n@LIRR\nSince Babylon is the only express station in Suffolk County and is the connecting point for shuttle trains please share the options for non-resident parking at Babylon. That is a great option for Port Jeff riders so tell us about the extra non-resident parking you secured for us.'
#
#tweet5 = 'Jobs Ipswich\n@JobsIpswich1\n·\n28m\nProgramme Co-ordinator – Suffolk County Council – Ipswich\nProgramme Co-ordinator – Suffolk County Council – Ipswich\nThis organisation positively encourages the use of technology to communicate and engage, but in this role you will need to operate across a wide and rural [...]\nalljobsintheuk.eu'


tweet_dict = {
    "name": re.compile(r'Name = (?P<name>^[a-zA-z0-9 _]{,50})$\n'),
    "username": re.compile(r'Username = (?P<username>^@[a-zA-Z_0-9]{,15})$\n'),
    #TODO test this in code,  works 9/10 times on regex101
    #"text": re.compile(r'Text = ((?P<text>^.{,280})\n$'),
}


def parse_line(line):

    for key, tweet in tweet_dict.items():
        match = tweet.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def parse_file(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    data : pd.DataFrame
        Parsed data

    """

    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r', encoding="utf8") as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = parse_line(line)

            # extract school name
            if key == 'name':
                name = match.group('name')
            else:
                name = match.group('NO TWITTER NAME')

            # extract grade
            if key == 'username':
                username = match.group('username')
                #username = int(username)
            else:
                username = match.group('NO TWITTER USERNAME')


            while line.strip():
                # extract number and value
                #number, value = line.strip().split(',')
                #value = value.strip()
                # create a dictionary containing this row of data
                row = {
                    'Name': name,
                    'Username': username
                    #'Student number': number,
                    #value_type: value
                }
                # append the dictionary to the data list
                data.append(row)
                line = file_object.readline()

            line = file_object.readline()

        # create a pandas DataFrame from the list of dicts
        data = pd.DataFrame(data)
        # set the School, Grade, and Student number as the index
        data.set_index(['name', 'username'], inplace=True)
        # consolidate df to remove nans
        data = data.groupby(level=data.index.names).first()
        # upgrade Score from float to integer
        data = data.apply(pd.to_numeric, errors='ignore')
    return data

if __name__ == '__main__':
    filepath = 'Unorganized.txt'
    data = parse_file(filepath)
    print(data)

#splitReg = re.compile(r"^([A-Za-z0-9 +]{,50}<name>)\n(^@[A-Za-z0-9_-]{,16}<username>)\n([0-9K|M]?<age>)\n([A-Za-z0-9_-]{,280}<text>", re.MULTILINE)
#print(re.findall(splitReg, tweet1))


# https://github.com/bluprince13/parsing_text_with_python
# https://www.vipinajayakumar.com/parsing-text-with-python/
# https://stackoverflow.com/questions/28856238/how-to-get-group-name-of-match-regular-expression-in-python
# https://stackoverflow.com/questions/36817785/different-way-to-specify-matching-new-line-in-python-regex?rq=1
# https://stackoverflow.com/questions/36807039/regular-expression-pattern-match-newline-and-tab-in-python

#TODO might have to compile re.compile first
#print(splitReg.groupindex)

