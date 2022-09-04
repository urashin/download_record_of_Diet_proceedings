# -*- coding: utf-8 -*-

import pandas as pd
import urllib.parse
import requests
import xml.etree.ElementTree as ET
import datetime as dt

class SpeechRecord:
    def __init__(self, srecord_json):
        self.speechID = srecord_json["speechID"]
        self.speechOrder = srecord_json["speechOrder"]
        self.speaker = srecord_json["speaker"]
        self.speakerYomi = srecord_json["speakerYomi"]
        self.speakerGroup = srecord_json["speakerGroup"]
        self.speakerPosition = srecord_json["speakerPosition"]
        self.speakerRole = srecord_json["speakerRole"]
        self.speech = srecord_json["speech"]
        self.startPage = srecord_json["startPage"]
        self.createTime = srecord_json["createTime"]
        self.updateTime = srecord_json["updateTime"]
        self.speechURL = srecord_json["speechURL"]
    def showSpeechRecord(self):
        print(self.speechID + " / " + self.speaker + " / " + self.speech)

class MeetingRecord:
    def __init__(self, mrecord_json):
        self.issueID = mrecord_json["issueID"]
        self.imageKind = mrecord_json["imageKind"]
        self.searchObject = mrecord_json["searchObject"]
        self.session = mrecord_json["session"]
        self.nameOfHouse = mrecord_json["nameOfHouse"]
        self.nameOfMeeting = mrecord_json["nameOfMeeting"]
        self.issue = mrecord_json["issue"]
        self.date = mrecord_json["date"]
        self.closing = mrecord_json["closing"]
        self.meetingURL = mrecord_json["meetingURL"]
        self.pdfURL = mrecord_json["pdfURL"]
        self.speechRecords = []
        for srecord_json in mrecord_json["speechRecord"]:
            speechRecord = SpeechRecord(srecord_json)
            self.speechRecords.append(speechRecord)
    def showMeetingRecord(self):
        for sr in self.speechRecords:
            sr.showSpeechRecord()

class Meeting:
    def __init__(self, response_json):
        self.numberOfRecords = response_json["numberOfRecords"]
        self.numberOfReturn = response_json["numberOfReturn"]
        self.startRecord = response_json["startRecord"]
        self.nextRecordPosition = response_json["nextRecordPosition"]
        self.meetingRecords = []
        for mrecord_json in response_json["meetingRecord"]:
            meetingRecord = MeetingRecord(mrecord_json)
            self.meetingRecords.append(meetingRecord)
    def showMeeting(self):
        for m in self.meetingRecords:
            m.showMeetingRecord()

class MeetingManager:
    def __init__(self):
        self.meeting_list = []
    def getRecordOfDiet(self,url, params: dict):
        parameter = '?' + urllib.parse.quote('maximumRecords=10'
                                + '&startRecord=' + str(params['startRecord'])
                                + '&from=' + params['from']
                                + '&until=' + params['until']
                                + '&recordPacking=json')
        response = requests.get(url + parameter)
        return response.json()
    def getEndDate(self,start_date, days):
        # 開始日付と終了日付の取得
        from_dt = dt.datetime.strptime(start_date, '%Y-%m-%d')
        print("from : " + from_dt.strftime('%Y-%m-%d'))
        end_dt = from_dt + dt.timedelta(days=days)
        end_date = end_dt.strftime('%Y-%m-%d')
        return end_date
    def getMeetings(self,start_date, days):
        end_date = self.getEndDate(start_date, days)
        #
        url = 'http://kokkai.ndl.go.jp/api/1.0/meeting'
        ret_n = 1
        total_n = 0
        next_pos = 0
        startRecord = 1
        while ret_n > 0:
            params = {'startRecord': startRecord, 'from': start_date, 'until': end_date}
            response_json = self.getRecordOfDiet(url, params)
            meeting = Meeting(response_json)
            if meeting == None:
                return
            self.meeting_list.append(meeting)
            ret_n = response_json["numberOfReturn"]
            next_pos = response_json["nextRecordPosition"]
            if next_pos == None:
                print("get end of issue None")
                break
            total_n = response_json["numberOfRecords"]
            startRecord = next_pos
    def showMeetings(self):
        for m in self.meeting_list:
            m.showMeeting()

if __name__ == '__main__':

    # 開始日付の指定    
    from_str = '2019-01-29'
    # 何日後まで？
    days=2

    mm = MeetingManager()
    mm.getMeetings(from_str,days)
    mm.showMeetings()


