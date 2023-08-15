from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)
import os, uuid
import json
def get_data(data):
    json_data=json.loads(open("config.json","r").read())
    return json_data[data]

class QueueHandler:
       
    def __init__(self,queue_name):
        self.queue_name=get_data(queue_name)['OutgoingQueueName']
        self.auth_token =get_data(queue_name)['AZURE_STORAGE_CONNECTION_STRING']
   
    def send_message(self,message):
        queue_client = QueueClient.from_connection_string(self.auth_token, self.queue_name)
        messages = queue_client.peek_messages()
        # print(queue_client.send_message(message))
        queue_client.send_message(message)

    def receive_message(self):
        queue_client = QueueClient.from_connection_string(self.auth_token, self.queue_name)
        messages = queue_client.peek_messages()
        messages = queue_client.receive_message(visibility_timeout=4000)
        return messages
    
    def delete_message(self,message):
        queue_client = QueueClient.from_connection_string(self.auth_token, self.queue_name)
        queue_client.delete_message(message.id, message.pop_receipt)
        
    def updater(self,message,content):
        return  QueueClient.from_connection_string(self.auth_token, self.queue_name).update_message(message.id,message.pop_receipt,content=content)       

