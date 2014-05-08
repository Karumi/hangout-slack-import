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

    for x in jsonObj["conversation_state"]:
        if x["conversation_id"]["id"] == args.conversation_id:
            participants = {}
            for p in x["conversation_state"]["conversation"]["participant_data"]:
                participants[p["id"]["chat_id"]] = p["fallback_name"]

            for y in x["conversation_state"]["event"]:
                timestamp = int(y["timestamp"]) / 1000000
                username = participants[y["sender_id"]["chat_id"]] if y["sender_id"]["chat_id"] in participants else "unknown"

                if y["event_type"] == u'REGULAR_CHAT_MESSAGE':
                    if "segment" in y["chat_message"]["message_content"]:
                        text = y["chat_message"]["message_content"]["segment"][0]["text"]
                    else:
                        text = \
                            y["chat_message"]["message_content"]["attachment"][0]["embed_item"]["embeds.PlusPhoto.plus_photo"]["url"]
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