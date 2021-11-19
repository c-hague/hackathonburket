from flask import request

from store.mongoStore import MongoStore


@app.route('/v1/mass', methods=['GET'])
def getMass():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    store.getMass(startTime, endTime, skip, limit)

@app.route('/v1/volume', methods=['GET'])
def getVolume():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    store.getVolume(startTime, endTime, skip, limit)

@app.route('/v1/state', methods=['GET'])
def getState():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    store.getState(startTime, endTime, skip, limit)

@app.route('/v1/time', methods=['GET'])
def getTime():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    store.getTime(startTime, endTime, skip, limit)