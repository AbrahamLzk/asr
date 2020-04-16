使用步骤：
	1. 请确认已安装Python包管理工具setuptools，请确认已安装requests和websocket-client，可通过“pip list”命令查看已安装列表。如果没有安装，请使用以下命令安装 
		pip install setuptools
		pip install requests
		pip install websocket-client
	2. 执行以下安装命令：
		python setup.py install
	3. 根据使用需求，选择demo文件夹对应的示例。参考注释，填写鉴权信息和参数信息，即可使用sdk。demo对应接口如下：
		一句话识别 & 录音文件识别 ： asr_customization_demo.py
		实时语音转写              ： rasr_demo.py
		短语音识别                ： asr_demo.py
		语音合成                  ： tts_demo.py
		定制语音合成              ： tts_customization_demo.py
	

说明：
	1. python sdk目前仅支持python3，暂不支持python2
	2. data文件夹下的示例音频可供参考使用。音频格式支持需要参考api文档。
	3. 相关参数不确定可以参考api文档，一般按照注释提示即可使用。格式、采样率等参数需要注意，不确定时务必参考api文档。需要精准填写才能正确识别。