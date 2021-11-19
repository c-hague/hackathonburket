from flask import json, request, jsonify
from service.systemController import SystemController
from store.mongoStore import MongoStore


@app.route('/v1/mass', methods=['GET'])
def getMass():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getMass(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/volume', methods=['GET'])
def getVolume():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getVolume(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/state', methods=['GET'])
def getState():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getState(startTime, endTime, skip, limit)
    return items

@app.route('/v1/time', methods=['GET'])
def getTime():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getTime(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/floflow', methods=['GET'])
def getFloFlow():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getFloFlow(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/velocity', methods=['GET'])
def getVelocity():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getVelocity(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/weight', methods=['GET'])
def getWeight():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getWeight(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/flow', methods=['GET'])
def getFlow():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getFlow(startTime, endTime, skip, limit)
    return jsonify(items)

@app.route('/v1/total', methods=['GET'])
def getTotal():
    store = MongoStore.getInstance()
    startTime = request.args.get('starttime')
    endTime = request.args.get('endtime')
    skip = request.args.get('skip', 0)
    limit = request.args.get('limit', 256)
    items = store.getTotal(startTime, endTime, skip, limit)
    return jsonify(items)


@app.route('v1/openvalve', methods=['POST'])
def postValve():
    controller = SystemController.getInstance()
    controller.openValve()
    return '', 201

@app.route('v1/openvalve', methods=['POST'])
def postValve():
    controller = SystemController.getInstance()
    controller.closeValve()
    return '', 201

@app.route('v1/resetvolume', methods=['POST'])
def postValve():
    controller = SystemController.getInstance()
    controller.resetVolume()
    return '', 201

