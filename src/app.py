from flask import request, jsonify, Flask, abort
from service.systemController import SystemController
from store.mongoStore import MongoStore

app = Flask(__name__)
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


@app.route('/v1/openvalve', methods=['POST'])
def postOpenValve():
    controller = SystemController.getInstance()
    controller.openValve()
    return '', 201

@app.route('/v1/closevalve', methods=['POST'])
def postCloseValve():
    controller = SystemController.getInstance()
    controller.closeValve()
    return '', 201

@app.route('/v1/resetvolume', methods=['POST'])
def postResetVolume():
    controller = SystemController.getInstance()
    controller.resetVolume()
    return '', 201

@app.route('/v1/dose', methods=['POST'])
def postDose():
    controller = SystemController.getInstance()
    try:
        amount = float(request.args.get('amount', 0))
    except ValueError:
        abort(400)
    r = {'amount': controller.dose(amount)}
    return r, 201

@app.route('/v1/calibrate', methods=['POST'])
def postCalibrate():
    controller = SystemController.getInstance()
    return controller.calibrateSystem(), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)