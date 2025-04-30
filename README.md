# arch_demo
1) make virtual environment
```
python -m venv venv
```
or
```
python3 -m venv venv
```
2) then
```
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt  
```

in first terminal 
```
uvicorn backend:app --reload --host 0.0.0.0 --port 8000               
```

in second terminal
```
streamlit run frontend.py 
```
