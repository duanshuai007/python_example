#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import sys
import os
import logging
import ssl
import paho.mqtt.client as mqtt
import queue
import threading
import time
import json
import copy
import random
import signal
import re
from threading import Timer

import config
from LoggingQueue import LoggingProducer, LoggingConsumer

class mqtt_client(mqtt.Client):
	logger = None

	def set_logger(self, logger):
		self.logger = logger

	def set_user_and_password(self, username, password):
		self.username_pw_set(username, password)

	def set_cafile(self, filename:str)->bool:
		try:
			if not os.path.exists(filename):
				self.logger.error("cafile is not exists")
				exit(1)
			self.tls_set(ca_certs=filename, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_1)
			self.tls_insecure_set(False)
			return True
		except Exception as e:
			self.logger.error("tls_set error:{}".format(e))
			return False

	def on_connect(self, mqttc, obj, flags, rc):
		#flags中的标志位能够知道此次连接时第一次连接还是短线后重连的
		self.logger.info("Connection returned result: " + mqtt.connack_string(rc))
		try:
			if rc == 0:
				self.logger.info("connect success")
				#when connect, subscribe topic
				#self.subscribe("#")
		except Exception as e:
			self.logger.error("on_connect error:{}".format(e))

	#执行mqttc.disconnect()主动断开连接会触发该函数
	#当因为什么原因导致客户端断开连接时也会触发该函数,ctrl-c停止程序不会触发该函数
	def on_disconnect(self, mqttc, obj, rc):
		mqttc.reconnect()

	'''
	mqttc:	the client instance for this callback
	obj:	the private user data as set in ``Client()`` or ``user_data_set()``
	msg:	an instance of MQTTMessage. This is a class with members ``topic``, ``payload``, ``qos``, ``retain``.
	'''
	def on_message(self, mqttc, obj, msg):
		try:
			json_msg = json.loads(str(msg.payload, encoding="utf-8"))
			self.logger.info("on message:" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
		except Exception as e:
			self.logger.error("on message exception:{}".format(e))

	def on_publish(self, mqttc, obj, mid):
		#重要，用来确认publish的消息发送出去了。有时即使publish返回成功，但消息却没有发送。
#		for item in self.delete_list:
#			if mid == item["mid"]:
#				self.logger.info("on publish remove msg, mid={}".format(mid))
#				self.delete_list.remove(item)
		pass

	def on_subscribe(self, mqttc, obj, mid, granted_qos):
		self.logger.info("Subscribed: " + " " + str(mid) + " " + str(granted_qos))
		try:
			pass
		except Exception as e:
			self.logger.error("on_subscribe error:{}".format(e))
	
	def on_unsubscribe(self, mqttc, obj, mid):
		self.logger.info("UnSubscribed: " + " " + str(mid))
		try:
			pass
		except Exception as e:
			self.logger.error("on_unsubscribe error:{}".format(e))

	'''
	def on_log(self, mqttc, obj, level, string):
		self.logger.info(string)
	'''

	def setsubscribe(self, topic=None, qos=0):
		self.sub_topic_list.append((topic, qos))

	def run(self, host=None, port=1883, keepalive=60):
		try:
			self.reconnect_delay_set(min_delay=10, max_delay=60)
			self.connect(host, port, keepalive)
			return True
		except Exception as e:
			self.logger.error("run mqtt error:{}".format(e))
			return False

def client_start():
	''' 
	client_id:  唯一用户id,不能和其他客户端有相同的。如果设置为None,则自动生成一个随机id,设置为None是clean_session必须为True
	clean_session:  设置为True时，当客户端断开broker会删除所有关于该客户端的信息.如果为False,客户端断开期间的消息会被保留。
	客户端断开时不会丢弃自己发送出的消息，调用connect或reconnect将导致消息重新发送。
	userdata=None   
	protocol=MQTTv311 or MQTTv31
	transport="tcp" or "websockets"
	'''
	LoggingConsumer()
	logger = LoggingProducer().get_default_logger()

	c = config.config("/home/duanshuai/mqttserver/config.ini")
	host = c.get("mqtt", "host")
	port = int(c.get("mqtt", "port"))
	user = c.get("mqtt", "username")
	passwd = c.get("mqtt", "userpassword")
	#cafile = c.get("MQTT", "CAFILE")

	mc = mqtt_client( clean_session = True, userdata = None, protocol = mqtt.MQTTv31, transport = 'tcp')
	mc.set_logger(logger)
	mc.set_user_and_password(user, passwd)
	#if mc.set_cafile(cafile) == False:
	#	exit(1)
	if mc.run(host=host, port=port, keepalive=120) == False:
		exit(1)
	mc.start_other_thread()
	mc.loop_forever()
