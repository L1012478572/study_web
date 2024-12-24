from flask import Flask
from flask.json import jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
from markupsafe import escape
from flask import request
from flask import Response
from flask import send_file

import sys
import os
sys.path.append(os.getcwd())
import back.gb_systemParam as sp

import cv2

debug = True

if debug != True:
    import GW_manger as gw
    manger = gw.GW_manger()


app = Flask(__name__)
CORS(app)
api = Api(app)

#返回一个json数据例如
# {
#  "code": 0,
#  "data": [
#    { "id": 1, "name": "Stream 1", "url": "rtmp://example.com/stream1" },
#    { "id": 2, "name": "Stream 2", "url": "http://example.com/stream2" }, // 非 RTMP 流
#    { "id": 3, "name": "Stream 3", "url": "rtmp://example.com/stream3" }
#  ]
#}

@app.route('/index/api/getMediaList&schema=rtsp', methods=['GET'])
def get_media_list():
    # 模拟返回一些数据
    data = {
        "code": 0,
        "data": [
            { "id": 1, "name": "Camera 1", "url": "rtsp://127.0.0.1:8554//mystream" }
        ]
    }
    return jsonify(data)

@app.route('/index/api/getThreadsLoad', methods=['GET'])
def get_threads_load():
    # 模拟返回一些数据
    data = {"threads": ["127.0.0.1:8554/mystream"]}
    return jsonify(data)

# @app.route('/', methods=["GET"])
# def index():
#     return "Welcome to API v1, try /hello."


'''
**描述**: 获取当前云台的配置信息。
**请求方法**: `GET`
**接口路径**: `/api/param/ptzinfo`
'''
@app.route('/api/param/ptzinfo', methods=['GET'])
def get_ptz_info():
    data_xml = sp.get_yuntaiParam()
    # 接口返回xml数据
    return Response(data_xml, mimetype='application/xml')

'''
**描述**: 设置云台的配置信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/ptzinfo`
'''
@app.route('/api/param/ptzinfo', methods=['PUT'])
def set_ptz_info():
    # 获取接口请求数据
    xml_data = request.data
    # print(xml_data)
    # 调用系统参数模块的设置方法
    result_xml = sp.set_yuntaiParam(xml_data)
    # 返回结果
    return Response(result_xml, mimetype='application/xml')

'''
**描述**: 获取当前偏移信息。
**请求方法**: `GET`
**接口路径**: `/api/param/offsetinfo`
'''
@app.route('/api/param/offsetinfo', methods=['GET'])
def get_offset_info():
    data_xml = sp.get_offsetParam()
    # 接口返回xml数据
    return Response(data_xml, mimetype='application/xml')

'''
**描述**: 设置偏移信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/offsetinfo`
'''
@app.route('/api/param/offsetinfo', methods=['PUT'])
def set_offset_info():
    xml_data = request.data
    result_xml = sp.set_offsetParam(xml_data)
    return Response(result_xml, mimetype='application/xml')

'''
**描述**: 获取当前云台控制信息。
**请求方法**: `GET`
**接口路径**: `/api/param/ptzcontrol`
'''
@app.route('/api/param/ptzcontrol', methods=['GET'])
def get_ptz_control():
    data_xml = sp.get_ptzcontrolParam()
    return Response(data_xml, mimetype='application/xml')

'''
**描述**: 设置云台控制信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/ptzcontrol`
'''
@app.route('/api/param/ptzcontrol', methods=['PUT'])
def set_ptz_control():
    xml_data = request.data
    result_xml = sp.set_ptzcontrolParam(xml_data)
    return Response(result_xml, mimetype='application/xml')

'''
**描述**: 获取预制信息列表。
**请求方法**: `GET`
**接口路径**: `/api/param/presetlist`
'''
@app.route('/api/param/presetlist', methods=['GET'])
def get_preset_list():
    data_xml = sp.get_presetlistParam()
    return Response(data_xml, mimetype='application/xml')

