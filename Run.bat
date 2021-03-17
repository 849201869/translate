pushd %~dp0

set python=D:\computer\anaconda\python.exe
set pyfile=D:\00work\0Robbie\translate\Text_transAPI.py
set file=D:\00work\0Robbie\translate
set from_lang=zh
set to_lang=en

python %pyfile% %file% %from_lang% %to_lang% 

popd
pause
