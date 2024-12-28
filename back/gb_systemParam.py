import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

ROOT_PATH = '/home/ljl/share/Config/'
MODEL_PATH = ROOT_PATH + 'model/'
PRESET_PATH = ROOT_PATH + 'preset/'
SYSTEM_PATH = ROOT_PATH + 'system/'

def get_error_xml(code: int, message: str) -> str:
    '''
    生成错误xml字符串
    '''
    return f'<?xml version="1.0" encoding="UTF-8"?><Error><code>{code}</code><message>{message}</message></Error>'

def get_yuntaiParam() -> str:
    '''
    获取云台参数
        参数文件: SYSTEM_PATH + yuntai.xml
        参数内容:
        <?xml version="1.0" encoding="UTF-8"?>
        <Yuntai>
            <class>1</class>    // 云台类型 1: 大立云台 2: 海康云台
            <ip>192.168.xx.xx</ip>    // 云台IP地址
            <username>admin</username>    // 云台用户名
            <password>Admin123</password>    // 云台密码
            <need_ir_ip>1</need_ir_ip>    // 是否需要红外设备IP地址 1: 需要 0: 不需要
            <ir_ip>192.168.xx.xx</ir_ip>    // 大立云台 红外设备 IP地址
            <username_ir>admin</username_ir>    // 大立云台 红外设备 用户名
            <password_ir>Admin123</password_ir>    // 大立云台 红外设备 密码
        </Yuntai>
    返回 xml字符串
        若成功 返回xml文件内容
        若失败 返回xml:
        <?xml version="1.0" encoding="UTF-8"?>
        <Yuntai>
            <code>404</code>
            <message>File not found</message>
        </Yuntai>
    '''
    # 判断文件是否存在
    if not os.path.exists(SYSTEM_PATH + 'yuntai.xml'):
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>404</code><message>File not found</message></Error>'
    try:
        # 读取文件
        tree = ET.parse(SYSTEM_PATH + 'yuntai.xml')
        root = tree.getroot()
        return ET.tostring(root, encoding='utf-8', method='xml').decode()
    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def set_yuntaiParam(data: str) -> str:
    '''
    设置云台参数
        输入参数内容：
        参数内容:
        <?xml version="1.0" encoding="UTF-8"?>
        <Yuntai>
            <class>1</class>    // 云台类型 1: 大立云台 2: 海康云台
            <ip>192.168.xx.xx</ip>    // 云台IP地址
            <username>admin</username>    // 云台用户名
            <password>Admin123</password>    // 云台密码
            <need_ir_ip>1</need_ir_ip>    // 是否需要红外设备IP地址 1: 需要 0: 不需要
            <ir_ip>192.168.xx.xx</ir_ip>    // 大立云台 红外设备 IP地址
            <username_ir>admin</username_ir>    // 大立云台 红外设备 用户名
            <password_ir>Admin123</password_ir>    // 大立云台 红外设备 密码
        </Yuntai>
    返回 xml字符串
        若成功 返回: 
        <?xml version="1.0" encoding="UTF-8"?>
        <Yuntai>
            <code>200</code>
            <message>Success</message>
        </Yuntai>
        若失败 返回 设置失败信息:
        <?xml version="1.0" encoding="UTF-8"?>
        <Yuntai>
            <code>500</code>
            <message>Internal Server Error</message>
        </Yuntai>
    '''
    
    try:
        # 解析输入的xml 参数
        param_class = ''
        param_ip = ''
        param_username = ''
        param_password = ''
        param_need_ir_ip = ''
        param_ir_ip = ''
        param_username_ir = ''
        param_password_ir = ''
        root = ET.fromstring(data)
        for child in root:
            if child.tag == 'class':
                param_class = child.text
            elif child.tag == 'ptzClass':
                param_class = child.text
            elif child.tag == 'ip':
                param_ip = child.text
            elif child.tag == 'username':
                param_username = child.text
            elif child.tag == 'password':
                param_password = child.text
            elif child.tag == 'need_ir_ip':
                param_need_ir_ip = child.text
            elif child.tag == 'ir_ip':
                param_ir_ip = child.text
            elif child.tag == 'username_ir':
                param_username_ir = child.text
            elif child.tag == 'password_ir':
                param_password_ir = child.text
        # 判断参数是否完整
        if param_class == '' or param_ip == '' or param_username == '' or param_password == '' or param_need_ir_ip == '' or param_ir_ip == '' or param_username_ir == '' or param_password_ir == '':
            return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
        # 生成xml文件
        root = ET.Element('Yuntai')
        ET.SubElement(root, 'class').text = param_class
        ET.SubElement(root, 'ip').text = param_ip
        ET.SubElement(root, 'username').text = param_username
        ET.SubElement(root, 'password').text = param_password
        ET.SubElement(root, 'need_ir_ip').text = param_need_ir_ip
        ET.SubElement(root, 'ir_ip').text = param_ir_ip
        ET.SubElement(root, 'username_ir').text = param_username_ir
        ET.SubElement(root, 'password_ir').text = param_password_ir
        tree = ET.ElementTree(root)
        # print("xml_data:")
        # 写入文件
        # 将XML转换为字符串并增加换行和缩进
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

        # 写入文件
        with open(SYSTEM_PATH + 'yuntai.xml', 'w', encoding='utf-8') as f:
            f.write(pretty_xml_as_string)

    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'


