
import os
import yaml

processing_bigdata = ['HMaster','HRegionServer','HiveMetaStore','HiveServer2','NameNode','DataNode','SecondaryNameNode','Kafka','AlertPublisher','EventCatcherService',
                        'EmbeddedOozieServer','HistoryServer','JobHistoryServer','ResourceManager','QuorumPeerMain','LoadBalancer','HueServer']

processing_config = ""
for i in processing_bigdata:

    a = os.system("jps|grep %s" %i)
    if a == 0:
        processing_config+=i
        processing_config+=","

processing_config = processing_config[0:-1]

print("可用进程如为：%s" %processing_config)

print("开始替换配置文件中的roles的值")

with open("/export/software/bigdata/dh-monitorclient/config/application.yml") as f:

    doc = yaml.load(f)

    doc['datahouse']['roles'] = processing_config

with open("/export/software/bigdata/dh-monitorclient/config/application.yml", "w") as f:

    yaml.dump(doc, f)