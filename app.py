import os
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

import config
import json

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)


# Cosmos Part #
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="AzureManagement", user_agent_overwrite=True)

db = client.get_database_client(DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)

# End of Cosmos Part #

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html') # render_template uses the files in the templates folder

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    #app.run(debug=True)