def get_offsetParam() -> str:
    '''
    获取偏移参数
        参数文件: SYSTEM_PATH + offset.xml
        参数内容:
        <?xml version="1.0" encoding="UTF-8"?>
        <Offset>
            <x_offset>0.1</x_offset>    // x位置偏移
            <y_offset>0.1</y_offset>    // y位置偏移
            <w_coefficient>0.9</w_coefficient>  // 宽度系数
            <h_coefficient>0.9</h_coefficient>  // 高度系数
            <x_rect>0.2</x_rect>    // 测温时 x坐标在正负x_rect之间
            <y_rect>0.2</y_rect>    // 测温时 y坐标在正负y_rect之间
            <x_min>0.34</x_min>     // 红外视角在高清视角中左边沿
            <y_min>0.18</y_min>     // 红外视角在高清视角中上边沿
            <x_max>0.80</x_max>     // 红外视角在高清视角中右边沿
            <y_max>0.78</y_max>     // 红外视角在高清视角中下边沿
        </Offset>
    返回 xml字符串
        若成功 返回xml文件内容:
        若失败 返回错误信息:
        <?xml version="1.0" encoding="UTF-8"?>
        <Offset>
            <code>404</code>
            <message>File not found</message>
        </Offset>
    '''
    # 判断文件是否存在
    if not os.path.exists(SYSTEM_PATH + 'offset.xml'):
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>404</code><message>File not found</message></Error>'
    # 读取文件
    try:
        tree = ET.parse(SYSTEM_PATH + 'offset.xml')
        root = tree.getroot()
        return ET.tostring(root, encoding='utf-8', method='xml').decode()
    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    
def set_offsetParam(data: str) -> str:
    '''
    设置偏移参数
        输入参数内容： xml
        <?xml version="1.0" encoding="UTF-8"?>
        <Offset>
            <x_offset>0.1</x_offset>    // x位置偏移
            <y_offset>0.1</y_offset>    // y位置偏移
            <w_coefficient>0.9</w_coefficient>  // 宽度系数
            <h_coefficient>0.9</h_coefficient>  // 高度系数
            <x_rect>0.2</x_rect>    // 测温时 x坐标在正负x_rect之间
            <y_rect>0.2</y_rect>    // 测温时 y坐标在正负y_rect之间
            <x_min>0.34</x_min>     // 红外视角在高清视角中左边沿
            <y_min>0.18</y_min>     // 红外视角在高清视角中上边沿
            <x_max>0.80</x_max>     // 红外视角在高清视角中右边沿
            <y_max>0.78</y_max>     // 红外视角在高清视角中下边沿
        </Offset>
    返回 xml字符串
        若成功 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Offset>
            <code>200</code>
            <message>Success</message>
        </Offset>
        若失败 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Offset>
            <code>500</code>
            <message>Internal Server Error</message>
        </Offset>
    '''
    try:
        # 解析输入的xml 参数
        param_x_offset = ''
        param_y_offset = ''
        param_w_coefficient = ''
        param_h_coefficient = ''
        param_x_rect = ''
        param_y_rect = ''
        param_x_min = ''
        param_y_min = ''
        param_x_max = ''
        param_y_max = ''
        root = ET.fromstring(data)
        for child in root:
            if child.tag == 'x_offset':
                param_x_offset = child.text
            elif child.tag == 'y_offset':
                param_y_offset = child.text
            elif child.tag == 'w_coefficient':
                param_w_coefficient = child.text
            elif child.tag == 'h_coefficient':
                param_h_coefficient = child.text
            elif child.tag == 'x_rect':
                param_x_rect = child.text
            elif child.tag == 'y_rect':
                param_y_rect = child.text
            elif child.tag == 'x_min':
                param_x_min = child.text
            elif child.tag == 'y_min':
                param_y_min = child.text
            elif child.tag == 'x_max':
                param_x_max = child.text
            elif child.tag == 'y_max':
                param_y_max = child.text
        # 判断参数是否完整
        if param_x_offset == '' or param_y_offset == '' or param_w_coefficient == '' or param_h_coefficient == '' or param_x_rect == '' or param_y_rect == '' or param_x_min == '' or param_y_min == '' or param_x_max == '' or param_y_max == '':
            return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
        # 生成xml文件
        root = ET.Element('Offset')
        ET.SubElement(root, 'x_offset').text = param_x_offset
        ET.SubElement(root, 'y_offset').text = param_y_offset
        ET.SubElement(root, 'w_coefficient').text = param_w_coefficient
        ET.SubElement(root, 'h_coefficient').text = param_h_coefficient
        ET.SubElement(root, 'x_rect').text = param_x_rect
        ET.SubElement(root, 'y_rect').text = param_y_rect
        ET.SubElement(root, 'x_min').text = param_x_min
        ET.SubElement(root, 'y_min').text = param_y_min
        ET.SubElement(root, 'x_max').text = param_x_max
        ET.SubElement(root, 'y_max').text = param_y_max

        # 将XML转换为字符串并增加换行和缩进
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

        # 写入文件
        with open(SYSTEM_PATH + 'offset.xml', 'w', encoding='utf-8') as f:
            f.write(pretty_xml_as_string)
        return '<?xml version="1.0" encoding="UTF-8"?><Offset><code>200</code><message>Success</message></Offset>'
    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    
