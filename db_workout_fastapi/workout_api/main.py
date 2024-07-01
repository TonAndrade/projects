from fastapi import FastAPI

app = FastAPI(title='minha_api')

'''if __name__=='main':
    import uvicorn      
    # Use 0000 para host local; /
    # O log_level serve para mostrar o quão detalhadas serão as informações mostradas no resultado. Neste caso, queremos apenas mostrar info.
    # Use o reload para recarregar o servidor caso faça alerações quando ativo. /
    uvicorn.run('main:app',host='0.0.0.0', port=8000, log_level='info', reload=True)'''