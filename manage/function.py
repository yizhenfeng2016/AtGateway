#-*- coding:utf-8 -*-
__author__ = 'Administrator'
import re
from share import user
from share import logfile

def cmd_by_deviceorcombs_data(cmd):
        # print("come in cmd_by_device_data")
        try:
            cmd_list=re.split(",|，| |;|；",cmd)
            dev_class_type=""
            if len(cmd_list)==1 or len(cmd_list)==2 and cmd_list[0]!="":
                # combs_list=user.data_dict.get("combs",None)
                combs_list=user.get_data_dict("combs")
                control_name=cmd_list[0]
                dev_class_type="combs"
                if combs_list:
                    for cl in combs_list:
                        if cl.get("control_name",None)==control_name:
                             dev_class_type="combs"
            else:
                # device_list=user.data_dict.get("devices",None)
                device_list=user.get_data_dict("devices")
                room_name=cmd_list[0]
                dev_name=cmd_list[1]
                if device_list:
                    for dl in device_list:
                        if dl.get("device_name",None)==dev_name and dl.get("room_name",None)==room_name:
                            dev_class_type=dl.get("dev_class_type")
        except Exception as e:
            logfile.logger.exception(e.message)
        finally:
            return dev_class_type,cmd_list

def split_cmd(cmd):
    cmd_list=cmd.split('\n')
    return cmd_list

def dev_by_classtype(dev_list):
    try:
        classtype_list=[]
        if dev_list:
            for d in dev_list:
                if d:
                    if (d.get("dev_class_type")=="sensor_builtin" or #过滤不必要的设备
                        d.get("dev_class_type")=="coordin_zigbee" or
                        d.get("dev_class_type")=="safe_builtin" or
                        d.get("dev_class_type")=="coordin_bsp_speaker" or
                        d.get("dev_class_type")=="zigbee_builtin" or
                        d.get("dev_class_type")=="repeater" or
                        d.get("dev_class_type")=="central_air_dg"):
                        continue
                    else:
                        classtype_list.append(d.get("dev_class_type"))
        classtype_list=list(set(classtype_list))

        classtype_list=sorted(classtype_list)
        # print(classtype_list)
        devices_list=[]
        for c in classtype_list:
            temp_list=[]
            temp_dict={}
            for d in dev_list:
                if d.get("dev_class_type",None)==c:
                    room_name=d.get("room_name")
                    dev_name=d.get("device_name")
                    temp_list.append((room_name,dev_name))
            temp_dict[c]=temp_list
            devices_list.append(temp_dict)
    except Exception as e:
        logfile.logger.exception(e.message)
    finally:
        return devices_list,classtype_list

def search_devices_by_type(devices_list):
    """
    :param devices_list: []
    :return:[]
    """
    try:
        dev_list=[]
        if devices_list:
            for rec_dict in devices_list:
                if user.get_info_dict("PID")=="0002":
                    if rec_dict.get("device_type",None)=="gateway":
                        dev_list.append(rec_dict)
                elif user.get_info_dict("PID")=="0003":
                    if rec_dict.get("device_type",None)=="coordin_zigbee":
                        dev_list.append(rec_dict)
                elif user.get_info_dict("PID")=="0008":
                    if rec_dict.get("device_type",None)=="mirror":
                        dev_list.append(rec_dict)
    except Exception as e:
        logfile.logger.exception(e.message)
    finally:
        return dev_list