def get_ptzcontrolParam() -> str:
    '''
    获取云台控制参数:
        参数文件: SYSTEM_PATH + yuntai_move.xml
        参数内容:
        <?xml version="1.0" encoding="UTF-8"?>
        <Control>
            <x_reversal>0</x_reversal>    // x轴反向 0: 不反向 1: 反向
            <y_reversal>0</y_reversal>    // y轴反向 0: 不反向 1: 反向
            <x_maxSpeed>200.0</x_maxSpeed>    // x轴最大速度
            <y_maxSpeed>200.0</y_maxSpeed>    // y轴最大速度
            <x_kp>100.0</x_kp>    // x轴P参数
            <x_ki>1.0</x_ki>    // x轴I参数
            <x_kd>10.0</x_kd>    // x轴D参数
            <y_kp>100.0</y_kp>    // y轴P参数
            <y_ki>1.0</y_ki>    // y轴I参数
            <y_kd>10.0</y_kd>    // y轴D参数
        </Control>
    返回 xml字符串
        若成功 返回xml文件内容
        若失败 返回错误信息:
        <?xml version="1.0" encoding="UTF-8"?>
        <Control>
            <code>404</code>
            <message>File not found</message>
        </Control>
    '''
    # 判断文件是否存在
    if not os.path.exists(SYSTEM_PATH + 'yuntai_move.xml'):
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>404</code><message>File not found</message></Error>'
    try:
        # 读取文件
        tree = ET.parse(SYSTEM_PATH + 'yuntai_move.xml')
        root = tree.getroot()
        return ET.tostring(root, encoding='utf-8', method='xml').decode()
    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    
def set_ptzcontrolParam(data: str) -> str:
    '''
    设置云台控制参数
        输入参数内容： xml
        <?xml version="1.0" encoding="UTF-8"?>
        <Control>
            <x_reversal>0</x_reversal>    // x轴反向 0: 不反向 1: 反向
            <y_reversal>0</y_reversal>    // y轴反向 0: 不反向 1: 反向
            <x_maxSpeed>200.0</x_maxSpeed>    // x轴最大速度
            <y_maxSpeed>200.0</y_maxSpeed>    // y轴最大速度
            <x_kp>100.0</x_kp>    // x轴P参数
            <x_ki>1.0</x_ki>    // x轴I参数
            <x_kd>10.0</x_kd>    // x轴D参数
            <y_kp>100.0</y_kp>    // y轴P参数
            <y_ki>1.0</y_ki>    // y轴I参数
            <y_kd>10.0</y_kd>    // y轴D参数
        </Control>
    返回 xml字符串
        若成功 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Control>
            <code>200</code>
            <message>Success</message>
        </Control>
        若失败 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Control>
            <code>500</code>
            <message>Internal Server Error</message>
        </Control>
    '''
    try:
        # 解析输入的xml 参数
        param_x_reversal = ''
        param_y_reversal = ''
        param_x_maxSpeed = ''
        param_y_maxSpeed = ''
        param_x_kp = ''
        param_x_ki = ''
        param_x_kd = ''
        param_y_kp = ''
        param_y_ki = ''
        param_y_kd = ''
        root = ET.fromstring(data)
        for child in root:
            if child.tag == 'x_reversal':
                param_x_reversal = child.text
            elif child.tag == 'y_reversal':
                param_y_reversal = child.text
            elif child.tag == 'x_maxSpeed':
                param_x_maxSpeed = child.text
            elif child.tag == 'y_maxSpeed':
                param_y_maxSpeed = child.text
            elif child.tag == 'x_kp':
                param_x_kp = child.text
            elif child.tag == 'x_ki':
                param_x_ki = child.text
            elif child.tag == 'x_kd':
                param_x_kd = child.text
            elif child.tag == 'y_kp':
                param_y_kp = child.text
            elif child.tag == 'y_ki':
                param_y_ki = child.text
            elif child.tag == 'y_kd':
                param_y_kd = child.text
        # 判断参数是否完整
        if param_x_reversal == '' or param_y_reversal == '' or param_x_maxSpeed == '' or param_y_maxSpeed == '' or param_x_kp == '' or param_x_ki == '' or param_x_kd == '' or param_y_kp == '' or param_y_ki == '' or param_y_kd == '':
            return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
        # 生成xml文件
        root = ET.Element('Control')
        ET.SubElement(root, 'x_reversal').text = param_x_reversal
        ET.SubElement(root, 'y_reversal').text = param_y_reversal
        ET.SubElement(root, 'x_maxSpeed').text = param_x_maxSpeed
        ET.SubElement(root, 'y_maxSpeed').text = param_y_maxSpeed
        ET.SubElement(root, 'x_kp').text = param_x_kp
        ET.SubElement(root, 'x_ki').text = param_x_ki
        ET.SubElement(root, 'x_kd').text = param_x_kd
        ET.SubElement(root, 'y_kp').text = param_y_kp
        ET.SubElement(root, 'y_ki').text = param_y_ki
        ET.SubElement(root, 'y_kd').text = param_y_kd
        tree = ET.ElementTree(root)
        # 写入文件
        tree.write(SYSTEM_PATH + 'yuntai_move.xml', encoding='utf-8')
        return '<?xml version="1.0" encoding="UTF-8"?><Control><code>200</code><message>Success</message></Control>'
    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'
    
