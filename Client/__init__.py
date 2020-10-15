import discord

class Client(discord.Client):
    
    def initialize(self):
        with open("./data/date-info.json") as fin:
            self.dateInfo = json.load(fin)
            self.lastSent = dt.strptime(self.dateInfo["last-sent-quote"], "%Y-%m-%d %H:%M:%S.%f")
            fin.close()
            
        with open("./data/trivia-info.json") as fin:
            self.triviaInfo = json.load(fin)
            fin.close()
        
        with open("./data/point-info.json") as fin:
            x = json.load(fin)
            self.points = {"lifetime": {}, "weekly": {}, "hitrate": {}}
            for i in x["lifetime"]:
                self.points["lifetime"][int(i)] = x["lifetime"][i]
            for i in x["weekly"]:
                self.points["weekly"][int(i)] = x["weekly"][i]
            for i in x["hitrate"]:
                self.points["hitrate"][int(i)] = x["hitrate"][i]
            fin.close()
        
        # Reset weekly points on a ?day.
        if dt.now().weekday() == 0 and dt.strptime(self.dateInfo["last-reset-weekly-points"], "%Y-%m-%d %H:%M:%S.%f").date() != dt.now().date():
            for i in self.points["weekly"]:
                self.points["weekly"][i] = 0
            with open("./data/point-info.json", "w") as fout:
                json.dump(self.points, fout, indent=2)
                fout.close()
            self.dateInfo["last-reset-weekly-points"] = str(dt.now())
            with open("./data/date-info.json", "w") as fout:
                json.dump({ "last-sent-quote": str(self.lastSent) }, fout, indent=2)
                fout.close()
        
        
        self.questionCache = []
        
        self.question = None
        self.answers = None
        self.rightAnswer = None
        self.answered = True
        self.lastSentQuestion = 0
        
        self.botChannel = self.get_channel(762173542233407528)
        self.quoteChannel = self.get_channel(761340228450910250)
        self.leaderboardChannel = self.get_channel(763825477533302856)
        
        
