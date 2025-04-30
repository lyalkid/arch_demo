# arch_demo

```
python -m venv venv
source venv/bin/activate  
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