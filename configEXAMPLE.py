# CONSTANTS LIST:

###BOT DETAILS###
# ENTER YOUR BOT API TOKEN FROM @BOTFATHER HERE:
BOT_TOKEN = ""
# ENTER YOUR BOT'S USERNAME WITHOUT '@' 
BOT_USERNAME = ""

###ADMIN DETAILS###
# ENTER YOUR NAME:
ADMIN_NAME = ""
# ENTER YOUR TELEGRAM ID:
ADMIN_ID = 123456789
# ENTER YOUR TIME ZONE (TZ FORMAT, EXAMPLE: 'ASIA/HONG_KONG')
ADMIN_TIMEZONE = ""

###MYSQL DETAILS###
# ENTER YOUR SERVER NAME
MYSQL_SERVER = "localhost"
# ENTER YOUR MYSQL USERNAME
MYSQL_USERNAME = ""
# ENTER YOUR MYSQL PASSWORD
MYSQL_PW = ""
# ENTER YOUR MYSQL DATABASE NAME
MYSQL_DBNAME = ""

###ACCUWEATHER API DETAILS###
# ENTER YOUR ACCUWEATHER API KEY (AT THE MOMENT USING 2 API KEYS)
# OPTAINED AT DEVELOPER.ACCUWEATHER.COM
ACCU_API_1 = ""
ACCU_API_2 = ""

###GOOGLE CUSTOM SEARCH ENGINE API DETAILS
# ENTER YOUR GOOGLE CSE API KEY
# OPTAINED AT https://developers.google.com/apis-explorer/
GOOGLE_API = ""
# ENTER YOUR CSE ID
# OPTAINED AT https://cse.google.com/
CSE_ID = ""

###YANDEX API
YANDEX_API = ""

### CREATE TABLE SQL, DO NOT AMEND###
SQL_CREATE_TABLE_1 = "CREATE TABLE IF NOT EXISTS `feedback` (`id` int(11) NOT NULL AUTO_INCREMENT, `message` mediumtext NOT NULL, `name` varchar(200) NOT NULL, `username` varchar(100) NOT NULL, `telegramid` int(20) NOT NULL, PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4"
SQL_CREATE_TABLE_2 = "CREATE TABLE IF NOT EXISTS `group` (`id` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(150) NOT NULL, `groupid` bigint(30) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4"
SQL_CREATE_TABLE_3 = "CREATE TABLE IF NOT EXISTS `patdb` (`patid` int(11) NOT NULL AUTO_INCREMENT, `patdesc` text NOT NULL, PRIMARY KEY (`patid`), UNIQUE (`patid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4"
SQL_CREATE_TABLE_4 = "CREATE TABLE IF NOT EXISTS `user` (`userid` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(100) NOT NULL, `username` varchar(100) DEFAULT NULL, `telegramid` int(20) NOT NULL, `patted` int(11) NOT NULL DEFAULT '0', `pattedby` int(11) NOT NULL DEFAULT '0', `loc` varchar(50) DEFAULT NULL, `banned` tinyint(1) NOT NULL DEFAULT '0', PRIMARY KEY (`userid`), UNIQUE KEY `userid` (`userid`), UNIQUE KEY `telegramid` (`telegramid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4"
SQL_DEFAULT_PAT = "INSERT INTO `patdb` (`patid`, `patdesc`) VALUES (1, 'is patted by'), (2, 'is again patted by')"


