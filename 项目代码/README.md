所有代码均在这,包括python、shell、SQL,均有注释

代码还没全部完成，会持续更新

```mathematica
├─CISS_OneMake # 工程名
│  │  tablenames.txt                               # 表清单，包括增量全量                                 
│  ├─Auto_Load_Data                                # 工程内的包名
│  │  ├─com
│  │  │  ├─alex
│  │  │  │  │  MainApp.py                          # 程序运行入口，核心调度运行的程序
│  │  │  │  ├─bean
│  │  │  │  │  │  ColumnMeta.py                    # Oracle列的信息对象：用于将列的名称、类型、注释进行封装
│  │  │  │  │  │  TableMeta.py                     # Oracle表的信息对象：用于将表的名称、列的信息、表的注释进行封装
│  │  │  │  ├─data_to_spark                        # 自动加载数据的主要代码的包名
│  │  │  │  │  │  CreateMetaCommon.py              # 定义了建表时固定的一些字符串数据，数据库名称、分层名称、文件类型属性等
│  │  │  │  │  │  CreateSparkTableFromOracle.py    # 自动创建SparkSQL数据库、以及获取Oracle表的信息创建SparkSQL表等
│  │  │  │  │  │  CreateSparkTablePartition.py     # 定义了建表时固定的一些字符串数据，数据库名称、分层名称、文件类型属性等
│  │  │  │  │  │  LoadIngDataToSeg.py              # 用于实现将Ingest的数据insert到Segmentation表中
│  │  │  │  │  ├─fileformat                        # 处理各种文件格式的脚本的包名
│  │  │  │  │  │  │  AvroTableProperties.py        # Avro文件格式对象，用于封装Avro建表时的字符串
│  │  │  │  │  │  │  OrcSnappyTableProperties.py   # Orc文件格式对象，用于封装Orc建表时的字符串
│  │  │  │  │  │  │  OrcTableProperties.py         # Orc文件格式加Snappy压缩的对象
│  │  │  │  │  │  │  TableProperties.py            # 用于获取表的属性的类
│  │  │  │  ├─utils                                # 程序中使用到的工具类的包名
│  │  │  │  │  │  ConfigUtil.py                    # 用于加载配置文件，获取配置文件信息
│  │  │  │  │  │  ConnectUtil.py                   # 用于获取Oracle连接、SparkSQL连接
│  │  │  │  │  │  OracleMetaUtil.py                # 用于获取Oracle中表的信息：表名、字段名、类型、注释等
│  │  │  │  │  │  ReadFileUtil.py                  # 用于读写文件，获取所有Oracle表的名称
│  │  │  │  │  │  TableNameUtil.py                 # 用于将全量表和增量表的名称放入不同的列表中
│  │  ├─config                                     # 配置日志的脚本的包名
│  │  │  │  common.py                              # 用于获取日志的类
│  │  │  │  settings.py                            # 用于配置日志记录方式的类
│  │  ├─logs                                       # 日志存放位置
│  │  │      alex.log                          # 日志文件
│  │  ├─resource                                   # 配置文件
│  │  │      config.txt                            # Oracle、SparkSQL的地址、端口、用户名、密码等配置信息
│  ├─DataPlatform                                  # 数据平台主要逻辑的脚本的包名
│  └─Data_Integration                              # 数据集成的脚本的包名
│      ├─python
│      │      full_import_tables.py                # python实现sqoop抽取Oracle全量表到HDFS
│      │      incr_import_tables.py                # python实现sqoop抽取Oracle增量表到HDFS
│      │      upload_avro_schema.py                # python实现sqoop上传每张表的Schema信息到HDFS
│      │
│      └─shell
│          └─sqoop_script
│                  full_import_tables.sh           # shell实现sqoop抽取Oracle全量表到HDFS
│                  full_import_tables.txt          # 全量表清单
│                  incr_import_tables.sh           # shell实现sqoop抽取Oracle增量表到HDFS
│                  incr_import_tables.txt          # 增量表清单
│                  upload_avro_schema.sh           # shell实现sqoop上传每张表的Schema信息到HDFS
│
└─Pip
  └─sasl-0.3.1-cp39-cp39-win_amd64.whl             # python实现本地操作SparkSQL的whl文件
```