'''
**描述**: 添加新的预制信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/presetlist/add`
'''
@app.route('/api/param/presetlist/add', methods=['PUT'])
def add_preset():
    xml_data = request.data
    result_xml = sp.add_presetInfo(xml_data)
    return Response(result_xml, mimetype='application/xml')

'''
**描述**: 删除指定的预制信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/presetlist/remove`
**请求参数**: - `id`: 预制信息ID
'''
@app.route('/api/param/presetlist/remove', methods=['PUT'])
def remove_preset():
    try:
        preset_id = request.args.get('id')
        # 根据是否提供了 preset_id 来处理逻辑
        if preset_id:
            # 处理带有 preset_id 的逻辑
            data_xml = sp.remove_presetInfo(int(preset_id))
            return Response(data_xml, mimetype='application/xml')
        else:
            err_xml = sp.get_error_xml(400, 'Missing parameter: preset_id')
            return Response(err_xml, mimetype='application/xml')
    except Exception as e:
        print('remove_preset: ', e)
    except:
        print('remove_preset: Unknown error')
    err_xml = sp.get_error_xml(500, 'Unknown error')
    return Response(err_xml, mimetype='application/xml')

'''
**描述**: 设置预制信息列表。
**请求方法**: `PUT`
**接口路径**: `/api/param/presetlist`
'''
@app.route('/api/param/presetlist', methods=['PUT'])
def set_preset_list():
    xml_data = request.data
    result_xml = sp.set_presetlistParam(xml_data)
    return Response(result_xml, mimetype='application/xml')

'''
**描述**: 更新指定的预制信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/presetlist/update`
**请求参数**:
- `id`: 预制信息ID
'''
@app.route('/api/param/presetlist/update', methods=['PUT'])
def update_preset():
    try:
        preset_id = request.args.get('id')
        xml_data = request.data
        if preset_id:
            data_xml = sp.update_presetInfo(int(preset_id), xml_data)
            return Response(data_xml, mimetype='application/xml')
        else:
            err_xml = sp.get_error_xml(400, 'Missing parameter: preset_id')
            return Response(err_xml, mimetype='application/xml')
    except Exception as e:
        print('update_preset: ', e)
    except:
        print('update_preset: Unknown error')
    err_xml = sp.get_error_xml(500, 'Unknown error')
    return Response(err_xml, mimetype='application/xml')

'''
**描述**: 应用配置信息。
**请求方法**: `PUT`
**接口路径**: `/api/param/app`
'''
@app.route('/api/param/app', methods=['PUT'])
def apply_param():
    if debug != True:
        manger.init_module()
    return jsonify({"status": "success", "message": "Configuration applied successfully"})

'''
**描述**: 获取所有模型文件的列表。
**请求方法**: `GET`
**接口路径**: `/api/model/list`
'''
@app.route('/api/model/list', methods=['GET'])
def get_model_list():
    model_list = sp.get_modelList()
    return Response(model_list, mimetype='application/xml')

'''
**描述**: 上传单个模型文件。
**请求方法**: `POST`
**接口路径**: `/api/model/upload`
**请求参数**: 
- `file`: 要上传的模型文件
'''
@app.route('/api/model/upload', methods=['POST'])
def upload_model():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400
        if file:
            # 获取文件的名字
            filename = file.filename
            # 保存文件
            ret = sp.save_model(filename, file)
            if ret == True:
                return jsonify({"status": "success", "message": "Model file uploaded successfully"}), 200
            else:
                return jsonify({"status": "error", "message": "Model file upload failed"}), 500
    except Exception as e:
        print('upload_model: ', e)
    except:
        print('upload_model: Unknown error')
    return jsonify({"status": "error", "message": "Unknown error"}), 500

