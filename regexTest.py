import re

#Username[letters A-Z, numbers 0-9, underscores] (15 chars) \n Handle (15 chars) \n · \n age of post (6 chars) \n text (280 chars)[link/hyperlink text might be here] \n video length (4 chars) \n From \nVideos \n comment (5 chars, can contain K or M) \n retweets (5 chars, can contain K or M) \n likes (5 chars, can contain K or M) \n Show this thread'

tweet1 ='Michael Block\n@NYTrafficLaw\n·\n8m\nCheck out my latest article: Speeding Ticket Won In Suffolk County https://linkedin.com/pulse/speeding-ticket-won-suffolk-county-michael-block-esq-… via \n@LinkedIn\nSpeeding Ticket Won In Suffolk County\nWe recently represented a client of ours at the Southampton Town Court in Suffolk County. He was charged with a 6 point speeding ticket.\nlinkedin.com'

tweet2 = 'SC Vanderbilt Museum\n@TheVanderbilt\n·\n9m\nCelebrate the lives of Irish immigrants on March 7 at the Vanderbilt Museum! Members only pre-sale open now! @ Suffolk County Vanderbilt Museum and Planetarium https://instagram.com/p/B8MSBwoHfGv/?igshid=11rry556b5js3…'

tweet3 = "Le' Foogazi Times\n@MasterPhoFooga1\n·\n18m\nReplying to \n@USRoute41\n @GinSecurities\n and \n@NYGovCuomo\nNo Westchester county\nHe just goes to Suffolk as part of the Hampstein crew\n1"

tweet4 = 'Builder of stuff\n@JohnDillworth\n·\n25m\nReplying to \n@LIRR\nSince Babylon is the only express station in Suffolk County and is the connecting point for shuttle trains please share the options for non-resident parking at Babylon. That is a great option for Port Jeff riders so tell us about the extra non-resident parking you secured for us.'

tweet5 = 'Jobs Ipswich\n@JobsIpswich1\n·\n28m\nProgramme Co-ordinator – Suffolk County Council – Ipswich\nProgramme Co-ordinator – Suffolk County Council – Ipswich\nThis organisation positively encourages the use of technology to communicate and engage, but in this role you will need to operate across a wide and rural [...]\nalljobsintheuk.eu'


# #TODO is it @ + 15 chars?
# 
# splitReg = re.split(r"^([A-Za-z0-9 +]{,50}<username>)\n(^@[A-Za-z0-9_-]{,16}<handle>)\n([0-9K|M]?<age>)\n([A-Za-z0-9_-]{,280}<text>)  $", tweet1)
# 
# for i in splitReg:
#     print(i)

splitReg = re.compile(r"^([A-Za-z0-9 +]{,50}<username>)\n(^@[A-Za-z0-9_-]{,16}<handle>)\n([0-9K|M]?<age>)\n([A-Za-z0-9_-]{,280}<text>", re.MULTILINE)
print(re.findall(splitReg, tweet1))

tweet = tweet3.splitlines()

for i in tweet:
    print(i)

##print("")
##print("")
##
##print("[", end = '')
##print(*tweet, sep = ", ", end = '')  
##print("]", end = '')
##
##print("")
##print("")
##
##print(tweet[0])

# https://stackoverflow.com/questions/28856238/how-to-get-group-name-of-match-regular-expression-in-python
# https://stackoverflow.com/questions/36817785/different-way-to-specify-matching-new-line-in-python-regex?rq=1
# https://stackoverflow.com/questions/36807039/regular-expression-pattern-match-newline-and-tab-in-python

#TODO might have to compile re.compile first
#print(splitReg.groupindex)