def get_presetlistParam() -> str:
    '''
    获取预制信息列表
        参数目录: PRESET_PATH
            1 检索目录下所有命名为num.xml的文件
            2 生成应答信息
        返回 xml字符串:
        <?xml version="1.0" encoding="UTF-8"?>
        <PresetList>
            <PresetNum>n</PresetNum>
            <Items>
                <Item id="0" preset_name="yuntai" modle_name="xx.pt" ir_model_name="xx.pt" cla_id="0,1,2" cla_name="xx,xx,xx" 
                score_val="0.5,0.5,0.5" object_id="0" ir_object_id="0" location="0,0" image_channel="0" isRunIrModel="0" isControlPtz="0" thermal_num="3" />
                ...
            </Items>
        </PresetList>
    '''
    try:
        # 获取文件列表
        file_list = os.listdir(PRESET_PATH)
        # 只保留名字为 数字.xml 的文件
        for file in file_list:
            file_split = file.split('.')
            if len(file_split) != 2:
                file_list.remove(file)
                continue
            if file_split[1] != 'xml':
                file_list.remove(file)
                continue
            if not file_split[0].isdigit():
                file_list.remove(file)
                continue
        # print(file_list)
        # 生成xml文件
        root = ET.Element('PresetList')
        ET.SubElement(root, 'PresetNum').text = str(len(file_list))
        items = ET.SubElement(root, 'Items')
        for file in file_list:
            tree = ET.parse(os.path.join(PRESET_PATH, file))
            preset_root = tree.getroot()
            item = ET.SubElement(items, 'Item')
            file_split = file.split('.')
            modle_path = preset_root.find('modle_path').text
            modle_name = modle_path.split('/')[-1]
            ir_modle_path = preset_root.find('ir_model_path').text
            ir_modle_name = ir_modle_path.split('/')[-1]
            
            # 解析 <classes> 元素
            classes = preset_root.find('classes')
            cla_id = []
            cla_name = []
            for class_item in classes.findall('Item'):
                cla_id.append(class_item.get('id'))
                cla_name.append(class_item.get('value'))
            
            # 解析 <score> 元素
            score = preset_root.find('score')
            score_val = []
            for score_item in score.findall('Item'):
                score_val.append(score_item.get('value'))
            
            item.set('id', file_split[0])
            item.set('preset_name', preset_root.find('preset_name').text)
            item.set('model_name', modle_name)
            item.set('ir_model_name', ir_modle_name)
            # print('ir_model_name:', ir_modle_name)
            item.set('cla_id', ','.join(cla_id))
            item.set('cla_name', ','.join(cla_name))
            item.set('score_val', ','.join(score_val))
            item.set('object_id', preset_root.find('object_id').text)
            item.set('ir_object_id', preset_root.find('ir_object_id').text)
            location = preset_root.find('location').find('Item')
            item.set('location', f"{location.get('x')},{location.get('y')}")
            item.set('image_channel', preset_root.find('image_channel').text)
            item.set('isRunIrModel', preset_root.find('isRunIrModel').text)
            item.set('isControlPtz', preset_root.find('isControlPtz').text)
            item.set('thermal_num', preset_root.find('tempture_num').text)

        return ET.tostring(root, encoding='utf-8').decode('utf-8')

    except Exception as e:
        print ('获取预制信息列表错误:', e)
    except :
        print ('获取预制信息列表 未知错误')
    return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def get_presetInfo(data: int) -> str:
    '''
    返回xml内容:
    <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <preset_name>xx</preset_name>
            <model_name>xx.pt</model_name>
            <ir_model_name>xx.pt</ir_model_name>
            <classes>
                <Item id="0" value="xx" />
                ...
            </classes>
            <score>
                <Item value="0.5" />
                ...
            </score>
            <object_id>0</object_id>
            <ir_object_id>0</ir_object_id>
            <location>
                <Item x="0" y="0" />
            </location>
            <image_channel>0</image_channel>
            <isRunIrModel>0</isRunIrModel>
            <isControlPtz>0</isControlPtz>
            <tempture_num>3</tempture_num>
        </Preset>
    '''
    # 打开对应的文件
    try:
        filename = PRESET_PATH + str(data) + '.xml'
        tree = ET.parse(filename)
        preset_root = tree.getroot()
        # 读取对应的信息
        modle_path = preset_root.find('modle_path').text
        modle_name = modle_path.split('/')[-1]
        ir_modle_path = preset_root.find('ir_model_path').text
        ir_modle_name = ir_modle_path.split('/')[-1]
        # 生成xml文件
        root = ET.Element('Preset')
        ET.SubElement(root, 'preset_name').text = preset_root.find('preset_name').text
        ET.SubElement(root, 'model_name').text = modle_name
        ET.SubElement(root, 'ir_model_name').text = ir_modle_name

        classes = ET.SubElement(root, 'classes')
        for item in preset_root.find('classes').findall('Item'):
            ET.SubElement(classes, 'Item', id=item.get('id'), value=item.get('value'))

        score = ET.SubElement(root, 'score')
        for item in preset_root.find('score').findall('Item'):
            ET.SubElement(score, 'Item', value=item.get('value'))

        ET.SubElement(root, 'object_id').text = preset_root.find('object_id').text
        ET.SubElement(root, 'ir_object_id').text = preset_root.find('ir_object_id').text

        location = ET.SubElement(root, 'location')
        for item in preset_root.find('location').findall('Item'):
            ET.SubElement(location, 'Item', x=item.get('x'), y=item.get('y'))

        ET.SubElement(root, 'image_channel').text = preset_root.find('image_channel').text
        ET.SubElement(root, 'isRunIrModel').text = preset_root.find('isRunIrModel').text
        ET.SubElement(root, 'isControlPtz').text = preset_root.find('isControlPtz').text
        ET.SubElement(root, 'tempture_num').text = preset_root.find('tempture_num').text

        return ET.tostring(root, encoding='utf-8').decode('utf-8')

    except Exception as e:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>404</code><message>File not found</message></Error>'
    except:
        return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def add_presetInfo(data: str) -> str:
    '''
    添加一条预制信息
        输入参数内容： xml
        <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <preset_name>xx</preset_name>
            <model_path>xx.pt</model_path>
            <ir_model_path>xx.pt</ir_model_path>
            <classes>
                <Item id="0" value="xx" />
                ...
            </classes>
            <score>
                <Item value="0.5" />
                ...
            </score>
            <object_id>0</object_id>
            <ir_object_id>0</ir_object_id>
            <location>
                <Item x="0" y="0" />
            </location>
            <image_channel>0</image_channel>
            <isRunIrModel>0</isRunIrModel>
            <isControlPtz>0</isControlPtz>
            <tempture_num>3</tempture_num>
        </Preset>
    返回 xml字符串
        若成功 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <code>200</code>
            <message>Success</message>
        </Preset>
        若失败 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <code>500</code>
            <message>Internal Server Error</message>
        </Preset>
    '''
    # 解析xml数据
    try :
        param_preset_name = ''
        param_modle_path = ''
        param_ir_modle_path = ''
        param_classes = []
        param_score = []
        param_object_id = ''
        param_ir_object_id = ''
        param_location = None
        param_image_channel = ''
        param_isRunIrModel = ''
        param_isControlPtz = ''
        param_tempture_num = ''
        root = ET.fromstring(data)
        for child in root:
            if child.tag == 'preset_name':                      # 预置信息名称
                param_preset_name = child.text
            elif child.tag == 'model_path':                     # 模型路径
                param_modle_path = child.text
            elif child.tag == 'ir_model_path':                  # 红外模型路径
                param_ir_modle_path = child.text
            elif child.tag == 'classes':                        # 类别
                param_classes = []
                # 解析items
                for item in child:
                    if item.tag == 'Item':
                        value = item.attrib['value']
                        param_classes.append(value)
            elif child.tag == 'score':                          # 置信度
                param_score = []
                # 解析items
                for item in child:
                    if item.tag == 'Item':
                        value = item.attrib['value']
                        param_score.append(value)
            elif child.tag == 'object_id':                      # 检测对象ID
                param_object_id = child.text
            elif child.tag == 'ir_object_id':
                param_ir_object_id = child.text
            elif child.tag == 'location':                       # 搜索位置
                param_location = (0, 0)
                # 解析items
                for item in child:
                    if item.tag == 'Item':
                        x_value = item.attrib['x']
                        y_value = item.attrib['y']
                        param_location = (x_value, y_value)   
            elif child.tag == 'image_channel':                  # 图像通道
                param_image_channel = child.text
            elif child.tag == 'isRunIrModel':                   # 是否运行红外模型
                param_isRunIrModel = child.text
            elif child.tag == 'isControlPtz':                   # 是否控制云台
                param_isControlPtz = child.text
            elif child.tag == 'tempture_num':                   # 测温次数
                param_tempture_num = child.text
        # 判断参数是否完整
        if (param_preset_name == '' or param_modle_path == '' or param_ir_modle_path == '' or len(param_classes) == 0 or len(param_score) == 0 
                or param_object_id == '' or param_location == None or param_image_channel == '' or param_isRunIrModel == ''
                or param_isControlPtz == '' or param_tempture_num == '' or param_ir_object_id == ''):
            return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
        # 获取预制信息文件列表 从而生成新文件的名字
        file_list = os.listdir(PRESET_PATH)
        # 只保留名字为 数字.xml 的文件
        for file in file_list:
            file_split = file.split('.')
            if len(file_split) != 2:
                file_list.remove(file)
                continue
            if file_split[1] != 'xml':
                file_list.remove(file)
                continue
            if not file_split[0].isdigit():
                file_list.remove(file)
                continue
        # 生成新文件名
        file_id_list = []
        for file in file_list:
            file_id_list.append(int(file.split('.')[0]))
        max_id = max(file_id_list)
        new_id = max_id + 1
        new_file_name = str(new_id) + '.xml'
        # 生成xml文件
        root = ET.Element('Preset')
        ET.SubElement(root, 'preset_name').text = param_preset_name
        ET.SubElement(root, 'modle_path').text = MODEL_PATH + param_modle_path
        ET.SubElement(root, 'ir_model_path').text = MODEL_PATH + param_ir_modle_path
        classes = ET.SubElement(root, 'classes')
        for i in range(len(param_classes)):
            ET.SubElement(classes, 'Item', id=str(i), value=param_classes[i])
        score = ET.SubElement(root, 'score')
        for i in range(len(param_score)):
            ET.SubElement(score, 'Item', id=str(i), value=param_score[i])
        ET.SubElement(root, 'object_id').text = param_object_id
        ET.SubElement(root, 'ir_object_id').text = param_ir_object_id
        location = ET.SubElement(root, 'location')
        ET.SubElement(location, 'Item', x=str(param_location[0]), y=str(param_location[1]))
        ET.SubElement(root, 'image_channel').text = param_image_channel
        ET.SubElement(root, 'isRunIrModel').text = param_isRunIrModel
        ET.SubElement(root, 'isControlPtz').text = param_isControlPtz
        ET.SubElement(root, 'tempture_num').text = param_tempture_num
        tree = ET.ElementTree(root)
        # 写入文件
        tree.write(PRESET_PATH + new_file_name, encoding='utf-8')
        return '<?xml version="1.0" encoding="UTF-8"?><Preset><code>200</code><message>Success</message></Preset>'

    except Exception as e:
        print ('添加预制信息错误:', e)
    except :
        print ('添加预制信息 未知错误')
    return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def remove_presetInfo(data: int) -> str:
    '''
    删除预制信息
        输入 预制信息编号 int
        返回 xml字符串
            若成功 返回:
            <?xml version="1.0" encoding="UTF-8"?>
            <Preset>
                <code>200</code>
                <message>Success</message>
            </Preset>
            若失败 返回:
            <?xml version="1.0" encoding="UTF-8"?>
            <Preset>
                <code>500</code>
                <message>Internal Server Error</message>
            </Preset>
    '''
    try:
        # 删除文件
        file_name = str(data) + '.xml'
        os.remove(PRESET_PATH + file_name)
        # 将剩余文件编号重新排序
        file_list = os.listdir(PRESET_PATH)
        # 只保留名字为 数字.xml 的文件
        for file in file_list:
            file_split = file.split('.')
            if len(file_split) != 2:
                file_list.remove(file)
                print('remove file: ', file, ' because of len(file_split) != 2')
                continue
            if file_split[1] != 'xml':
                file_list.remove(file)
                print('remove file: ', file, ' because of file_split[1] != xml')
                continue
            if not file_split[0].isdigit():
                file_list.remove(file)
                print('remove file: ', file, ' because of not file_split[0].isdigit()')
                continue
        # 按照文件名字重新排序
        file_list.sort(key=lambda x: int(x.split('.')[0]))
        # 重新命名
        for i in range(len(file_list)):
            file_id = int(file_list[i].split('.')[0])
            if file_id > data:
                new_file_name = str(file_id - 1) + '.xml'
                os.rename(PRESET_PATH + file_list[i], PRESET_PATH + new_file_name)
        return '<?xml version="1.0" encoding="UTF-8"?><Preset><code>200</code><message>Success</message></Preset>'
    except Exception as e:
        print ('删除预制信息错误:', e)
    except :
        print ('删除预制信息 未知错误')
    return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def set_presetlistParam(data: str) -> str:
    '''
    设置预制信息列表
        输入参数内容： xml
        <?xml version="1.0" encoding="UTF-8"?>
        <PresetList>
            <PresetNum>n</PresetNum>
            <Items>
                <Item id="0" preset_name="yuntai" modle_name="xx.pt" ir_model_name="xx.pt" cla_id="0,1,2" cla_name="xx,xx,xx" 
                score_val="0.5,0.5,0.5" object_id="0" location="0,0" image_channel="0" isRunIrModel="0" isControlPtz="0" thermal_num="3" />
                ...
            </Items>
        </PresetList>
    返回 xml字符串
        若成功 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <PresetList>
            <code>200</code>
            <message>Success</message>
        </PresetList>
        若失败 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <PresetList>
            <code>500</code>
            <message>Internal Server Error</message>
        </PresetList>
    '''
    try:
        # 解析xml数据
        param_preset_num = ''
        param_items = []
        root = ET.fromstring(data)
        for child in root:
            if child.tag == 'PresetNum':
                param_preset_num = child.text
            elif child.tag == 'Items':
                param_items = []
                for item in child:
                    param_item = {}
                    param_item['id'] = item.attrib['id']
                    param_item['preset_name'] = item.attrib['preset_name']
                    param_item['modle_name'] = item.attrib['modle_name']
                    param_item['ir_modle_name'] = item.attrib['ir_modle_name']
                    param_item['cla_id'] = item.attrib['cla_id']
                    param_item['cla_name'] = item.attrib['cla_name']
                    param_item['score_val'] = item.attrib['score_val']
                    param_item['object_id'] = item.attrib['object_id']
                    param_item['location'] = item.attrib['location']
                    param_item['image_channel'] = item.attrib['image_channel']
                    param_item['isRunIrModel'] = item.attrib['isRunIrModel']
                    param_item['isControlPtz'] = item.attrib['isControlPtz']
                    param_item['thermal_num'] = item.attrib['thermal_num']
                    param_items.append(param_item)
        # 判断参数是否完整
        if param_preset_num == '' or len(param_items) == 0:
            return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
        # 删除原有文件
        file_list = os.listdir(PRESET_PATH)
        # 只保留名字为 数字.xml 的文件
        for file in file_list:
            file_split = file.split('.')
            if len(file_split) != 2:
                file_list.remove(file)
                continue
            if file_split[1] != 'xml':
                file_list.remove(file)
                continue
            if not file_split[0].isdigit():
                file_list.remove(file)
                continue
        for file in file_list:
            os.remove(PRESET_PATH + file)
        # 生成新文件
        for item in param_items:
            root = ET.Element('Preset')
            ET.SubElement(root, 'preset_name').text = item['preset_name']
            ET.SubElement(root, 'modle_path').text = MODEL_PATH + item['modle_name']
            ET.SubElement(root, 'ir_modle_path').text = MODEL_PATH + item['ir_modle_name']
            classes = ET.SubElement(root, 'classes')
            cla_id = item['cla_id'].split(',')
            cla_name = item['cla_name'].split(',')
            for i in range(len(cla_id)):
                ET.SubElement(classes, 'Item', id=cla_id[i], value=cla_name[i])
            score = ET.SubElement(root, 'score')
            score_val = item['score_val'].split(',')
            for i in range(len(score_val)):
                ET.SubElement(score, 'Item', value=score_val[i])
            ET.SubElement(root, 'object_id').text = item['object_id']
            location = ET.SubElement(root, 'location')
            location_split = item['location'].split(',')
            ET.SubElement(location, 'Item', x=location_split[0], y=location_split[1])
            ET.SubElement(root, 'image_channel').text = item['image_channel']
            ET.SubElement(root, 'isRunIrModel').text = item['isRunIrModel']
            ET.SubElement(root, 'isControlPtz').text = item['isControlPtz']
            ET.SubElement(root, 'tempture_num').text = item['thermal_num']
            tree = ET.ElementTree(root)
            # 写入文件
            tree.write(PRESET_PATH + item['id'] + '.xml', encoding='utf-8')
        return '<?xml version="1.0" encoding="UTF-8"?><PresetList><code>200</code><message>Success</message></PresetList>'
    except Exception as e:
        print ('设置预制信息列表错误:', e)
    except :
        print ('设置预制信息列表 未知错误')
    return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def update_presetInfo(id :int, data: str) -> str:
    '''
    更新预制信息
        输入参数内容： xml
        <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <preset_name>xx</preset_name>
            <modle_path>xx.pt</modle_path>
            <ir_modle_path>xx.pt</ir_modle_path>
            <classes>
                <Item id="0" value="xx" />
                ...
            </classes>
            <score>
                <Item value="0.5" />
                ...
            </score>
            <object_id>0</object_id>
            <ir_object_id>0</ir_object_id>
            <location>
                <Item x="0" y="0" />
            </location>
            <image_channel>0</image_channel>
            <isRunIrModel>0</isRunIrModel>
            <isControlPtz>0</isControlPtz>
            <tempture_num>3</tempture_num>
        </Preset>
    返回 xml字符串
        若成功 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <code>200</code>
            <message>Success</message>
        </Preset>
        若失败 返回:
        <?xml version="1.0" encoding="UTF-8"?>
        <Preset>
            <code>500</code>
            <message>Internal Server Error</message>
        </Preset>
    '''
    try:
        # 判断是否存在该文件
        if not os.path.exists(PRESET_PATH + str(id) + '.xml'):
            return '<?xml version="1.0" encoding="UTF-8"?><Error><code>404</code><message>File not found</message></Error>'
        print('update_presetInfo:', data)
        # 解析xml数据
        param_preset_name = ''
        param_modle_name = ''
        param_ir_modle_name = ''
        param_classes = []
        param_score = []
        param_object_id = ''
        param_ir_object_id = ''
        param_location = None
        param_image_channel = ''
        param_isRunIrModel = ''
        param_isControlPtz = ''
        param_tempture_num = ''
        root = ET.fromstring(data)
        for child in root:
            if child.tag == 'preset_name':                    # 预置信息名称
                param_preset_name = child.text
            elif child.tag == 'model_path':                     # 模型路径
                param_modle_name = child.text
            elif child.tag == 'ir_model_path':                  # 红外模型路径
                param_ir_modle_name = child.text
            elif child.tag == 'classes':                        # 类别
                param_classes = []
                # 解析items
                for item in child:
                    if item.tag == 'Item':
                        value = item.attrib['value']
                        param_classes.append(value)
            elif child.tag == 'score':                          # 置信度
                param_score = []
                # 解析items
                for item in child:
                    if item.tag == 'Item':
                        value = item.attrib['value']
                        param_score.append(value)
            elif child.tag == 'object_id':                      # 检测对象ID
                param_object_id = child.text
            elif child.tag == 'ir_object_id':                   # 红外检测对象ID
                param_ir_object_id = child.text
            elif child.tag == 'location':                       # 搜索位置
                param_location = (0, 0)
                # 解析items
                for item in child:
                    if item.tag == 'Item':
                        x_value = item.attrib['x']
                        y_value = item.attrib['y']
                        param_location = (x_value, y_value)   
            elif child.tag == 'image_channel':                  # 图像通道
                param_image_channel = child.text
            elif child.tag == 'isRunIrModel':                   # 是否运行红外模型
                param_isRunIrModel = child.text
            elif child.tag == 'isControlPtz':                   # 是否控制云台
                param_isControlPtz = child.text
            elif child.tag == 'tempture_num':                   # 测温次数
                param_tempture_num = child.text
        # # 判断参数是否完整
        # if param_preset_name == '' or param_modle_name == '' or len(param_classes) == 0 or len(param_score) == 0 or param_object_id == '' or param_ir_object_id or param_location == None or param_image_channel == '' or param_tempture_num == '' or param_isRunIrModel == '' or param_isControlPtz == '' or param_ir_modle_name == '':
        #     print('param_preset_name:', param_preset_name)
        #     print('param_modle_name:', param_modle_name)
        #     print('param_classes:', len(param_classes))
        #     print('param_score:', len(param_score))
        #     print('param_object_id:', param_object_id)
        #     print('param_ir_object_id:', param_ir_object_id)
        #     print('param_location:', param_location)
        #     print('param_image_channel:', param_image_channel)
        #     print('param_tempture_num:', param_tempture_num)
        #     print('param_isRunIrModel:', param_isRunIrModel)
        #     print('param_isControlPtz:', param_isControlPtz)
        #     print('param_ir_modle_name:', param_ir_modle_name)
        #     return '<?xml version="1.0" encoding="UTF-8"?><Error><code>400</code><message>Bad Request</message></Error>'
        # 生成xml文件
        root = ET.Element('Preset')
        ET.SubElement(root, 'preset_name').text = param_preset_name
        ET.SubElement(root, 'modle_path').text = MODEL_PATH + param_modle_name
        ET.SubElement(root, 'ir_model_path').text = MODEL_PATH + param_ir_modle_name
        classes = ET.SubElement(root, 'classes')
        for i in range(len(param_classes)):
            ET.SubElement(classes, 'Item', id=str(i), value=param_classes[i])
        score = ET.SubElement(root, 'score')
        for i in range(len(param_score)):
            ET.SubElement(score, 'Item', id=str(i), value=param_score[i])
        ET.SubElement(root, 'object_id').text = param_object_id
        ET.SubElement(root, 'ir_object_id').text = param_ir_object_id
        location = ET.SubElement(root, 'location')
        ET.SubElement(location, 'Item', x=str(param_location[0]), y=str(param_location[1]))
        ET.SubElement(root, 'image_channel').text = param_image_channel
        ET.SubElement(root, 'isRunIrModel').text = param_isRunIrModel
        ET.SubElement(root, 'isControlPtz').text = param_isControlPtz
        ET.SubElement(root, 'tempture_num').text = param_tempture_num
        tree = ET.ElementTree(root)
        # 写入文件
        # 将XML转换为字符串并增加换行和缩进
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        with open(PRESET_PATH + str(id) + '.xml', 'w') as f:
            f.write(reparsed.toprettyxml(indent='    '))
            
        
        return '<?xml version="1.0" encoding="UTF-8"?><Preset><code>200</code><message>Success</message></Preset>'
    except Exception as e:
        print ('更新预制信息错误:', e)
    except :
        print ('更新预制信息 未知错误')
    return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'

