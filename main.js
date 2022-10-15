const {Database} = require('./database');
const {Entity} = require('./entity');
const {WebSocket} = require('ws');

const PORT = 9000;

const database = new Database();
const wsServer = new WebSocket.Server({
    port: PORT,
});

var wsClients = [];

wsServer.on('connection', function(wsClient) {
    wsClients.push(wsClient);
    wsClient.on('message', function(data) {
        var decoder = new TextDecoder("utf-8");
        var message = decoder.decode(data);
        var parsedJSON = JSON.parse(message);

        if(!parsedJSON["type"]) {
            console.error("Every request to database must have 'type' field.");
            return;
        }
        if(parsedJSON["data"]) {
            //If we have data field, that means we want to save something
            var objectEntity = new Entity(parsedJSON["type"], parsedJSON["data"]);
            database.saveJSON(objectEntity).then(resolved1 => {
                if(resolved1) {
                    database.selectJSONCategory(resolved1, undefined)
                        .then(resolved2 => {
                            for(var i = 0; i < wsClients.length; i++) {
                                  wsClients[i].send(JSON.stringify(resolved2));
                            }
                        });  
                    
                }
            });
        } else {
            //If we do not have this field, that means we want to load something
            database.selectJSONCategory(parsedJSON["type"], parsedJSON["filters"])
            .then(resolved => {
                wsClient.send(JSON.stringify(resolved));
            });
        }
    });
});
