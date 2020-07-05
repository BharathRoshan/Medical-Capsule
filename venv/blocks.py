import hashlib
import time
import datetime


class MainBlock:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()
        self.inner_previous_hash = "0"
        self.innerBlocks = []

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()

    def setInnerPrevHash(self, hash):
        self.inner_previous_hash = hash

    def getTimestamp(self):
        return self.timestamp

    def getData(self):
        return self.data

    def getPreviousHash(self):
        return self.previous_hash

    def getHash(self):
        return self.hash

    def getInnerBlocks(self):
        return self.innerBlocks

    def getInnerPrevHash(self):
        return self.inner_previous_hash


class InnerBlock:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()

    def getTimestamp(self):
        return self.timestamp

    def getData(self):
        return self.data

    def getPreviousHash(self):
        return self.previous_hash

    def getHash(self):
        return self.hash


class Record:
    def __init__(self, treatment, date, hname, symptoms, bp, sugar, weight, docName):
        self.treatment = treatment
        self.date = date
        self.hname = hname
        self.symptoms = symptoms
        self.bp = bp
        self.sugar = sugar
        self.weight = weight
        self.docName = docName