def save_model(filename, file):
    '''
    保存模型文件：
        若文件已存在，覆盖原文件
        filename: 文件名
        file: request.files['file']
    '''
    try:
        # 获取全部模型文件列表
        file_list = os.listdir(MODEL_PATH)
        # 删除原有文件
        for osfile in file_list:
            if osfile == filename:
                os.remove(MODEL_PATH + filename)
        # 保存新文件
        file.save(MODEL_PATH + filename)
        return True
    except Exception as e:
        print ('保存模型文件错误:', e)
    except :
        print ('保存模型文件 未知错误')
    return False

def get_model_path(filename: str):
    '''
    获取模型文件路径
    '''
    # 判断模型路径下是否有该文件
    if not os.path.exists(MODEL_PATH + filename):
        return None
    return MODEL_PATH + filename

def delete_model(filename: str):
    '''
    删除模型文件
    '''
    try:
        # 获取全部模型文件列表
        file_list = os.listdir(MODEL_PATH)
        # 删除原有文件
        for osfile in file_list:
            if osfile == filename:
                os.remove(MODEL_PATH + filename)
        return True
    except Exception as e:
        print ('删除模型文件错误:', e)
    except :
        print ('删除模型文件 未知错误')
    return False

def get_modelList() -> str:
    '''
    获取模型文件列表
        返回 xml字符串:
        <?xml version="1.0" encoding="UTF-8"?>
        <ModelList>
            <ModelNum>n</ModelNum>
            <Items>
                <Item id="0" name="xx.pt" />
                ...
            </Items>
        </ModelList>
    '''
    try:
        # 获取全部模型文件列表
        file_list = os.listdir(MODEL_PATH)
        # 生成xml文件
        root = ET.Element('ModelList')
        ET.SubElement(root, 'ModelNum').text = str(len(file_list))
        items = ET.SubElement(root, 'Items')
        for i in range(len(file_list)):
            ET.SubElement(items, 'Item', id=str(i), name=file_list[i])
        return ET.tostring(root, encoding='utf-8').decode('utf-8')
    except Exception as e:
        print ('获取模型文件列表错误:', e)
    except :
        print ('获取模型文件列表 未知错误')
    return '<?xml version="1.0" encoding="UTF-8"?><Error><code>500</code><message>Internal Server Error</message></Error>'


