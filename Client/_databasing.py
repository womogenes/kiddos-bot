def get_attrib(self, userID, attribute=""):
    x = self.db.users.find_one({'idx': userID})
    if x:
        return x[attribute]
    return None