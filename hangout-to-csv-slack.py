import json
import csv
import argparse

parser = argparse.ArgumentParser(description='Parse your Google data archives of Hangout into CSV for Slack import')
parser.add_argument('-i', '--input', type=file, required=True, help='Hangout json file', metavar='<Hangouts.json>')
parser.add_argument('-o', '--output', type=argparse.FileType('wb'), required=True, help='CSV output file', metavar='<hangouts.csv>')
parser.add_argument('-cid', '--conversation_id', required=True, metavar='<KYJA4kuoMFTyYCYXNzPpEsAnD4>')
parser.add_argument('-ch', '--channel', required=True, metavar='<hangout>')

args = parser.parse_args()
print args.input

jsonObj = json.load(args.input)

with args.output as csvfile:
    hangoutswriter = csv.writer(csvfile)

    for x in jsonObj["conversations"]:

        if x["conversation"]["conversation_id"]["id"] == args.conversation_id:
            participants = {}
            for p in x["conversation"]["conversation"]["participant_data"]:
                participants[p["id"]["chat_id"]] = p["fallback_name"]

            for y in x["events"]:
                timestamp = int(y["timestamp"]) / 1000000
                username = participants[y["sender_id"]["chat_id"]] if y["sender_id"]["chat_id"] in participants else "unknown"

                if y["event_type"] == u'REGULAR_CHAT_MESSAGE':
                    if "segment" in y["chat_message"]["message_content"]:
                        messages = []
                        for s in y["chat_message"]["message_content"]["segment"]:
                            if s["type"] == "LINE_BREAK":
                                messages.append("\n")
                            else:
                                messages.append(s["text"].replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c","").replace(u"\u201d", "").strip())
                        text = ' '.join(messages)
                    else:
                        text = \
                            y["chat_message"]["message_content"]["attachment"][0]["embed_item"]["plus_photo"]["url"]
                    #if username == "unknown":
                    #    print timestamp, channel, y["sender_id"]["chat_id"], text,
                    print timestamp, args.channel, username, text
                    hangoutswriter.writerow([timestamp, args.channel, username, text.encode('utf-8')])

                else:
                    # HANGOUT_EVENT
                    # ADD_USER
                    # RENAME_CONVERSATION
                    # REMOVE_USER
                    # print y["event_type"]
                    pass