ACHV = [{"name": "Welcome to Hell", "desc": "Play a game"},
        {"name": "Welcome to the Asylum", "desc": "Play a chaos game"},
        {"name": "Alzheimer's Patient", "desc": "Play a game with an amnesia language pack"},
        {"name": "O HAI DER!", "desc": "Play a game with Para's secret account (not @para949)"},
        {"name": "Spy vs Spy", "desc": "Play a game in secret mode (no role reveal)"},
        {"name": "Explorer", "desc": "Play at least 2 games each in 10 different groups"},
        {"name": "Linguist", "desc": "Play at least 2 games each in 10 different language packs"},
        {"name": "I Have No Idea What I'm Doing", "desc": "Play a game in secret amnesia mode"},
        {"name": "Enochlophobia", "desc": "Play a 35 player game"},
        {"name": "Introvert", "desc": "Play a 5 player game"},
        {"name": "Naughty!", "desc": "Play a game using any NSFW language pack"},
        {"name": "Dedicated", "desc": "Play 100 games"},
        {"name": "Obsessed", "desc": "Play 1000 games"},
        {"name": "Here's Johnny!", "desc": "Get 50 kills as the serial killer"},
        {"name": "I've Got Your Back", "desc": "Save 50 people as the Guardian Angel"},
        {"name": "Masochist", "desc": "Win a game as the Tanne"},
        {"name": "Wobble Wobble", "desc": "Survive a game as the drunk (at least 10 players)"},
        {"name": "Inconspicuous", "desc": "In a game of 20 or more people, do not get a single lynch vote against you (and survive)"},
        {"name": "Survivalist", "desc": "Survive 100 games"},
        {"name": "Black Sheep", "desc": "Get lynched first 3 games in a row"},
        {"name": "Promiscuous", "desc": "As the harlot, survive a 5+ night game without staying home or visiting the same person more than once"},
        {"name": "Mason Brother", "desc": "Be one of at least two surviving masons in a game"},
        {"name": "Double Shifter", "desc": "Change roles twice in one game (cult conversion does not count)"},
        {"name": "Hey Man, Nice Shot", "desc": "As the hunter, use your dying shot to kill a wolf or serial killer"},
        {"name": "That's Why You Don't Stay Home", "desc": "As a wolf or cultist, kill or convert a harlot that stayed home"},
        {"name": "Double Vision", "desc": "Be one of two seers at the same time"},
        {"name": "Double Kill", "desc": "Be part of the Serial Killer / Hunter ending"},
        {"name": "Should Have Known", "desc": "As the Seer, reveal the Beholder"},
        {"name": "I See a Lack of Trust", "desc": "As the Seer, get lynched on the first day"},
        {"name": "Sunday Bloody Sunday", "desc": "Be one of at least 4 victims to die in a single night"},
        {"name": "Change Sides Works", "desc": "Change roles in a game, and win"},
        {"name": "Forbidden Love", "desc": "Win as a wolf / villager couple (villager, not village team)"},
        {"name": "Developer", "desc": "Have a pull request merged into the repo"},
        {"name": "The First Stone", "desc": "Be the first to cast a lynch vote 5 times in a single game"},
        {"name": "Smart Gunner", "desc": "As the Gunner, both of your bullets hit a wolf, serial killer, or cultist"},
        {"name": "Streetwise", "desc": "Find a different wolf, serial killer, or cultist 4 nights in a row as the detective"},
        {"name": "Speed Dating", "desc": "Have the bot select you as a lover (cupid failed to choose)"},
        {"name": "Even a Stopped Clock is Right Twice a Day", "desc": "As the Fool, have at least two of your visions be correct by the end of the game"},
        {"name": "So Close!", "desc": "As the Tanner, be tied for the most lynch votes"},
        {"name": "Cultist Convention", "desc": "Be one of 10 or more cultists alive at the end of a game"},
        {"name": "Self Loving", "desc": "As cupid, pick yourself as one of the lovers"},
        {"name": "Should've Said Something", "desc": "As a wolf, your pack eats your lover (first night does not count)"},
        {"name": "Tanner Overkill", "desc": "As the Tanner, have everyone (but yourself) vote to lynch you"},
        {"name": "Serial Samaritan", "desc": "As the Serial Killer, kill at least 3 wolves in single game"},
        {"name": "Cultist Fodder", "desc": "Be the cultist that is sent to attempt to convert the Cult Hunter"},
        {"name": "Lone Wolf", "desc": "In a chaos game of 10 or more people, be the only wolf - and win"},
        {"name": "Pack Hunter", "desc": "Be one of 7 living wolves at one time"},
        {"name": "Saved by the Bull(et)", "desc": "As a villager, the wolves match the number of villagers, but the game does not end because the gunner has a bullet"},
        {"name": "In for the Long Haul", "desc": "Survive for at least an hour in a single game"},
        {"name": "OH SHI-", "desc": "Kill your lover on the first night"},
        {"name": "Veteran", "desc": "Play 500 games.  You can now join @werewolfvets"}]

