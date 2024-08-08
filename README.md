## video_to_text

get audio from video , and transfer to text，then optimize the text，           
generate new audio，then split the text，use single sentence to generate image，                
finally generate video              

# run

```
poetry shell 
poetry install
poetry run python app.py
```



## poetry using
```
env:   

pip3 install poetry    

初始化：    
poetry init    

打开虚拟环境：       
poetry shell   

退出虚拟环境：
exit

如果有toml文件，可以直接把lib统一安装
poetry install

安装单个包
poetry add flask [--dev]

移除单个包
poetry remove dep_name

执行脚本
poetry run python app.py

更新所有锁定版本的依赖
poetry update

更改源
[[tool.poetry.source]]
name = "mirrors"
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
priority = "default"
```


## warning
1. 注意mac上生成的c++动态包，需要改为.so文件，否则boost.python无法使用
2. openai-whisper安装的时候使用poetry add git+https://github.com/openai/whisper.git 





