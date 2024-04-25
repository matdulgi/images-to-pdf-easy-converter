@echo off
setlocal

echo === Starting Build Process === 

echo creating python virtual environment..
python -m venv venv

echo entering python virtual environment
call .\venv\Scripts\activate

echo installing required python packages
pip install Pillow reportlab pyinstaller pyQt5

echo start to build 
pyinstaller.exe -n images_to_pdf_easy_converter --clean --onefile --noconsole images_to_pdf_easy_converter.py
echo build complete!
echo executable's generated in %CD%\dist\images_to_pdf_easy_converter.exe

deactivate

echo === Build Success! ===