'''
**描述**: 下载单个模型文件。
**请求方法**: `GET`
**接口路径**: `/api/model/download`
**请求参数**: 
- `file`: 要下载的模型文件名
'''
@app.route('/api/model/download', methods=['GET'])
def download_model():
    try:
        filename = request.args.get('file')
        print('filename: ', filename)
        if filename:
            file_path = sp.get_model_path(filename)
            if file_path is not None:
                return send_file(file_path, as_attachment=True)
            else:
                return jsonify({"status": "error", "message": "Model file not found"}), 404
        else:
            return jsonify({"status": "error", "message": "Missing parameter: file"}), 400
    except Exception as e:
        print('download_model: ', e)
    except:
        print('download_model: Unknown error')
    return jsonify({"status": "error", "message": "Unknown error"}), 500

'''
**描述**: 删除指定的模型文件。
**请求方法**: `PUT`
**接口路径**: `/api/model/delete`
**请求参数**: 
- `file`: 要删除的模型文件名
'''
@app.route('/api/model/delete', methods=['PUT'])
def delete_model():
    try:
        filename = request.args.get('file')
        if filename:
            ret = sp.delete_model(filename)
            if ret == True:
                return jsonify({"status": "success", "message": "Model file deleted successfully"}), 200
            else:
                return jsonify({"status": "error", "message": "Model file deletion failed"}), 500
        else:
            return jsonify({"status": "error", "message": "Missing parameter: file"}), 400
    except Exception as e:
        print('delete_model: ', e)
    except:
        print('delete_model: Unknown error')
    return jsonify({"status": "error", "message": "Unknown error"}), 500

'''
## 任务测试
**描述**: 输入预制信息编号 返回JPEG图像数据。
**请求方法**: `GET`
**接口路径**: `/api/task/test`
**请求参数**: 
- `preset_id`: 预制信息编号
'''
@app.route('/api/task/test', methods=['GET'])
def task_test():
    try:
        preset_id = request.args.get('preset_id')
        if preset_id:
            if debug != True:
                ret = manger.call_frame_capture(preset_id)
                if manger.capture_construct_img is not None:
                    img_data = cv2.imencode('.jpg', manger.capture_construct_img)[1].tostring()
                    return Response(img_data, mimetype='image/jpeg')
                elif manger.capture_thermal_img is not None and manger.capture_source_img is None:
                    img_data = cv2.imencode('.jpg', manger.capture_thermal_img)[1].tostring()
                    return Response(img_data, mimetype='image/jpeg')
                elif manger.capture_source_img is not None:
                    img_data = cv2.imencode('.jpg', manger.capture_source_img)[1].tostring()
                    return Response(img_data, mimetype='image/jpeg')
                else:
                    return jsonify({"status": "error", "message": "Failed to get image"}), 500
            else:
                return jsonify({"status": "success", "message": "Task executed successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Missing parameter: preset_id"}), 400
    except Exception as e:
        print('task_test: ', e)
    except:
        print('task_test: Unknown error')
    return jsonify({"status": "error", "message": "Unknown error"}), 500

'''
**描述**: 输入预制信息编号，执行任务。
**请求方法**: `POST`
**接口路径**: `/api/task/execute`
**请求参数**: 
- `preset_id`: 预制信息编号
'''
@app.route('/api/task/execute', methods=['POST'])
def task_execute():
    try:
        preset_id = request.args.get('preset_id')
        if preset_id:
            if debug != True:
                ret = manger.call_preset(preset_id)
                if ret == True:
                    return jsonify({"status": "success", "message": "Task executed successfully"}), 200
                else:
                    return jsonify({"status": "error", "message": "Task execution failed"}), 500
            else:
                return jsonify({"status": "success", "message": "Task executed successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Missing parameter: preset_id"}), 400
    except Exception as e:
        print('task_execute: ', e)
    except:
        print('task_execute: Unknown error')
    return jsonify({"status": "error", "message": "Unknown error"}), 500


class Hello(Resource):
    @staticmethod
    def get():
        return "[get] hello flask"

    @staticmethod
    def post():
        return "[post] hello flask"


api.add_resource(Hello, '/hello')

if __name__ == "__main__":
    # app.run(host='127.0.0.1', debug=True, port=8010)
    app.run(host='0.0.0.0', debug=True, port=8010)

    if debug != True:
        manger.exit_system()
